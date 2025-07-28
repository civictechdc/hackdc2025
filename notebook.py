import marimo

__generated_with = "0.12.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    from data import fetch_comments_df
    return fetch_comments_df, mo, pl


@app.cell
def _(mo):
    text_input = mo.ui.text(placeholder="Enter Docket ID")
    return (text_input,)


@app.cell
def _(text_input):
    text_input
    return


@app.cell
def _(fetch_comments_df, mo, text_input):
    with mo.status.spinner(title="Fetching comments. Be patient...") as _spinner:
        df = fetch_comments_df(docket_id=text_input.value)
    return (df,)


@app.cell
def _(df, mo):
    mo.md(f"Fetched {len(df)} comments!")
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _(df):
    df.head(5)
    return


@app.cell
def _(df, pl):
    (
        df
        .filter(pl.col("comment").is_duplicated())
        .select(pl.col("comment").unique())
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
