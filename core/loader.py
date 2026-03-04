import pandas as pd
import json
from io import StringIO

def load_file(uploaded_file):
    """
    Charge n'importe quel fichier (CSV, Excel, JSON, Parquet, TXT)
    et renvoie un DataFrame + métadonnées.
    """

    file_name = uploaded_file.name.lower()

    try:
        # CSV
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        # Excel
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)

        # JSON (plusieurs formats possibles)
        elif file_name.endswith(".json"):
            try:
                df = pd.read_json(uploaded_file)
            except:
                uploaded_file.seek(0)
                content = uploaded_file.read().decode("utf-8")

                try:
                    data = json.loads(content)
                    if isinstance(data, dict):
                        df = pd.json_normalize(data)
                    else:
                        df = pd.DataFrame(data)
                except:
                    uploaded_file.seek(0)
                    df = pd.DataFrame([json.loads(line) for line in uploaded_file])

        # Parquet
        elif file_name.endswith(".parquet"):
            df = pd.read_parquet(uploaded_file)

        # TXT (tentative CSV)
        elif file_name.endswith(".txt"):
            uploaded_file.seek(0)
            content = uploaded_file.read().decode("utf-8")
            try:
                df = pd.read_csv(StringIO(content), sep=None, engine="python")
            except:
                df = pd.DataFrame({"content": content.split("\n")})

        else:
            raise ValueError("Format non reconnu")

        metadata = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "memory_mb": df.memory_usage(deep=True).sum() / 1024**2,
            "column_names": list(df.columns),
        }

        return df, metadata

    except Exception as e:
        raise Exception(f"Erreur de chargement : {str(e)}")

