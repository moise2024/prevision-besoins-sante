"""Crée des séries entièrement fictives pour tester le pipeline."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = np.random.default_rng(2026)
centers = pd.DataFrame([
    ("FICT-01", "Centre fictif A", 5.336, -4.026, 260),
    ("FICT-02", "Centre fictif B", 5.360, -3.990, 190),
    ("FICT-03", "Centre fictif C", 5.300, -4.080, 150),
    ("FICT-04", "Centre fictif D", 5.385, -4.050, 220),
    ("FICT-05", "Centre fictif E", 5.275, -3.970, 120),
    ("FICT-06", "Centre fictif F", 5.415, -3.940, 175),
], columns=["centre_id", "nom_fictif", "latitude_fictive", "longitude_fictive", "niveau_base_fictif"])
centers.drop(columns="niveau_base_fictif").to_csv(DATA / "centres_fictifs.csv", index=False)
rows = []
dates = pd.date_range("2022-01-01", "2025-12-01", freq="MS")
for i, row in centers.iterrows():
    base = [260,190,150,220,120,175][i]
    for t, dt in enumerate(dates):
        season = 1 + .15*np.sin(2*np.pi*dt.month/12) + .05*np.cos(2*np.pi*dt.month/12)
        trend = 1 + .002*t
        visits = max(0, round(base*season*trend + rng.normal(0, base*.07)))
        rows.append((row.centre_id, dt.strftime("%Y-%m-%d"), visits))
pd.DataFrame(rows, columns=["centre_id", "mois", "visites"]).to_csv(DATA / "frequentation_mensuelle_simulee.csv", index=False)
