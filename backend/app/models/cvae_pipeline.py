# app/models/cvae_pipeline.py

import torch
from joblib import load
import json
import pandas as pd
import numpy as np
from app.models.cvae_model import CVAE

class CVAEPipeline:
    def __init__(self, model, scaler, ohe, target_cols, config):
        self.model = model
        self.scaler = scaler
        self.ohe = ohe
        self.target_cols = target_cols
        self.config = config

    @classmethod
    def load(cls, path: str):
        import torch
        from joblib import load
        import json

        with open(f"{path}/cvae_config.json") as f:
            config = json.load(f)

        model = CVAE(
            input_dim=config["input_dim"],
            cond_dim=config["cond_dim"],
            latent_dim=config["latent_dim"]
        )

        state_dict = torch.load(f"{path}/cvae_weights.pth", map_location="cpu")
        model.load_state_dict(state_dict)

        model.eval()

        scaler = load(f"{path}/scaler.pkl")
        ohe = load(f"{path}/ohe.pkl")
        target_cols = load(f"{path}/target_cols.pkl")

        return cls(model, scaler, ohe, target_cols, config)

    def generate(self, conditions: dict, n_samples: int = 1):
        import pandas as pd
        import numpy as np
        import torch

        self.model.eval()

        # 1. DataFrame
        df = pd.DataFrame([conditions])

        # 2. признаки
        cat_cols = self.config["categorical_features"]
        num_cols = self.config["numerical_features"]

        # categorical
        if len(cat_cols) > 0:
            cat_encoded = self.ohe.transform(df[cat_cols])

            if hasattr(cat_encoded, "toarray"):
                cat_encoded = cat_encoded.toarray()
        else:
            cat_encoded = np.empty((1, 0))

        # numerical
        if len(num_cols) > 0:
            num_data = df[num_cols].values
        else:
            num_data = np.empty((1, 0))

        # порядок как в обучении
        C = np.hstack([cat_encoded, num_data])

        C_tensor = torch.tensor(C, dtype=torch.float32)

        samples = []

        for _ in range(n_samples):
            z = torch.randn(1, self.config["latent_dim"])

            with torch.no_grad():
                sample = self.model.decode(z, C_tensor)

            samples.append(sample.numpy())

        samples = np.vstack(samples)

        # ✅ scaler применяется только к output
        samples_real = self.scaler.inverse_transform(samples)

        df_out = pd.DataFrame(samples_real, columns=self.target_cols)

        return df_out.to_dict(orient="records")