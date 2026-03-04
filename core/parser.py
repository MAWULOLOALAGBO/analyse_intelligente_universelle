import re

INTENT_KEYWORDS = {
    "statistique": ["moyenne", "mean", "médiane", "median", "écart", "std", "variance", "min", "max", "somme", "total"],
    "visualisation": ["histogramme", "hist", "bar", "barplot", "camembert", "pie", "scatter", "nuage", "ligne", "line"],
    "nettoyage": ["manquant", "missing", "null", "na", "doublon", "duplicate", "outlier", "anomalie"],
    "exploration": ["describe", "résumé", "structure", "types", "corrélation", "correlation", "overview"]
}

OPERATION_MAP = {
    "moyenne": "mean",
    "mean": "mean",
    "médiane": "median",
    "median": "median",
    "écart": "std",
    "std": "std",
    "variance": "variance",
    "min": "min",
    "max": "max",
    "somme": "sum",
    "total": "sum",

    "histogramme": "histogram",
    "hist": "histogram",
    "bar": "bar",
    "barplot": "bar",
    "camembert": "pie",
    "pie": "pie",
    "scatter": "scatter",
    "nuage": "scatter",
    "ligne": "line",
    "line": "line",

    "manquant": "missing",
    "missing": "missing",
    "null": "missing",
    "doublon": "duplicates",
    "duplicate": "duplicates",
    "outlier": "outliers",
    "anomalie": "outliers",

    "describe": "describe",
    "résumé": "describe",
    "structure": "types",
    "types": "types",
    "corrélation": "correlation",
    "correlation": "correlation"
}

def detect_intention(query):
    q = query.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(k in q for k in keywords):
            return intent
    return "exploration"

def detect_operation(query):
    q = query.lower()
    for key, op in OPERATION_MAP.items():
        if key in q:
            return op
    return "describe"

def extract_columns(query, df):
    q = query.lower()
    cols = list(df.columns)
    matches = []

    for col in cols:
        col_low = col.lower()
        if col_low in q:
            matches.append(col)
        else:
            words = re.findall(r"\b\w+\b", q)
            for w in words:
                if len(w) > 2 and w in col_low:
                    matches.append(col)

    matches = list(dict.fromkeys(matches))
    return matches

def extract_groupby(query, df):
    q = query.lower()
    match = re.search(r"par\s+(\w+)", q)
    if not match:
        return None

    candidate = match.group(1)
    for col in df.columns:
        if candidate.lower() in col.lower():
            return col

    return None

def parse_query(query, df):
    intention = detect_intention(query)
    operation = detect_operation(query)
    columns = extract_columns(query, df)
    groupby = extract_groupby(query, df)

    plan = {
        "intention": intention,
        "operation": operation,
        "columns": columns,
        "groupby": groupby,
        "valid": True,
        "errors": []
    }

    if len(columns) == 0 and operation not in ["describe", "types"]:
        plan["valid"] = False
        plan["errors"].append("Aucune colonne détectée dans la requête.")

    if len(columns) > 2 and operation in ["scatter"]:
        plan["valid"] = False
        plan["errors"].append("Un scatter nécessite exactement 2 colonnes.")

    return plan

