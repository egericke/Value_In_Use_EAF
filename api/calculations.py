import numpy as np

# Constants from model
MW_SI, MW_SIO2, MW_CAO, MW_MGO = 28.09, 60.08, 56.08, 40.30
MW_AL, MW_AL2O3, MW_FE, MW_FEO = 26.98, 101.96, 55.85, 71.85
MW_C, MW_MN, MW_MNO, MW_P, MW_P2O5 = 12.01, 54.94, 70.94, 30.97, 141.94

DH_SI, DH_C_CO, DH_C_CO2 = -910.9, -110.5, -393.5  # kJ/mol
DH_AL, DH_FE, DH_MN = -1675 / 2, -272, -385

CHEM_EFF = 0.8
POST_COMB_EFF = 0.3
BURNER_SUB = 7.5  # kWh/Nm3 natural gas
SLAG_SPEC_HEAT = 0.6  # kWh/kg slag
USEFUL_ETA = 0.65
INFIL_AIR_FRAC = 0.5
DECARB_MAX = 0.1  # %C/min
CO_FRAC = 0.7

def calculate_energy_credit(kg_element, dh, mw, eff=CHEM_EFF):
    mol = kg_element / mw
    energy_kj = -dh * mol
    kwh = (energy_kj / 3600) * eff * USEFUL_ETA
    return kwh

def compute_viu(material, params):
    charge_kg = params['furnace_capacity_ton'] * 1000

    # Element masses
    kg_fe = material["pct_fe"] / 100 * charge_kg
    kg_c = material["pct_c"] / 100 * charge_kg
    kg_si = material["pct_si"] / 100 * charge_kg
    kg_mn = material["pct_mn"] / 100 * charge_kg
    kg_al = material["pct_al"] / 100 * charge_kg
    kg_p = material["pct_p"] / 100 * charge_kg
    kg_s = material["pct_s"] / 100 * charge_kg
    kg_cu = material["pct_cu"] / 100 * charge_kg
    kg_sn = material["pct_sn"] / 100 * charge_kg

    # Gangue
    kg_gangue_sio2 = material["gangue_sio2"] / 100 * charge_kg
    kg_gangue_al2o3 = material["gangue_al2o3"] / 100 * charge_kg
    kg_gangue_cao = material["gangue_cao"] / 100 * charge_kg
    kg_gangue_mgo = material["gangue_mgo"] / 100 * charge_kg
    kg_gangue_feo = material["gangue_feo"] / 100 * charge_kg

    # Oxidation
    kg_sio2_ox = kg_si * (MW_SIO2 / MW_SI)
    kg_al2o3_ox = kg_al * (MW_AL2O3 / (2 * MW_AL))
    kg_mno_ox = kg_mn * (MW_MNO / MW_MN)
    kg_p2o5_ox = kg_p * (MW_P2O5 / (2 * MW_P))

    total_sio2 = kg_sio2_ox + kg_gangue_sio2
    total_al2o3 = kg_al2o3_ox + kg_gangue_al2o3
    total_acidic = total_sio2 + total_al2o3

    # Flux
    required_cao = params['basicity_target'] * total_sio2 - kg_gangue_cao
    required_mgo = (params['mgo_sat_target'] / 100 * (total_acidic + required_cao)) - kg_gangue_mgo
    required_mgo = max(0, required_mgo)
    dolo_kg = required_mgo / 0.4
    lime_kg = required_cao - dolo_kg * 0.6
    lime_kg = max(0, lime_kg)
    flux_penalty = (lime_kg / 1000 * params['lime_cost_ton'] + dolo_kg / 1000 * params['dololime_cost_ton']) / (charge_kg / 1000)  # $/ton charge

    # Slag and yield
    total_slag_no_feo = total_acidic + kg_gangue_cao + required_cao + kg_gangue_mgo + required_mgo + kg_mno_ox + kg_p2o5_ox + kg_gangue_feo
    feo_pct = 20 + (total_slag_no_feo / charge_kg * 100) * 0.05 - params['target_c'] * 10
    feo_pct = np.clip(feo_pct, 10, 30)
    kg_feo = (feo_pct / 100) * total_slag_no_feo / (1 - feo_pct / 100)
    total_slag = total_slag_no_feo + kg_feo
    lost_fe = kg_feo * (MW_FE / MW_FEO)
    metallic_fe_in = kg_fe + kg_gangue_feo * (MW_FE / MW_FEO) * (material["metallization"] / 100)
    liquid_steel_kg = metallic_fe_in - lost_fe
    yield_pct = (liquid_steel_kg / charge_kg) * 100
    yield_loss_penalty = (lost_fe / 1000 * params['fe_value_ton']) / (charge_kg / 1000)
    slag_vol = total_slag / (charge_kg / 1000)  # kg/t charge

    # Energy
    credit_si = calculate_energy_credit(kg_si, DH_SI, MW_SI) * params['electricity_cost']
    credit_al = calculate_energy_credit(kg_al, DH_AL, MW_AL) * params['electricity_cost']
    credit_mn = calculate_energy_credit(kg_mn, DH_MN, MW_MN) * params['electricity_cost']
    credit_c = calculate_energy_credit(kg_c, (CO_FRAC * DH_C_CO + (1 - CO_FRAC) * DH_C_CO2), MW_C) * params['electricity_cost']
    credit_post = credit_c * (1 - CO_FRAC) * POST_COMB_EFF
    preheat_credit = 75 if params['preheat'] else 0  # kWh/ton
    credit_temp = max(0, (material["temp"] - 25) * 0.0004 * charge_kg / 1000) * params['electricity_cost']  # $/charge
    energy_credit = (credit_si + credit_al + credit_mn + credit_c + credit_post + credit_temp + preheat_credit) / (charge_kg / 1000)  # $/ton

    slag_energy_penalty = total_slag * SLAG_SPEC_HEAT * params['electricity_cost'] / (charge_kg / 1000)

    # Oxygen
    o2_kg_total = kg_si * (32 / MW_SI) + kg_c * (16 / MW_C * 0.5 * CO_FRAC + 32 / MW_C * (1 - CO_FRAC)) + kg_al * (48 / (2 * MW_AL)) + kg_mn * (16 / MW_MN) + lost_fe * (16 / (2 * MW_FE)) + kg_p * (80 / (2 * MW_P))
    o2_nm3 = o2_kg_total / 1.429
    oxygen_penalty = o2_nm3 * params['o2_cost_nm3'] / (charge_kg / 1000)

    # Residual penalties (dilution cost per ton)
    dil_cu = max(0, (material["pct_cu"] - params['target_cu']) / (material["pct_cu"] - params['prime']['pct_cu'])) if material["pct_cu"] > params['target_cu'] else 0
    dil_sn = max(0, (material["pct_sn"] - params['target_sn']) / (material["pct_sn"] - params['prime']['pct_sn'])) if material["pct_sn"] > params['target_sn'] else 0
    copper_dil_penalty = dil_cu * params['prime']["price"]
    tin_penalty = dil_sn * params['prime']["price"]

    # P and S penalties (assume ladle desulf/dephos cost, e.g., $80 per 0.01% P, $300 per 0.01% S)
    p_penalty = max(0, material["pct_p"] - params['target_p']) * 8000  # $/ton for excess
    s_penalty = max(0, material["pct_s"] - params['target_s']) * 30000

    # VIU per NT
    total_cost_ton_charge = material["price"] + flux_penalty + slag_energy_penalty + yield_loss_penalty + oxygen_penalty + copper_dil_penalty + p_penalty + s_penalty + tin_penalty - energy_credit
    viu_per_nt = total_cost_ton_charge / (yield_pct / 100)

    return {
        "Base Price": material["price"],
        "Energy Credit": energy_credit,
        "Flux Cost Penalty": flux_penalty,
        "Slag Energy Penalty": slag_energy_penalty,
        "Yield Loss Penalty": yield_loss_penalty,
        "Oxygen Cost Penalty": oxygen_penalty,
        "Copper Dilution Penalty": copper_dil_penalty,
        "Phosphorus Penalty": p_penalty,
        "Sulfur (Ladle) Penalty": s_penalty,
        "Tin Penalty": tin_penalty,
        "VIU Cost / NT": viu_per_nt,
        "Predicted Yield (%)": yield_pct,
        "Slag Volume (kg/t)": slag_vol,
        "Copper (%)": material["pct_cu"],
        "Phosphorus (%)": material["pct_p"],
        "Sulfur (%)": material["pct_s"],
        "Tin (%)": material["pct_sn"]
    }
