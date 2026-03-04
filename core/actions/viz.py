import plotly.express as px

def plot_histogram(df, plan):
    col = plan["columns"][0]
    fig = px.histogram(df, x=col, title=f"Distribution de {col}")
    return None, fig

def plot_bar(df, plan):
    col = plan["columns"][0]
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, "count"]
    fig = px.bar(counts, x=col, y="count", title=f"Répartition de {col}")
    return counts, fig

def plot_pie(df, plan):
    col = plan["columns"][0]
    counts = df[col].value_counts().reset_index()
    counts.columns = [col, "count"]
    fig = px.pie(counts, names=col, values="count", title=f"Répartition de {col}")
    return counts, fig

def plot_scatter(df, plan):
    col1, col2 = plan["columns"][:2]
    fig = px.scatter(df, x=col1, y=col2, title=f"{col1} vs {col2}")
    return None, fig

def plot_line(df, plan):
    col = plan["columns"][0]
    fig = px.line(df, y=col, title=f"Évolution de {col}")
    return None, fig

