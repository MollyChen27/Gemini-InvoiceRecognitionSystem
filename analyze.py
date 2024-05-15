import pandas as pd
import matplotlib.pyplot as plt

def amountPerMonth(df): # 消費金額
    monthly_total = df.groupby(df["date"])["total"].sum()
    print(monthly_total)

def typeUnique(df):
    type_counts = df["type"].value_counts()
    print(type_counts)
   