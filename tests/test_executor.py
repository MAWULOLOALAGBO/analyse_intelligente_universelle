import pandas as pd
from core.parser import parse_query
from core.validator import validate_plan
from core.executor import execute

def test_execute_mean():
    df = pd.DataFrame({"Age": [10, 20, 30]})
    plan = validate_plan(parse_query("moyenne de Age", df), df)
    result = execute(plan, df)
    assert result["success"] is True
    assert result["result"] == 20

