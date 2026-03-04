import pandas as pd
import numpy as np

def check_missing(df, plan):
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if missing.empty:
        return "Aucune valeur manquante", None
    return missing, None

def check_duplicates(df, plan):
    dup = df.duplicated().sum()
    return f"{dup} lignes dupliquées", None

def detect_outliers(df, plan):
    col = plan["columns"][0]
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
    return f"{len(outliers)} valeurs aberrantes détectées", None

