from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "backend" / "data" / "solar.csv"

df = pd.read_csv(DATA_PATH)

print("Rows and columns:", df.shape)

print("\nColumns and data types:")
print(df.dtypes.to_string())

print("\nMissing values:")
print(df.isna().sum().to_string())

print("\nEclipse type codes:")
print(df["Eclipse Type"].str[0].value_counts().to_string())

print("\n2026 eclipses:")
print(
    df.loc[
        df["Calendar Date"].str.startswith("2026")
    ].to_string(index=False)
)