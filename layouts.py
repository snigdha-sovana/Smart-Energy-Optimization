from dash import html, dcc
import dash_bootstrap_components as dbc

def serve_layout(years, months):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("⚡ Electra.AI Dashboard", className="app-title"),
                html.P("Monitor, forecast, and detect anomalies in electricity usage", className="subtitle"),

                dcc.Dropdown(
                    id="view-selector",
                    options=[
                        {"label": "Time-Series Plot", "value": "time"},
                        {"label": "Appliance-wise Consumption", "value": "appliance"},
                        {"label": "Electricity Forecast", "value": "forecast"},
                        {"label": "Faulty Devices", "value": "faults"}
                    ],
                    value="time",
                    clearable=False,
                    className="dropdown"
                ),

                html.Br(),

                dcc.Dropdown(
                    id="year-selector",
                    options=[{"label": str(y), "value": y} for y in years],
                    value=years[-1],  # latest year
                    clearable=False,
                    className="dropdown"
                ),

                html.Br(),

                dcc.Dropdown(
                    id="month-selector",
                    options=[{"label": m, "value": m} for m in months],
                    value=months[0],  # first month
                    clearable=False,
                    className="dropdown"
                ),

                html.Br(),

                dcc.Checklist(
                    id="appliance-selector",
                    options=[
                        {"label": "Fridge", "value": "Fridge"},
                        {"label": "AC", "value": "AC"},
                        {"label": "Other Appliances", "value": "Other Appliances"},
                        {"label": "Kitchen Appliances", "value": "Kitchen Appliances"},
                        {"label": "Washing Machine", "value": "Washing Machine"}
                    ],
                    value=["Fridge", "AC"],  # Default
                    labelStyle={"display": "block", "color": "white"},
                    style={"margin-top": "15px"}
                )
            ], width=3, className="sidebar"),

            dbc.Col([
                dcc.Loading(
                    dcc.Graph(id="main-graph", config={"displayModeBar": True}),
                    type="circle",
                    color="#19E2C5"
                )
            ], width=9, className="main-panel"),
        ])
    ], fluid=True)
