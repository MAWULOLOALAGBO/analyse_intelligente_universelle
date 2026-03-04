import pandas as pd
import numpy as np

NUMERIC_OPS = ["mean", "median", "std", "variance", "min", "max", "sum"]
VISUAL_NUMERIC = ["histogram", "line", "scatter"]
VISUAL_CATEGORICAL = ["bar", "pie"]
CLEANING_OPS = ["missing", "duplicates", "outliers"]
EXPLORATION_OPS = ["describe", "types", "correlation"]

def validate_columns(plan, df):
    errors = []
    cols = plan["columns"]

    if not cols:
        return ["Aucune colonne détectée dans la requête."]

    for col in cols:
        if col not in df.columns:
            errors.append(f"La colonne '{col}' n'existe pas dans les données.")

    return errors

def validate_groupby(plan, df):
    group = plan["groupby"]
    if group is None:
        return []

    if group not in df.columns:
        return [f"La colonne de groupement '{group}' n'existe pas."]

    if not pd.api.types.is_categorical_dtype(df[group]) and not df[group].dtype == object:
        return [f"La colonne '{group}' doit être catégorielle pour un groupby."]

    return []

def validate_operation(plan, df):
    op = plan["operation"]
    cols = plan["columns"]
    errors = []

    # Statistiques numériques
    if op in NUMERIC_OPS:
        for col in cols:
            if not pd.api.types.is_numeric_dtype(df[col]):
                errors.append(f"L'opération '{op}' nécessite une colonne numérique : '{col}' ne l'est pas.")

    # Visualisations numériques
    if op in VISUAL_NUMERIC:
        for col in cols:
            if not pd.api.types.is_numeric_dtype(df[col]):
                errors.append(f"Un graphique '{op}' nécessite une colonne numérique : '{col}' ne l'est pas.")

    # Visualisations catégorielles
    if op in VISUAL_CATEGORICAL:
        col = cols[0]
        if not (pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == object):
            errors.append(f"Un graphique '{op}' nécessite une colonne catégorielle : '{col}' ne l'est pas.")

    # Scatter → 2 colonnes numériques
    if op == "scatter":
        if len(cols) != 2:
            errors.append("Un scatter nécessite exactement 2 colonnes.")
        else:
            for col in cols:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    errors.append(f"Scatter impossible : '{col}' n'est pas numérique.")

    # Corrélation → au moins 2 colonnes numériques
    if op == "correlation":
        numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
        if len(numeric_cols) < 2:
            errors.append("Une corrélation nécessite au moins 2 colonnes numériques.")

    return errors

def validate_plan(plan, df):
    """
    Vérifie que le plan est logique, cohérent et exécutable.
    Retourne un plan annoté avec valid=True/False et une liste d'erreurs.
    """

    errors = []

    # Vérification colonnes
    errors += validate_columns(plan, df)

    # Vérification groupby
    errors += validate_groupby(plan, df)

    # Vérification opération
    errors += validate_operation(plan, df)

    plan["valid"] = len(errors) == 0
    plan["errors"] = errors

    return plan

