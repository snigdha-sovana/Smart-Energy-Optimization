# Electra.AI – Smart Electricity Consumption Dashboard

Electra.AI is an interactive electricity monitoring and forecasting dashboard built using Dash and Plotly.  
It provides insights into total electricity consumption, appliance-wise usage, anomaly detection, and forecasting visualization.

---

## Features

### 1. Time-Series Visualization
- Displays total electricity consumption over time
- Interactive Plotly graph
- Dark-themed dashboard UI

### 2. Appliance-wise Consumption Analysis
- Monthly consumption distribution for:
  - Fridge
  - Kitchen Appliances
  - AC
  - Washing Machine
  - Other Appliances
- Interactive pie chart with month selection

### 3. Electricity Consumption Forecast
- Compares:
  - Actual Consumption
  - Predicted Consumption
- Highlights excess consumption (high MAE values)
- Helps identify unusual usage patterns

### 4. Faulty Device Detection
- Uses rolling Z-score anomaly detection
- Detects abnormal fluctuations in:
  - Fridge
  - AC
  - Kitchen Appliances
  - Washing Machine
  - Other Appliances
- Interactive device selector

---

## Tech Stack

- Python
- Dash
- Plotly
- Pandas
- NumPy

---
