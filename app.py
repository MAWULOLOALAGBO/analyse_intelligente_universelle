import streamlit as st
import pandas as pd

from core.loader import load_file
from core.typing_cleaning import infer_types
from core.parser import parse_query
from core.validator import validate_plan
from core.executor import execute

st.set_page_config(page_title="Data Brain Assistant", layout="wide", page_icon="🧠")

if "data" not in st.session_state:
    st.session_state.data = None
if "metadata" not in st.session_state:
    st.session_state.metadata = None
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🧠 Data Brain Assistant")
st.markdown("*Analyse universelle de données — Tout fichier, toute question*")

st.header("1. Chargez votre fichier")
uploaded_file = st.file_uploader(
    "CSV, Excel, JSON, Parquet, ou texte structuré",
    type=["csv", "xlsx", "xls", "json", "parquet", "txt"]
)

if uploaded_file:
    try:
        df, meta = load_file(uploaded_file)
        df = infer_types(df)
        st.session_state.data = df
        st.session_state.metadata = meta

        st.success(
            f"✅ {meta['rows']:,} lignes × {meta['columns']} colonnes | "
            f"Mémoire: {meta['memory_mb']:.1f} MB"
        )

        with st.expander("🔍 Aperçu et structure"):
            tab1, tab2, tab3 = st.tabs(["Données", "Types", "Statistiques rapides"])

            with tab1:
                st.dataframe(df.head(10), use_container_width=True)

            with tab2:
                type_info = pd.DataFrame({
                    "Colonne": df.columns,
                    "Type détecté": df.dtypes.astype(str),
                    "Valeurs uniques": [df[c].nunique() for c in df.columns],
                    "Valeurs manquantes": [df[c].isnull().sum() for c in df.columns],
                    "Exemple": [
                        str(df[c].dropna().iloc[0]) if df[c].dropna().shape[0] > 0 else "N/A"
                        for c in df.columns
                    ],
                })
                st.dataframe(type_info, use_container_width=True)

            with tab3:
                st.write(df.describe(include="all").transpose())

    except Exception as e:
        st.error(f"❌ Erreur de chargement : {str(e)}")

if st.session_state.data is not None:
    df = st.session_state.data

    st.header("2. Posez votre question")
    query = st.text_input(
        "Exemples : 'moyenne de Age', 'histogramme de Age', 'corrélation entre Age et Stress_Level'",
        placeholder="Décrivez ce que vous voulez analyser..."
    )

    if query:
        with st.spinner("🧠 Analyse de la requête..."):
            plan = parse_query(query, df)
            plan = validate_plan(plan, df)

            st.subheader("📋 Plan compris")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Intention :** `{plan['intention']}`")
                st.write(f"**Opération :** `{plan['operation']}`")
            with col2:
                st.write(f"**Colonnes :** {', '.join(plan['columns']) if plan['columns'] else 'Aucune'}")
                st.write(f"**Groupby :** {plan['groupby'] or 'Aucun'}")
            with col3:
                st.write(f"**Valide :** {'✅ Oui' if plan['valid'] else '❌ Non'}")
                if plan["errors"]:
                    st.write("**Erreurs :**")
                    for err in plan["errors"]:
                        st.write(f"- {err}")

            st.subheader("🚀 Résultat")

            result = execute(plan, df)

            if not result["success"]:
                st.error(result["error"])
            else:
                if result["figure"] is not None:
                    st.plotly_chart(result["figure"], use_container_width=True)

                if isinstance(result["result"], pd.DataFrame):
                    st.dataframe(result["result"], use_container_width=True)
                elif isinstance(result["result"], (int, float)):
                    st.metric("Résultat", f"{result['result']:.4f}")
                elif isinstance(result["result"], str):
                    st.success(result["result"])
                elif result["result"] is not None:
                    st.write(result["result"])

                st.session_state.history.append(
                    {
                        "query": query,
                        "intention": plan["intention"],
                        "operation": plan["operation"],
                        "success": result["success"],
                    }
                )

with st.sidebar:
    st.header("📜 Historique des requêtes")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-15:]):
            icon = "✅" if item["success"] else "❌"
            st.write(f"{icon} {item['query'][:40]}...")
            st.caption(f"{item['intention']} | {item['operation']}")
            st.divider()
    else:
        st.write("Aucune requête encore")

    if st.button("🗑️ Effacer l'historique"):
        st.session_state.history = []
        st.rerun()

