import plotly.express as px
import pandas as pd

df = pd.read_csv("coverageData.csv")
fig = px.treemap(df, path=['label', 'rule_ID', 'TPs'], 
                 values='examples_covered', color='label')
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
print(df.head(5))
fig.show()