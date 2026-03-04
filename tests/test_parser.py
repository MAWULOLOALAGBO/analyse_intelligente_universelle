import pandas as pd
from core.parser import parse_query

def test_parse_mean():
    df = pd.DataFrame({"Age": [20, 30, 40]})
    plan = parse_query("moyenne de Age", df)
    assert plan["intention"] == "statistique"
    assert plan["operation"] == "mean"
    assert plan["columns"] == ["Age"]

