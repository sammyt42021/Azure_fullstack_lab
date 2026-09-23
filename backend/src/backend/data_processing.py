import pandas as pd

from backend.constants import SOLAR_CSV

df = pd.read_csv(SOLAR_CSV, dtype={"Catalog Number": str})

df["year"] = df["Calendar Date"].str.extract(r"^(-?\d+)")[0].astype(int)

df["type"] = df["Eclipse Type"].str[0]

df = df.astype(object).where(pd.notna(df), None)