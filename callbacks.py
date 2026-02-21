from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

def register_callbacks(app, df, df2, df3, df4):

    @app.callback(
        Output("main-graph", "figure"),
        [Input("view-selector", "value"),
         Input("year-selector", "value"),
         Input("month-selector", "value"),
         Input("appliance-selector", "value")]
    )
    def update_graph(view, year, month,selected_appliances):

        # Filter datasets by year/month
        df_year = df[df.index.year == year]
        df3_year = df3[df3["Date"].str.contains(str(year))]
        df4_year = df4[df4["Date"].dt.year == year]
        df2_year = df2[df2["year"] == year]

        # 📊 Time-Series Plot
        if view == "time":
            trace = go.Scatter(
                x=df_year.index,
                y=df_year["Total_Consumption"],
                mode="lines",
                name=f"Electricity Consumption {year}",
                line_color="#19E2C5"
            )
            fig = go.Figure(data=[trace])
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis_title="Consumption (kWh)",
                xaxis_title="Date",
                title=f"Time-Series Plot of Electricity Consumption ({year})"
            )
            return fig

        # 🔮 Forecast vs Actual
        elif view == "forecast":
            df_sub = df3_year
            df_anoms = df_sub[df_sub["MAE"] >= 15]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_sub["Date"], y=df_sub["Total_Consumption"],
                mode="lines", name="Actual", line_color="#19E2C5"
            ))
            fig.add_trace(go.Scatter(
                x=df_sub["Date"], y=df_sub["Predicted_Consumption"],
                mode="lines", name="Predicted", line_color="#C6810B"
            ))
            fig.add_trace(go.Scatter(
                x=df_anoms["Date"], y=df_anoms["Total_Consumption"],
                mode="markers", name="Excess",
                marker=dict(size=7, color="#C60B0B")
            ))
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title=f"Electricity Forecast vs Actual ({year})"
            )
            return fig

        # ⚡ Faulty Devices
        elif view == "faults":
            df_sub = df4_year.copy()

            def zscore(x, window):
                r = x.rolling(window=window)
                m = r.mean().shift(1)
                s = r.std(ddof=0).shift(1)
                return (x - m) / s

    # Standardized anomaly columns
            df_sub["fridge_zscore"] = zscore(df_sub["Fridge"], 30)
            df_sub["ac_zscore"] = zscore(df_sub["AC"], 30)
            df_sub["other_appliances_zscore"] = zscore(df_sub["Other Appliances"], 30)
            df_sub["kitchen_appliances_zscore"] = zscore(df_sub["Kitchen Appliances"], 30)
            df_sub["washing_machine_zscore"] = zscore(df_sub["Washing Machine"], 3)

            df_sub.replace([np.inf, -np.inf], np.nan, inplace=True)
            df_sub.fillna(0, inplace=True)

            colors = {
                            "Fridge": "#19E2C5",
                            "AC": "#FF8C00",
                            "Other Appliances": "#FFD700",
                            "Kitchen Appliances": "#ADFF2F",
                            "Washing Machine": "#1E90FF"
                        }

            fig = go.Figure()
            for appliance in selected_appliances: 
                fig.add_trace(go.Scatter(
                    x=df_sub["Date"], y=df_sub[appliance],
                    mode="lines", name=f"{appliance} Consumption",
                    line_color=colors.get(appliance, "#19E2C5")
                ))

        # Anomalies
                col_name = f"{appliance.lower().replace(' ', '_')}_zscore"
                anomalies = df_sub[df_sub[col_name] > 5]

                fig.add_trace(go.Scatter(
                x=anomalies["Date"], y=anomalies[appliance],
                mode="markers", name=f"{appliance} Anomalies",
                marker=dict(size=8, color="red")
                ))

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title=f"Faulty Devices - Anomaly Detection ({year})"
            )
            return fig


        # 🍕 Appliance-wise
        elif view == "appliance":
            df_sub = df2_year[df2_year["month"] == month]
            if df_sub.empty:
                return go.Figure()

            row = df_sub.iloc[0]
            values = [
                row["Fridge"],
                row["Kitchen Appliances"],
                row["AC"],
                row["Washing Machine"],
                row["Other Appliances"]
            ]
            fig = go.Figure(data=[go.Pie(
                labels=["Fridge", "Kitchen Appliances", "AC", "Washing Machine", "Other Appliances"],
                values=values, hole=0.3
            )])
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title=f"Appliance-wise Consumption ({month} {year})"
            )
            return fig

        return go.Figure()
