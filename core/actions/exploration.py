import pandas as pd
import plotly.express as px

def describe_data(df, plan):
    return df.describe(include="all").transpose(), None

def show_types(df, plan):
    info = pd.DataFrame({
        "Type": df.dtypes.astype(str),
        "Non_Null": df.count(),
        "Null": df.isnull().sum(),
        "Unique": df.nunique()
    })
    return info, None

def compute_correlation(df, plan):
    numeric = df.select_dtypes(include="number")
    corr = numeric.corr()
    fig = px.imshow(corr, text_auto=True, title="Matrice de corrélation")
    return corr, fig

