'use client';

import { useState } from 'react';

export default function MaterialForm() {
  const [materials, setMaterials] = useState([]);
  const [formData, setFormData] = useState({
    name: '', price: 0, pct_fe: 98, pct_c: 0.2, pct_si: 0.5, pct_mn: 0.5, pct_al: 0.1,
    pct_p: 0.02, pct_s: 0.03, pct_cu: 0.4, pct_sn: 0.015, gangue_sio2: 0.5, gangue_al2o3: 0.3,
    gangue_cao: 0.1, gangue_mgo: 0.1, gangue_feo: 1.0, density: 7800, metallization: 100, temp: 25
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: parseFloat(e.target.value) || e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setMaterials([...materials, formData]);
    alert(`Added ${formData.name}`);
    // Reset form if needed
  };

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-semibold mb-2">Add Raw Material</h2>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
        <input name="name" placeholder="Name" onChange={handleChange} className="p-2 border rounded" required />
        <input name="price" type="number" placeholder="Price ($/ton)" onChange={handleChange} className="p-2 border rounded" />
        {/* Add all other inputs similarly */}
        <input name="pct_fe" type="number" step="0.01" placeholder="%Fe" value={formData.pct_fe} onChange={handleChange} className="p-2 border rounded" />
        <input name="pct_c" type="number" step="0.01" placeholder="%C" value={formData.pct_c} onChange={handleChange} className="p-2 border rounded" />
        <input name="pct_si" type="number" step="0.01" placeholder="%Si" value={formData.pct_si} onChange={handleChange} className="p-2 border rounded" />
        <input name="pct_mn" type="number" step="0.01" placeholder="%Mn" value={formData.pct_mn} onChange={handleChange} className="p-2 border rounded" />
        <input name="pct_al" type="number" step="0.01" placeholder="%Al" value={formData.pct_al} onChange={handleChange} className="p-2 border rounded" />
        <input name="pct_p" type="number" step="0.01" placeholder="%P" value={formData.pct_p} onChange={handleChange} className="p-2 border rounded" />
        <input name="pct_s" type="number" step="0.01" placeholder="%S" value={formData.pct_s} onChange={handleChange} className="p-2 border rounded" />
        <input name="pct_cu" type="number" step="0.01" placeholder="%Cu" value={formData.pct_cu} onChange={handleChange} className="p-2 border rounded" />
        <input name="pct_sn" type="number" step="0.01" placeholder="%Sn" value={formData.pct_sn} onChange={handleChange} className="p-2 border rounded" />
        <input name="gangue_sio2" type="number" step="0.01" placeholder="% gangue SiO2" value={formData.gangue_sio2} onChange={handleChange} className="p-2 border rounded" />
        <input name="gangue_al2o3" type="number" step="0.01" placeholder="% gangue Al2O3" value={formData.gangue_al2o3} onChange={handleChange} className="p-2 border rounded" />
        <input name="gangue_cao" type="number" step="0.01" placeholder="% gangue CaO" value={formData.gangue_cao} onChange={handleChange} className="p-2 border rounded" />
        <input name="gangue_mgo" type="number" step="0.01" placeholder="% gangue MgO" value={formData.gangue_mgo} onChange={handleChange} className="p-2 border rounded" />
        <input name="gangue_feo" type="number" step="0.01" placeholder="% gangue FeO" value={formData.gangue_feo} onChange={handleChange} className="p-2 border rounded" />
        <input name="density" type="number" placeholder="Density (kg/m3)" value={formData.density} onChange={handleChange} className="p-2 border rounded" />
        <input name="metallization" type="number" placeholder="Metallization %" value={formData.metallization} onChange={handleChange} className="p-2 border rounded" />
        <input name="temp" type="number" placeholder="Input temp (C)" value={formData.temp} onChange={handleChange} className="p-2 border rounded" />
        <button type="submit" className="col-span-2 bg-blue-500 text-white p-2 rounded">Add Material</button>
      </form>
      {materials.length > 0 && (
        <table className="mt-4 w-full border">
          <thead><tr><th>Name</th><th>Price</th>{/* Add headers */}</tr></thead>
          <tbody>{materials.map((m, i) => <tr key={i}><td>{m.name}</td><td>{m.price}</td>{/* Add cells */}</tr>)}</tbody>
        </table>
      )}
    </div>
  );
}
