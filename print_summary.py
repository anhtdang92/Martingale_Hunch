import pandas as pd

try:
    df = pd.read_csv('output/comparative_summary.csv')
    print(df.to_markdown(index=False))
except Exception as e:
    print(f"Error: {e}")
