import dash
import dash_bootstrap_components as dbc
from layouts import serve_layout
from data_loader import load_data
from callbacks import register_callbacks

# Load datasets
df, df2, df3, df4 = load_data()

# Extract years & months dynamically
years = sorted(df.index.year.unique())
months = df2["month"].unique().tolist()

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Electra.AI"

# Set layout
app.layout = lambda: serve_layout(years, months)

# Register callbacks
register_callbacks(app, df, df2, df3, df4)

if __name__ == "__main__":
    app.run(debug=True)
