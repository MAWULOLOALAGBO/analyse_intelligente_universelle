import pandas as pd
import numpy as np

def compute_mean(df, plan):
    col = plan["columns"][0]
    return df[col].mean(), None

def compute_median(df, plan):
    col = plan["columns"][0]
    return df[col].median(), None

def compute_std(df, plan):
    col = plan["columns"][0]
    return df[col].std(), None

def compute_variance(df, plan):
    col = plan["columns"][0]
    return df[col].var(), None

def compute_min(df, plan):
    col = plan["columns"][0]
    return df[col].min(), None

def compute_max(df, plan):
    col = plan["columns"][0]
    return df[col].max(), None

def compute_sum(df, plan):
    col = plan["columns"][0]
    return df[col].sum(), None

