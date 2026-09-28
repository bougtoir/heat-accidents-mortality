#!/usr/bin/env python3
"""
Japan crash-circumstance strata: deaths per prefecture-day by accident type
(NPA honhyo field 事故類型). Codes (codebook_2022.xlsx, sheet 事故類型（本票）):
  01 pedestrian vs vehicle (the fatality is the struck pedestrian)
  21 vehicle vs vehicle
  41 single-vehicle
  61 train crossing accident
Other/unknown codes are grouped as "other".

Output: data/processed/jp_pref_day_type.csv
        (pref_id, pref_name, date, atype, deaths)
"""
import os
import pandas as pd
from build_japan import YEARS, NPA, NPA_URL, PROC, download, pref_code_map

ATYPE = {"01": "vehicle_pedestrian", "21": "vehicle_vehicle",
         "41": "single_vehicle"}
Y = ["発生日時\u3000\u3000年", "発生日時\u3000\u3000月", "発生日時\u3000\u3000日"]


def main():
    cmap = pref_code_map()
    frames = []
    for y in YEARS:
        p = download(f"{NPA_URL}/{y}/honhyo_{y}.csv",
                     os.path.join(NPA, f"honhyo_{y}.csv"))
        df = pd.read_csv(p, encoding="cp932", dtype=str,
                         usecols=["都道府県コード", "死者数", "事故類型"] + Y)
        df["deaths"] = df["死者数"].astype(int)
        df["date"] = pd.to_datetime(dict(
            year=df[Y[0]].astype(int), month=df[Y[1]].astype(int),
            day=df[Y[2]].astype(int)), errors="coerce")
        df["pref_id"] = df["都道府県コード"].map(lambda c: cmap.get(c, (pd.NA,))[0])
        df["pref_name"] = df["都道府県コード"].map(lambda c: cmap.get(c, (None, None))[1])
        df["atype"] = df["事故類型"].map(ATYPE).fillna("other")
        frames.append(df[["pref_id", "pref_name", "date", "atype", "deaths"]])
    acc = pd.concat(frames, ignore_index=True).dropna(subset=["date", "pref_id"])
    acc["pref_id"] = acc.pref_id.astype(int)
    out = (acc.groupby(["pref_id", "pref_name", "date", "atype"], as_index=False)
           .deaths.sum())
    out.to_csv(os.path.join(PROC, "jp_pref_day_type.csv"), index=False)
    print(out.groupby("atype").deaths.sum())
    print(f"saved jp_pref_day_type.csv ({len(out):,} rows)")


if __name__ == "__main__":
    main()
