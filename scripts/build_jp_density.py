#!/usr/bin/env python3
"""
Prefecture population density (persons/km2) as a proxy for public-transport
availability in Japan. Population comes from the 2020 national census and
area from the official administrative-area survey, as compiled in the
public prefecture table at en.wikipedia.org/wiki/Prefectures_of_Japan
(which cites the Statistics Bureau and GSI figures). Density is used only
to split prefectures at the median (transit-rich vs transit-poor proxy);
small reporting differences do not change group membership.

Output: data/processed/jp_pref_density.csv
"""
import os
import urllib.request
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROC = os.path.join(ROOT, "data", "processed")
os.makedirs(PROC, exist_ok=True)

URL = "https://en.wikipedia.org/wiki/Prefectures_of_Japan"
SUFFIX = ("\u90fd", "\u5e9c", "\u770c")   # 都, 府, 県


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req).read()
    tab = None
    for t in pd.read_html(html):
        cols = [str(c) for c in t.columns]
        if t.shape[0] >= 47 and any("2020" in c for c in cols) and any("Area" in c for c in cols):
            tab = t; break
    if tab is None:
        raise RuntimeError("prefecture table not found on page")
    popcol = next(c for c in tab.columns if "2020" in str(c))
    areacol = next(c for c in tab.columns if "Area" in str(c))
    jpcol = next(c for c in tab.columns
                 if str(tab[c].iloc[0]).endswith(SUFFIX) or str(tab[c].iloc[0]) == "\u5317\u6d77\u9053")
    d = pd.DataFrame({
        "pref_name": tab[jpcol].astype(str).str.replace("[\u90fd\u5e9c\u770c]$", "", regex=True),
        "pop2020": pd.to_numeric(tab[popcol].astype(str).str.replace(",", ""), errors="coerce"),
        "area_km2": pd.to_numeric(tab[areacol].astype(str).str.replace(",", ""), errors="coerce"),
    }).dropna()
    if len(d) != 47:
        raise RuntimeError(f"expected 47 prefectures, got {len(d)}")
    d["density"] = d.pop2020 / d.area_km2
    med = d.density.median()
    d["density_group"] = ["high_density" if v >= med else "low_density" for v in d.density]
    d.to_csv(os.path.join(PROC, "jp_pref_density.csv"), index=False)
    print(d.sort_values("density", ascending=False).to_string(index=False))
    print(f"\nmedian density {med:.1f}/km2 -> "
          f"{(d.density_group == 'high_density').sum()} high / "
          f"{(d.density_group == 'low_density').sum()} low")


if __name__ == "__main__":
    main()
