import { useState } from "react";
import axios from "axios";
import "./App.css";

const MATERIALS = ["Al2O3", "CuO", "Fe2O3", "TiO2", "ZnO"];

export default function App() {
  const [material, setMaterial] = useState(MATERIALS[0]);
  const [coreSize, setCoreSize] = useState("");
  const [surfCharge, setSurfCharge] = useState("");
  const [count, setCount] = useState(1);
  const [results, setResults] = useState([]);

  const generate = async () => {
    const res = await axios.post("/api/generate", {
      properties: {
        NPs: material,
        coresize: Number(coreSize),
        surfcharge: Number(surfCharge),
      },
      n_samples: Number(count),
    });

    setResults(res.data.results);
  };

  const downloadCSV = async () => {
    if (!results.length) return;

    const res = await axios.post(
      "/api/generate/csv",
      {
        model_used: "frontend-model", // 👈 добавили обязательное поле
        input_properties: {
          NPs: material,
          coresize: Number(coreSize),
          surfcharge: Number(surfCharge),
        },
        generated_count: results.length, // 👈 важно для backend
        results: results,
      },
      {
        responseType: "blob",
      }
    );

    // ❗ axios уже вернул blob — НЕ нужно создавать новый Blob
    const url = window.URL.createObjectURL(res.data);

    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "nanoparticles");

    document.body.appendChild(link);
    link.click();
    link.remove();

    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="container">
      <h1>Nanoparticle Generator</h1>

      <div className="form">
        <select value={material} onChange={(e) => setMaterial(e.target.value)}>
          {MATERIALS.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>

        <input
          placeholder="Core size"
          value={coreSize}
          onChange={(e) => setCoreSize(e.target.value)}
        />

        <input
          placeholder="Surface charge"
          value={surfCharge}
          onChange={(e) => setSurfCharge(e.target.value)}
        />

        <input
          type="number"
          min="1"
          placeholder="Count"
          value={count}
          onChange={(e) => setCount(e.target.value)}
        />

        <button onClick={generate}>Generate</button>

        <button onClick={downloadCSV} disabled={!results.length}>
          Download CSV
        </button>
      </div>

      <table>
        <thead>
          <tr>
            {results[0] &&
              Object.keys(results[0]).map((k) => <th key={k}>{k}</th>)}
          </tr>
        </thead>

        <tbody>
          {results.map((r, i) => (
            <tr key={i}>
              {Object.values(r).map((v, j) => (
                <td key={j}>{v}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
