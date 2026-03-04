import pandas as pd
import numpy as np

def infer_types(df):
    """
    Inférence douce des types :
    - Convertit en numérique si >95% des valeurs sont convertibles
    - Convertit en datetime si >95% des valeurs sont convertibles
    - Convertit en catégorie si peu de valeurs uniques
    """

    df = df.copy()

    for col in df.columns:
        series = df[col]

        # Détection numérique douce
        if series.dtype == "object":
            cleaned = series.str.replace(",", ".", regex=False).str.replace(" ", "", regex=False)
            numeric = pd.to_numeric(cleaned, errors="coerce")

            if numeric.notna().mean() > 0.95:
                df[col] = numeric
                continue

        # Détection datetime douce
        if series.dtype == "object":
            dt = pd.to_datetime(series, errors="coerce")
            if dt.notna().mean() > 0.95:
                df[col] = dt
                continue

        # Détection catégorielle
        if df[col].nunique() < 0.05 * len(df):
            df[col] = df[col].astype("category")

    return df

