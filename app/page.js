'use client';

import { useState, useEffect } from 'react';
import MaterialForm from '../components/MaterialForm';
import ComparisonTable from '../components/ComparisonTable';
import OperationalParametersForm from '../components/OperationalParametersForm';

export default function Home() {
  const [materials, setMaterials] = useState([]);
  const [params, setParams] = useState({
    electricity_cost: 0.07,
    o2_cost_nm3: 0.15,
    ng_cost_nm3: 0.20,
    lime_cost_ton: 150.0,
    dololime_cost_ton: 200.0,
    carbon_cost_kg: 0.5,
    electrode_cost_kg: 5.0,
    refractory_cost_index: 10.0,
    time_cost_min: 20.0,
    fe_value_ton: 400.0,
    basicity_target: 2.5,
    v_ratio_target: 2.5,
    mgo_sat_target: 12.0,
    target_c: 0.5,
    target_p: 0.02,
    target_s: 0.02,
    target_cu: 0.10,
    target_sn: 0.01,
    tapping_temp: 1650.0,
    base_ttt: 60.0,
    furnace_capacity_ton: 100.0,
    preheat: false,
    scrap_type_factor: 1.0,
    prime: {
        name: "DRI",
        price: 450.0,
        pct_cu: 0.01,
        pct_sn: 0.001
    }
  });

  useEffect(() => {
    fetch('/api/materials').then(res => res.json()).then(setMaterials);
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">EAF Raw Material VIU Comparison Tool</h1>
      <OperationalParametersForm params={params} setParams={setParams} />
      <MaterialForm materials={materials} setMaterials={setMaterials} />
      {materials.length >= 2 && <ComparisonTable materials={materials} setMaterials={setMaterials} params={params} />}
    </div>
  );
}
