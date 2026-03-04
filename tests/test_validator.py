import pandas as pd
from core.parser import parse_query
from core.validator import validate_plan

def test_validator_numeric_mean():
    df = pd.DataFrame({"Age": [10, 20, 30]})
    plan = parse_query("moyenne de Age", df)
    plan = validate_plan(plan, df)
    assert plan["valid"] is True

