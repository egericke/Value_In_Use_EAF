'use client';

import { useState } from 'react';

export default function MaterialForm({ materials, setMaterials }) {
  const [formState, setFormState] = useState({
    name: '',
    price: 0,
    pct_fe: 98.0,
    pct_c: 0.2,
    pct_si: 0.5,
    pct_mn: 0.5,
    pct_al: 0.1,
    pct_p: 0.02,
    pct_s: 0.03,
    pct_cu: 0.4,
    pct_sn: 0.015,
    gangue_sio2: 0.5,
    gangue_al2o3: 0.3,
    gangue_cao: 0.1,
    gangue_mgo: 0.1,
    gangue_feo: 1.0,
    density: 7800.0,
    metallization: 100.0,
    temp: 25.0
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormState(prevState => ({
      ...prevState,
      [name]: name === 'name' ? value : parseFloat(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await fetch('/api/add_material', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(formState)
    });
    // Refresh materials
    fetch('/api/materials').then(res => res.json()).then(setMaterials);
  };

  return (
    <div>
      <h2 className="text-2xl mb-2">Add Raw Material</h2>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Object.keys(formState).map(key => (
          <input
            key={key}
            name={key}
            type={key === 'name' ? 'text' : 'number'}
            placeholder={key.replace(/_/g, ' ')}
            value={formState[key]}
            onChange={handleChange}
            required
            className="p-2 border"
          />
        ))}
        <button type="submit" className="col-span-2 md:col-span-4 bg-blue-500 text-white p-2">Add Material</button>
      </form>
      {materials.length > 0 && (
        <div>
          <h2 className="text-2xl mb-2 mt-4">Added Materials</h2>
          <table className="table-auto w-full">
            <thead>
              <tr>
                {Object.keys(materials[0]).map(key => <th key={key} className="px-4 py-2">{key.replace(/_/g, ' ')}</th>)}
              </tr>
            </thead>
            <tbody>
              {materials.map((material, index) => (
                <tr key={index}>
                  {Object.values(material).map((value, i) => <td key={i} className="border px-4 py-2">{typeof value === 'number' ? value.toFixed(3) : value}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
