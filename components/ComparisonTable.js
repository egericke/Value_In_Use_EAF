'use client';

import { useState, useEffect } from 'react';

export default function ComparisonTable() {
  const [materials, setMaterials] = useState([]);
  const [mat1Idx, setMat1Idx] = useState(0);
  const [mat2Idx, setMat2Idx] = useState(1);
  const [blendPct, setBlendPct] = useState(50);
  const [results, setResults] = useState(null);

  useEffect(() => {
    fetch('/api/materials').then(res => res.json()).then(setMaterials);
  }, []);

  const handleCompute = async () => {
    const params = { /* Gather params from inputs or defaults */ };
    const data = { mat1_idx: mat1Idx, mat2_idx: mat2Idx, blend_pct1: blendPct, params };
    const res = await fetch('/api/compute_viu', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    setResults(await res.json());
  };

  return (
    <div>
      <h2 className="text-2xl mb-2">Compare</h2>
      <select onChange={(e) => setMat1Idx(e.target.value)}>{materials.map((m, i) => <option value={i}>{m.name}</option>)}</select>
      <select onChange={(e) => setMat2Idx(e.target.value)}>{materials.map((m, i) => <option value={i}>{m.name}</option>)}</select>
      <input type="range" min="0" max="100" value={blendPct} onChange={(e) => setBlendPct(e.target.value)} />
      <button onClick={handleCompute} className="bg-green-500 text-white p-2">Compute</button>
      {results && (
        <table className="table-auto w-full mt-4">
          <thead><tr><th>Component</th><th>{results.mat1_name}</th><th>{results.mat2_name}</th><th>Blended</th></tr></thead>
          <tbody>
            <tr><td>Base Price</td><td>{results.res1.base_price}</td><td>{results.res2.base_price}</td><td>{results.res_blend.base_price}</td></tr>
            <tr style={{color: 'green'}}><td>Energy Credit</td><td>{results.res1.energy_credit}</td><td>{results.res2.energy_credit}</td><td>{results.res_blend.energy_credit}</td></tr>
            {/* Add all rows with styles: red for penalties, lightblue for VIU */}
          </tbody>
        </table>
      )}
    </div>
  );
}
