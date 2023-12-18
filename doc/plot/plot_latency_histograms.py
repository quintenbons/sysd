#!/usr/bin/env python3
import polars as pl
import plotly.graph_objects as go
import plotly.express as px

def plot_histograms(file1, file2):
    df1 = pl.read_csv(file1)
    df2 = pl.read_csv(file2)

    df1 = df1.sample(len(df2))

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df1["delay"], name="same machine"))
    fig.add_trace(go.Histogram(x=df2["delay"], name="same cluster"))

    fig.update_layout(barmode='overlay', title_text='Latency Histograms', width=800, height=400)
    fig.update_traces(opacity=0.75)
    fig.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file1')
    parser.add_argument('file2')
    args = parser.parse_args()

    plot_histograms(args.file1, args.file2)
