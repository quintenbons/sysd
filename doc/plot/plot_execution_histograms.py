#!/usr/bin/env python3
import polars as pl
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def plot_histograms(csv_file):
    df = pl.read_csv(csv_file)
    df = df.with_columns((pl.col("all_jobs_done_time") - pl.col("start_time")).alias("total_time"))

    fig = px.histogram(df.to_pandas(), x="total_time")
    fig.update_layout(width=700, title_text="Histograms of CSV Columns")
    fig.show()

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('csv_file')
  args = parser.parse_args()

  plot_histograms(args.csv_file)
