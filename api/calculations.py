import streamlit as st
import pandas as pd
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

# Streamlit App
st.title("EAF Raw Material VIU Comparison Tool")

st.write("Define parameters, add materials, select two for comparison, and compute blended summary.")

# Sidebar for parameters
with st.sidebar:
    st.header("Operational Parameters")
    electricity_cost = st.number_input("Electricity cost ($/kWh)", value=0.07)
    o2_cost_nm3 = st.number_input("Oxygen cost ($/Nm3)", value=0.15)
    ng_cost_nm3 = st.number_input("Natural gas cost ($/Nm3)", value=0.20)
    lime_cost_ton = st.number_input("Lime cost ($/ton)", value=150.0)
    dololime_cost_ton = st.number_input("Dolo-lime cost ($/ton)", value=200.0)
    carbon_cost_kg = st.number_input("Injected carbon cost ($/kg)", value=0.5)
    electrode_cost_kg = st.number_input("Electrode cost ($/kg)", value=5.0)
    refractory_cost_index = st.number_input("Refractory cost index ($/heat/point)", value=10.0)
    time_cost_min = st.number_input("Productivity cost ($/min)", value=20.0)
    fe_value_ton = st.number_input("Fe value ($/ton)", value=400.0)
    basicity_target = st.number_input("Target basicity (CaO/SiO2)", value=2.5)
    v_ratio_target = st.number_input("Target V-ratio", value=2.5)
    mgo_sat_target = st.number_input("Target MgO %", value=12.0)
    target_c = st.number_input("Target %C", value=0.5)
    target_p = st.number_input("Target max %P", value=0.02)
    target_s = st.number_input("Target max %S", value=0.02)
    target_cu = st.number_input("Target max %Cu", value=0.10)
    target_sn = st.number_input("Target max %Sn", value=0.01)
    tapping_temp = st.number_input("Tapping temp (C)", value=1650.0)
    base_ttt = st.number_input("Base tap-to-tap time (min)", value=60.0)
    furnace_capacity_ton = st.number_input("Furnace capacity (ton)", value=100.0)
    preheat = st.checkbox("Enable preheating", value=False)
    preheat_credit = 75 if preheat else 0  # kWh/ton
    scrap_type_factor = st.number_input("Scrap type factor (1=heavy, 0.8=light)", value=1.0)
    useful_eta = USEFUL_ETA * scrap_type_factor

    # Prime diluent
    st.header("Prime Diluent")
    prime_name = st.text_input("Name", value="DRI")
    prime_price = st.number_input("Price ($/ton)", value=450.0)
    prime_cu = st.number_input("%Cu", value=0.01)
    prime_sn = st.number_input("%Sn", value=0.001)
    prime = {"name": prime_name, "price": prime_price, "pct_cu": prime_cu, "pct_sn": prime_sn, "pct_fe": 92.0, "pct_c": 1.5, "pct_si": 1.0, 
             "pct_mn": 0.5, "pct_al": 0.5, "pct_p": 0.01, "pct_s": 0.01, "gangue_sio2": 2.0, "gangue_al2o3": 1.5, "gangue_cao": 0.5, 
             "gangue_mgo": 0.5, "gangue_feo": 3.0, "density": 2500, "metallization": 92.0, "temp": 25.0}  # Assumed defaults for DRI

# Session state for materials
if 'materials' not in st.session_state:
    st.session_state.materials = []

# Add material form
st.header("Add Raw Materials")
with st.form("add_material"):
    name = st.text_input("Name")
    price = st.number_input("Price ($/ton)")
    pct_fe = st.number_input("%Fe", value=98.0)
    pct_c = st.number_input("%C", value=0.2)
    pct_si = st.number_input("%Si", value=0.5)
    pct_mn = st.number_input("%Mn", value=0.5)
    pct_al = st.number_input("%Al", value=0.1)
    pct_p = st.number_input("%P", value=0.02)
    pct_s = st.number_input("%S", value=0.03)
    pct_cu = st.number_input("%Cu", value=0.4)
    pct_sn = st.number_input("%Sn", value=0.015)
    gangue_sio2 = st.number_input("% gangue SiO2", value=0.5)
    gangue_al2o3 = st.number_input("% gangue Al2O3", value=0.3)
    gangue_cao = st.number_input("% gangue CaO", value=0.1)
    gangue_mgo = st.number_input("% gangue MgO", value=0.1)
    gangue_feo = st.number_input("% gangue FeO", value=1.0)
    density = st.number_input("Density (kg/m3)", value=7800.0)
    metallization = st.number_input("Metallization %", value=100.0)
    temp = st.number_input("Input temp (C)", value=25.0)

    submitted = st.form_submit_button("Add Material")
    if submitted:
        material = {
            "name": name, "price": price, "pct_fe": pct_fe, "pct_c": pct_c, "pct_si": pct_si,
            "pct_mn": pct_mn, "pct_al": pct_al, "pct_p": pct_p, "pct_s": pct_s,
            "pct_cu": pct_cu, "pct_sn": pct_sn, "gangue_sio2": gangue_sio2,
            "gangue_al2o3": gangue_al2o3, "gangue_cao": gangue_cao, "gangue_mgo": gangue_mgo,
            "gangue_feo": gangue_feo, "density": density, "metallization": metallization, "temp": temp
        }
        st.session_state.materials.append(material)
        st.success(f"Added {name}")

# Display materials
if st.session_state.materials:
    st.subheader("Added Materials")
    df_mats = pd.DataFrame(st.session_state.materials)
    st.dataframe(df_mats.style.format("{:.3f}"))

# Comparison
st.header("Compare Two Materials with Blend")
if len(st.session_state.materials) >= 2:
    col1, col2, col3 = st.columns(3)
    with col1:
        mat1_idx = st.selectbox("Material 1", range(len(st.session_state.materials)), format_func=lambda i: st.session_state.materials[i]["name"])
    with col2:
        mat2_idx = st.selectbox("Material 2", range(len(st.session_state.materials)), format_func=lambda i: st.session_state.materials[i]["name"])
    with col3:
        blend_pct1 = st.slider("Blend % of Material 1", 0, 100, 50)

    if st.button("Compute VIU Summary"):
        mat1 = st.session_state.materials[mat1_idx]
        mat2 = st.session_state.materials[mat2_idx]
        w1 = blend_pct1 / 100
        w2 = 1 - w1
        blended = {k: w1 * mat1.get(k, 0) + w2 * mat2.get(k, 0) for k in mat1 if k != "name"}

        def compute_viu(material, charge_kg):
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
            required_cao = basicity_target * total_sio2 - kg_gangue_cao
            required_mgo = (mgo_sat_target / 100 * (total_acidic + required_cao)) - kg_gangue_mgo
            required_mgo = max(0, required_mgo)
            dolo_kg = required_mgo / 0.4
            lime_kg = required_cao - dolo_kg * 0.6
            lime_kg = max(0, lime_kg)
            flux_penalty = (lime_kg / 1000 * lime_cost_ton + dolo_kg / 1000 * dololime_cost_ton) / (charge_kg / 1000)  # $/ton charge

            # Slag and yield
            total_slag_no_feo = total_acidic + kg_gangue_cao + required_cao + kg_gangue_mgo + required_mgo + kg_mno_ox + kg_p2o5_ox + kg_gangue_feo
            feo_pct = 20 + (total_slag_no_feo / charge_kg * 100) * 0.05 - target_c * 10
            feo_pct = np.clip(feo_pct, 10, 30)
            kg_feo = (feo_pct / 100) * total_slag_no_feo / (1 - feo_pct / 100)
            total_slag = total_slag_no_feo + kg_feo
            lost_fe = kg_feo * (MW_FE / MW_FEO)
            metallic_fe_in = kg_fe + kg_gangue_feo * (MW_FE / MW_FEO) * (material["metallization"] / 100)
            liquid_steel_kg = metallic_fe_in - lost_fe
            yield_pct = (liquid_steel_kg / charge_kg) * 100
            yield_loss_penalty = (lost_fe / 1000 * fe_value_ton) / (charge_kg / 1000)
            slag_vol = total_slag / (charge_kg / 1000)  # kg/t charge

            # Energy
            credit_si = calculate_energy_credit(kg_si, DH_SI, MW_SI) * electricity_cost
            credit_al = calculate_energy_credit(kg_al, DH_AL, MW_AL) * electricity_cost
            credit_mn = calculate_energy_credit(kg_mn, DH_MN, MW_MN) * electricity_cost
            credit_c = calculate_energy_credit(kg_c, (CO_FRAC * DH_C_CO + (1 - CO_FRAC) * DH_C_CO2), MW_C) * electricity_cost
            credit_post = credit_c * (1 - CO_FRAC) * POST_COMB_EFF
            credit_temp = max(0, (material["temp"] - 25) * 0.0004 * charge_kg / 1000) * electricity_cost  # $/charge
            energy_credit = (credit_si + credit_al + credit_mn + credit_c + credit_post + credit_temp + preheat_credit) / (charge_kg / 1000)  # $/ton

            slag_energy_penalty = total_slag * SLAG_SPEC_HEAT * electricity_cost / (charge_kg / 1000)

            # Oxygen
            o2_kg_total = kg_si * (32 / MW_SI) + kg_c * (16 / MW_C * 0.5 * CO_FRAC + 32 / MW_C * (1 - CO_FRAC)) + kg_al * (48 / (2 * MW_AL)) + kg_mn * (16 / MW_MN) + lost_fe * (16 / (2 * MW_FE)) + kg_p * (80 / (2 * MW_P))
            o2_nm3 = o2_kg_total / 1.429
            oxygen_penalty = o2_nm3 * o2_cost_nm3 / (charge_kg / 1000)

            # Residual penalties (dilution cost per ton)
            dil_cu = max(0, (material["pct_cu"] - target_cu) / (material["pct_cu"] - prime["pct_cu"])) if material["pct_cu"] > target_cu else 0
            dil_sn = max(0, (material["pct_sn"] - target_sn) / (material["pct_sn"] - prime["pct_sn"])) if material["pct_sn"] > target_sn else 0
            copper_dil_penalty = dil_cu * prime["price"]
            tin_penalty = dil_sn * prime["price"]

            # P and S penalties (assume ladle desulf/dephos cost, e.g., $80 per 0.01% P, $300 per 0.01% S)
            p_penalty = max(0, material["pct_p"] - target_p) * 8000  # $/ton for excess
            s_penalty = max(0, material["pct_s"] - target_s) * 30000

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

        # Compute for mat1, mat2, blended
        res1 = compute_viu(mat1, furnace_capacity_ton * 1000)
        res2 = compute_viu(mat2, furnace_capacity_ton * 1000)
        res_blend = compute_viu(blended, furnace_capacity_ton * 1000)

        # DataFrame
        df = pd.DataFrame({
            mat1["name"]: res1,
            mat2["name"]: res2,
            "Blended Summary": res_blend
        })

        # Styling
        def style_row(row):
            styles = []
            for val, idx in zip(row, df.index):
                if idx == "Energy Credit":
                    styles.append('color: green; font-weight: bold')
                elif 'Penalty' in idx:
                    styles.append('color: red')
                elif idx == "VIU Cost / NT":
                    styles.append('background-color: lightblue; font-weight: bold')
                else:
                    styles.append('')
            return styles

        styled_df = df.style.apply(style_row, axis=1).format("{:.3f}")

        st.subheader("VIU Comparison Summary")
        st.dataframe(styled_df)
else:
    st.info("Add at least two materials to compare.")
