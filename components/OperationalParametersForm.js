'use client';

import { useState } from 'react';

export default function OperationalParametersForm({ params, setParams }) {
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setParams(prevParams => ({
      ...prevParams,
      [name]: type === 'checkbox' ? checked : parseFloat(value)
    }));
  };

  const handlePrimeChange = (e) => {
    const { name, value } = e.target;
    setParams(prevParams => ({
      ...prevParams,
      prime: {
        ...prevParams.prime,
        [name]: value
      }
    }));
  };

  return (
    <div>
      <h2 className="text-2xl mb-2">Operational Parameters</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <input name="electricity_cost" type="number" value={params.electricity_cost} onChange={handleChange} placeholder="Electricity cost ($/kWh)" className="p-2 border" />
        <input name="o2_cost_nm3" type="number" value={params.o2_cost_nm3} onChange={handleChange} placeholder="Oxygen cost ($/Nm3)" className="p-2 border" />
        <input name="ng_cost_nm3" type="number" value={params.ng_cost_nm3} onChange={handleChange} placeholder="Natural gas cost ($/Nm3)" className="p-2 border" />
        <input name="lime_cost_ton" type="number" value={params.lime_cost_ton} onChange={handleChange} placeholder="Lime cost ($/ton)" className="p-2 border" />
        <input name="dololime_cost_ton" type="number" value={params.dololime_cost_ton} onChange={handleChange} placeholder="Dolo-lime cost ($/ton)" className="p-2 border" />
        <input name="carbon_cost_kg" type="number" value={params.carbon_cost_kg} onChange={handleChange} placeholder="Injected carbon cost ($/kg)" className="p-2 border" />
        <input name="electrode_cost_kg" type="number" value={params.electrode_cost_kg} onChange={handleChange} placeholder="Electrode cost ($/kg)" className="p-2 border" />
        <input name="refractory_cost_index" type="number" value={params.refractory_cost_index} onChange={handleChange} placeholder="Refractory cost index ($/heat/point)" className="p-2 border" />
        <input name="time_cost_min" type="number" value={params.time_cost_min} onChange={handleChange} placeholder="Productivity cost ($/min)" className="p-2 border" />
        <input name="fe_value_ton" type="number" value={params.fe_value_ton} onChange={handleChange} placeholder="Fe value ($/ton)" className="p-2 border" />
        <input name="basicity_target" type="number" value={params.basicity_target} onChange={handleChange} placeholder="Target basicity (CaO/SiO2)" className="p-2 border" />
        <input name="v_ratio_target" type="number" value={params.v_ratio_target} onChange={handleChange} placeholder="Target V-ratio" className="p-2 border" />
        <input name="mgo_sat_target" type="number" value={params.mgo_sat_target} onChange={handleChange} placeholder="Target MgO %" className="p-2 border" />
        <input name="target_c" type="number" value={params.target_c} onChange={handleChange} placeholder="Target %C" className="p-2 border" />
        <input name="target_p" type="number" value={params.target_p} onChange={handleChange} placeholder="Target max %P" className="p-2 border" />
        <input name="target_s" type="number" value={params.target_s} onChange={handleChange} placeholder="Target max %S" className="p-2 border" />
        <input name="target_cu" type="number" value={params.target_cu} onChange={handleChange} placeholder="Target max %Cu" className="p-2 border" />
        <input name="target_sn" type="number" value={params.target_sn} onChange={handleChange} placeholder="Target max %Sn" className="p-2 border" />
        <input name="tapping_temp" type="number" value={params.tapping_temp} onChange={handleChange} placeholder="Tapping temp (C)" className="p-2 border" />
        <input name="base_ttt" type="number" value={params.base_ttt} onChange={handleChange} placeholder="Base tap-to-tap time (min)" className="p-2 border" />
        <input name="furnace_capacity_ton" type="number" value={params.furnace_capacity_ton} onChange={handleChange} placeholder="Furnace capacity (ton)" className="p-2 border" />
        <div className="flex items-center">
          <input name="preheat" type="checkbox" checked={params.preheat} onChange={handleChange} className="mr-2" />
          <label>Enable preheating</label>
        </div>
        <input name="scrap_type_factor" type="number" value={params.scrap_type_factor} onChange={handleChange} placeholder="Scrap type factor (1=heavy, 0.8=light)" className="p-2 border" />
      </div>
      <h3 className="text-xl mt-4 mb-2">Prime Diluent</h3>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <input name="name" value={params.prime.name} onChange={handlePrimeChange} placeholder="Name" className="p-2 border" />
        <input name="price" type="number" value={params.prime.price} onChange={handlePrimeChange} placeholder="Price ($/ton)" className="p-2 border" />
        <input name="pct_cu" type="number" value={params.prime.pct_cu} onChange={handlePrimeChange} placeholder="%Cu" className="p-2 border" />
        <input name="pct_sn" type="number" value={params.prime.pct_sn} onChange={handlePrimeChange} placeholder="%Sn" className="p-2 border" />
      </div>
    </div>
  );
}
