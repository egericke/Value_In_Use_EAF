'use client';

import { useState } from 'react';
import { computeVIU } from '../utils/calculations';  // Import calc function

export default function Comparison() {
  const [mat1, setMat1] = useState(null);
  const [mat2, setMat2] = useState(null);
  const [blendPct, setBlendPct] = useState(50);
  const [results, setResults] = useState(null);

  const handleCompute = () => {
    // Assume materials from global state or props; compute using imported function
    const res1 = computeVIU(mat1);
    const res2 = computeVIU(mat2);
    const blended = {};  // Blend logic
    const resBlend = computeVIU(blended);
    setResults({ res1, res2, resBlend });
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-2">Compare Materials</h2>
      {/* Selectors and slider */}
      <button onClick={handleCompute} className="bg-green-500 text-white p-2 rounded">Compute</button>
      {results && (
        <table className="mt-4 w-full border">
          <thead><tr><th>VIU Component</th><th>Mat1</th><th>Mat2</th><th>Blend</th></tr></thead>
          <tbody>
            {/* Rows with conditional coloring */}
            <tr><td>Base Price</td><td style={{color: 'black'}}>{results.res1.basePrice}</td>{/* etc */}</tr>
            {/* Add all rows */}
          </tbody>
        </table>
      )}
    </div>
  );
}
