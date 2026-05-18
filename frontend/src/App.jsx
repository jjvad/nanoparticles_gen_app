import { useState } from "react";
import axios from "axios";
import "./App.css";

const MATERIALS = ["Al2O3", "CuO", "Fe2O3", "TiO2", "ZnO"];

export default function App() {
  const [material, setMaterial] = useState("");
  const [coreSize, setCoreSize] = useState("");
  const [surfCharge, setSurfCharge] = useState("");
  const [count, setCount] = useState(1);

  const [generationData, setGenerationData] = useState(null);

  const generate = async () => {
    const properties = {};

    if (material) {
      properties.NPs = material;
    }

    if (coreSize !== "") {
      properties.coresize = Number(coreSize);
    }

    if (surfCharge !== "") {
      properties.surfcharge = Number(surfCharge);
    }

    const res = await axios.post("/api/generate", {
      properties,
      n_samples: Number(count),
    });

    setGenerationData(res.data);
  };

  const downloadCSV = async () => {
    if (!generationData) return;

    const res = await axios.post(
      "/api/generate/csv",
      generationData,
      {
        responseType: "blob",
      }
    );

    const blob = new Blob([res.data], {
      type: "text/csv",
    });

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;

    link.download = "nanoparticles.csv";

    document.body.appendChild(link);

    link.click();

    link.remove();

    window.URL.revokeObjectURL(url);
  };

  const formatValue = (value) => {
    if (typeof value === "number") {
      return value.toFixed(4);
    }

    return value;
  };

  return (
    <div className="container">
      <h1>Nanoparticle Generator</h1>

      <div className="form">
        <div className="input-group">
          <label>Nanoparticle Material</label>

          <select
            value={material}
            onChange={(e) => setMaterial(e.target.value)}
          >
            <option value="">Not selected</option>

            {MATERIALS.map((m) => (
              <option key={m} value={m}>
                {m}
              </option>
            ))}
          </select>
        </div>

        <div className="input-group">
          <label>Core Size</label>

          <input
            type="number"
            placeholder="Enter core size"
            value={coreSize}
            onChange={(e) => setCoreSize(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Surface Charge</label>

          <input
            type="number"
            placeholder="Enter surface charge"
            value={surfCharge}
            onChange={(e) => setSurfCharge(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>Samples Count</label>

          <input
            type="number"
            min="1"
            value={count}
            onChange={(e) => setCount(e.target.value)}
          />
        </div>

        <div className="buttons">
          <button className="primary-btn" onClick={generate}>
            Generate
          </button>

          <button
            className="secondary-btn"
            onClick={downloadCSV}
            disabled={!generationData?.results?.length}
          >
            Download CSV
          </button>
        </div>
      </div>

      {generationData?.results?.length > 0 && (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                {Object.keys(generationData.results[0]).map((k) => (
                  <th key={k}>{k}</th>
                ))}
              </tr>
            </thead>

            <tbody>
              {generationData.results.map((row, i) => (
                <tr key={i}>
                  {Object.values(row).map((value, j) => (
                    <td key={j}>{formatValue(value)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}