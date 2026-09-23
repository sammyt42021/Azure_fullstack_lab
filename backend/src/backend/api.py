from fastapi import FastAPI, HTTPException

from backend.data_processing import df

app = FastAPI(
    title="eClipseBord API",
    description="API for exploring NASA solar eclipse data",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/eclipses")
def get_eclipses(
    year_from: int = 1900,
    year_to: int = 2100,
    eclipse_type: str | None = None,
):
    if year_from > year_to:
        raise HTTPException(
            status_code=400,
            detail="year_from must be less than or equal to year_to",
        )

    filtered_df = df[df["year"].between(year_from, year_to)]

    if eclipse_type:
        filtered_df = filtered_df[
            filtered_df["type"] == eclipse_type.upper()
        ]

    return {
        "total": len(filtered_df),
        "items": filtered_df.head(500).to_dict(orient="records"),
    }