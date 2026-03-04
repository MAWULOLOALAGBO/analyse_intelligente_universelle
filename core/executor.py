from core.actions.stats import (
    compute_mean, compute_median, compute_std, compute_variance,
    compute_min, compute_max, compute_sum
)
from core.actions.viz import (
    plot_histogram, plot_bar, plot_pie, plot_scatter, plot_line
)
from core.actions.cleaning import (
    check_missing, check_duplicates, detect_outliers
)
from core.actions.exploration import (
    describe_data, show_types, compute_correlation
)

ACTIONS = {
    ("statistique", "mean"): compute_mean,
    ("statistique", "median"): compute_median,
    ("statistique", "std"): compute_std,
    ("statistique", "variance"): compute_variance,
    ("statistique", "min"): compute_min,
    ("statistique", "max"): compute_max,
    ("statistique", "sum"): compute_sum,

    ("visualisation", "histogram"): plot_histogram,
    ("visualisation", "bar"): plot_bar,
    ("visualisation", "pie"): plot_pie,
    ("visualisation", "scatter"): plot_scatter,
    ("visualisation", "line"): plot_line,

    ("nettoyage", "missing"): check_missing,
    ("nettoyage", "duplicates"): check_duplicates,
    ("nettoyage", "outliers"): detect_outliers,

    ("exploration", "describe"): describe_data,
    ("exploration", "types"): show_types,
    ("exploration", "correlation"): compute_correlation,
}

def execute(plan, df):
    """
    Exécute une action validée.
    Retourne un dictionnaire :
    {
        "success": True/False,
        "result": ...,
        "figure": ...,
        "error": None/str
    }
    """

    if not plan["valid"]:
        return {
            "success": False,
            "result": None,
            "figure": None,
            "error": "\n".join(plan["errors"])
        }

    key = (plan["intention"], plan["operation"])
    func = ACTIONS.get(key)

    if func is None:
        return {
            "success": False,
            "result": None,
            "figure": None,
            "error": f"Action non supportée : {key}"
        }

    try:
        output = func(df, plan)
        if isinstance(output, tuple):
            result, fig = output
        else:
            result, fig = output, None

        return {
            "success": True,
            "result": result,
            "figure": fig,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "result": None,
            "figure": None,
            "error": str(e)
        }

