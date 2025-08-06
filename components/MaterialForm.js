'use client';

import { useState, useEffect } from 'react';

export default function MaterialForm() {
  const [materials, setMaterials] = useState([]);

  useEffect(() => {
    fetch('/api/materials').then(res => res.json()).then(setMaterials);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);
    await fetch('/api/add_material', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    // Refresh materials
    fetch('/api/materials').then(res => res.json()).then(setMaterials);
  };

  return (
    <div>
      <h2 className="text-2xl mb-2">Add Raw Material</h2>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
        <input name="name" placeholder="Name" required className="p-2 border" />
        <input name="price" type="number" placeholder="Price ($/ton)" className="p-2 border" />
        {/* Add all 18 inputs as <input name="pct_fe" type="number" ... /> */}
        <button type="submit" className="col-span-2 bg-blue-500 text-white p-2">Add</button>
      </form>
      {materials.length > 0 && <table>{/* Display table */}</table>}
    </div>
  );
}
