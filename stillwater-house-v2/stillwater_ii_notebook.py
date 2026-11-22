import marimo

app = marimo.App(width="full")

@app.cell
def _():
    import marimo as mo
    from pathlib import Path
    root = Path(__file__).parent
    return mo, root

@app.cell
def _(mo):
    mo.md("# STILLWATER HOUSE II\nA stepped limestone residence, glazed atelier and expansive water garden.")
    return

@app.cell
def _(mo, root):
    mo.ui.tabs({
        "01 · Expanded residence": mo.image(root / "renders/01-Expanded-Residence.png"),
        "02 · Poolside architecture": mo.image(root / "renders/02-Poolside-Architecture.png"),
        "03 · Garden leisure": mo.image(root / "renders/03-Garden-Leisure.png"),
    })
    return

@app.cell
def _(mo, root):
    mo.md((root / "README.md").read_text())
    return

if __name__ == "__main__":
    app.run()
