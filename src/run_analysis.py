"""Analyse de démonstration reproductible; aucune donnée réelle de santé."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import folium
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def features(dates):
    dates = pd.DatetimeIndex(dates)
    t = (dates.year - dates[0].year) * 12 + (dates.month - dates[0].month)
    t = np.asarray(t, dtype=float)
    month = dates.month.to_numpy()
    return np.column_stack([t, np.sin(2*np.pi*month/12), np.cos(2*np.pi*month/12)])

def make_model(name):
    if name == "Régression linéaire":
        return LinearRegression()
    return make_pipeline(StandardScaler(), Ridge(alpha=1.0))

def main():
    df = pd.read_csv(DATA / "frequentation_mensuelle_simulee.csv", parse_dates=["mois"])
    centers = pd.read_csv(DATA / "centres_fictifs.csv")
    results, forecasts = [], []
    for cid, g in df.groupby("centre_id", sort=True):
        g = g.sort_values("mois").reset_index(drop=True)
        y = g.visites.astype(float).to_numpy()
        dates = g.mois
        cut = len(g)-12
        for name in ["Naïf saisonnier", "Régression linéaire", "Ridge"]:
            if name == "Naïf saisonnier":
                actual, pred = y[cut:], y[cut-12:cut]
            else:
                model = make_model(name)
                model.fit(features(dates.iloc[:cut]), y[:cut])
                actual, pred = y[cut:], model.predict(features(dates.iloc[cut:]))
            mape = float(np.mean(np.abs((actual-pred)/actual))*100) if np.all(actual != 0) else np.nan
            results.append({"centre_id": cid, "modele": name,
                            "MAE_visites": mean_absolute_error(actual, pred),
                            "RMSE_visites": np.sqrt(mean_squared_error(actual, pred)),
                            "MAPE_pct": mape})
        center_scores = [r for r in results if r["centre_id"] == cid]
        winner = min(center_scores, key=lambda r: r["MAE_visites"])["modele"]
        future_dates = pd.date_range(dates.iloc[-1] + pd.offsets.MonthBegin(1), periods=12, freq="MS")
        if winner == "Naïf saisonnier":
            future_y = np.tile(y[-12:], 1)
        else:
            model = make_model(winner)
            model.fit(features(dates), y)
            future_y = model.predict(features(future_dates))
        for dt, val in zip(future_dates, future_y):
            forecasts.append({"centre_id": cid, "mois": dt.strftime("%Y-%m-%d"),
                              "modele_retenu": winner, "visites_prevues_simulees": max(0, int(round(val)))})
    scores = pd.DataFrame(results)
    scores.to_csv(OUT / "model_comparison.csv", index=False)
    forecast = pd.DataFrame(forecasts).merge(centers, on="centre_id", validate="many_to_one")
    forecast.to_csv(OUT / "forecasts.csv", index=False)
    # Carte synthétique des visites prévues cumulées sur les 12 mois, données fictives.
    totals = forecast.groupby("centre_id", as_index=False).visites_prevues_simulees.sum().merge(centers, on="centre_id")
    features_geo = []
    # No third-party tile server: avoid OSM 403/policy blocks and keep points usable.
    m = folium.Map(location=[5.35, -4.02], zoom_start=10, tiles=None)
    for row in totals.itertuples():
        value = int(row.visites_prevues_simulees)
        popup = f"{row.nom_fictif} — {value:,} visites simulées prévues / 12 mois".replace(",", " ")
        folium.CircleMarker([row.latitude_fictive, row.longitude_fictive], radius=6 + value/250,
                            color="#135e96", fill=True, fill_opacity=.7, tooltip=popup).add_to(m)
        features_geo.append({"type":"Feature", "geometry":{"type":"Point","coordinates":[row.longitude_fictive,row.latitude_fictive]},
            "properties":{"centre_id":row.centre_id,"nom_fictif":row.nom_fictif,
                           "visites_prevues_simulees_12_mois":value,"statut":"DONNEES FICTIVES"}})
    m.get_root().html.add_child(folium.Element('<div style="position:fixed;top:10px;left:50px;z-index:9999;background:white;padding:8px;border:1px solid #888"><b>Démo uniquement — établissements et prévisions fictifs</b></div>'))
    m.save(OUT / "carte_besoins.html")
    (OUT / "centres_previsions.geojson").write_text(json.dumps({"type":"FeatureCollection","features":features_geo},ensure_ascii=False,indent=2), encoding="utf-8")
    (OUT / "carte_besoins.qgs").write_text(qgis_project(), encoding="utf-8")
    print(f"Résultats écrits dans {OUT}")

def qgis_project():
    # Lightweight QGIS project; relative GeoJSON path makes it portable.
    return '''<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis projectname="Health forecast demo" version="3.34"><title>DEMO UNIQUEMENT — données fictives</title>
<projectCrs><spatialrefsys><authid>EPSG:4326</authid></spatialrefsys></projectCrs>
<projectlayers><layer-tree-group name=""><layer-tree-layer name="Prévisions fictives sur 12 mois" source="./centres_previsions.geojson" providerKey="ogr" checked="Qt::Checked"/></layer-tree-group>
<mapcanvas><extent><xmin>-4.12</xmin><ymin>5.22</ymin><xmax>-3.88</xmax><ymax>5.48</ymax></extent></mapcanvas>
<layer-tree-group name="Données fictives"/></projectlayers></qgis>'''

if __name__ == "__main__":
    main()
