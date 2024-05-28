# -*- coding: utf-8 -*-
"""
Created on Tue May 28 00:09:22 2024

@author: Meenakshi P
"""

import plotly.express as px
from dash import Dash, dcc, html, Output, Input
import pandas as pd

app = Dash(__name__, title="DMel_App")
# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

df = pd.read_csv("p_dat.csv")
df["odor"] = df["odor"].str.lower()
stage = df["stage"].unique().tolist()
odors = df["odor"].unique().tolist()
options = [{"label": odor, "value": odor} for odor in odors]

app.layout = html.Div(
    [
        dcc.Checklist(
            options=options,
            inline=True,
            value=["benzaldehyde"],
            id="checklist",
        ),
        dcc.Graph(id="scatter"),
    ]
)


@app.callback(
    Output("scatter", "figure"),
    Input("checklist", "value"),
)
def update_figure(values):

    key = df.loc[df["odor"].isin(values), "CID"]    
    p_df = df[df["CID"].isin(key)]
    fig = px.scatter(
        p_df,
        x="log_conc",
        y="response",
        color="stage",
        facet_col="starvation_bool"
    )
    fig.add_hline(y=0.0)
    fig.update_layout(yaxis_range=[-1,1])
    fig.update_layout(xaxis_range=[-10,1])
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
    
# #internal check using n-amyl acetate CID 12348    
# df.loc[df["odor"] == "n-amyl acetate", ["CID", "response", "log_conc", "stage"]]
# df.loc[df["CID"] == 12348, ["CID", "response", "log_conc", "stage"]]

# #internal check using benzaldehyde CID     
# df.loc[df["odor"] == "benzaldehyde", ["CID", "response", "log_conc", "stage"]]
# df.loc[df["CID"] == 240, ["CID", "response", "log_conc", "stage"]]
