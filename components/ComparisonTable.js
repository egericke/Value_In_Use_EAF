'use client';

import { useState, useEffect } from 'react';

export default function ComparisonTable({ materials, setMaterials, params }) {
  const [mat1Idx, setMat1Idx] = useState(0);
  const [mat2Idx, setMat2Idx] = useState(1);
  const [blendPct, setBlendPct] = useState(50);
  const [results, setResults] = useState(null);

  const handleCompute = async () => {
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
      <h2 className="text-2xl mb-2 mt-4">Compare Materials</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <select onChange={(e) => setMat1Idx(e.target.value)} className="p-2 border">{materials.map((m, i) => <option key={i} value={i}>{m.name}</option>)}</select>
        <select onChange={(e) => setMat2Idx(e.target.value)} className="p-2 border">{materials.map((m, i) => <option key={i} value={i}>{m.name}</option>)}</select>
        <input type="range" min="0" max="100" value={blendPct} onChange={(e) => setBlendPct(e.target.value)} />
      </div>
      <button onClick={handleCompute} className="bg-green-500 text-white p-2 mt-2">Compute VIU Summary</button>
      {results && (
        <table className="table-auto w-full mt-4">
          <thead>
            <tr>
              <th className="px-4 py-2">Component</th>
              <th className="px-4 py-2">{results.mat1_name}</th>
              <th className="px-4 py-2">{results.mat2_name}</th>
              <th className="px-4 py-2">Blended</th>
            </tr>
          </thead>
          <tbody>
            {Object.keys(results.res1).map(key => (
              <tr key={key} style={{
                color: key.includes('Credit') ? 'green' : key.includes('Penalty') ? 'red' : 'black',
                backgroundColor: key.includes('VIU') ? 'lightblue' : 'transparent',
                fontWeight: key.includes('VIU') ? 'bold' : 'normal'
              }}>
                <td className="border px-4 py-2">{key}</td>
                <td className="border px-4 py-2">{results.res1[key].toFixed(2)}</td>
                <td className="border px-4 py-2">{results.res2[key].toFixed(2)}</td>
                <td className="border px-4 py-2">{results.res_blend[key].toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
