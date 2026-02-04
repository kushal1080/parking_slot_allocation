import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from parking_system.database.db import get_conn
from datetime import datetime, timedelta
import numpy as np

def get_vehicle_logs():
    """Fetch vehicle logs with checkin and checkout times and slot info."""
    with get_conn() as conn:
        df = pd.read_sql_query("""
            SELECT v.license_plate, v.vehicle_type, v.slot_id,
                   s.slot_type, s.level,
                   vl.checkin_time, vl.checkout_time, vl.amount
            FROM vehicles v
            LEFT JOIN vehicle_logs vl ON v.license_plate = vl.license_plate
            LEFT JOIN slots s ON v.slot_id = s.id
        """, conn)
    if not df.empty:
        df['checkin_time'] = pd.to_datetime(df['checkin_time'])
        df['checkout_time'] = pd.to_datetime(df['checkout_time'])
    return df

def predict_slot_demand(excel_path="slot_demand.xlsx"):
    """
    Predict next 24-hour slot demand using linear regression.
    Saves Excel with:
        - historical hourly check-ins
        - predicted hourly demand
        - chart
    """
    df = get_vehicle_logs()
    if df.empty:
        print("No logs to predict.")
        return None

    # Extract hour of check-in
    df['hour'] = df['checkin_time'].dt.hour
    hourly_counts = df.groupby('hour').size().reset_index(name='count')

    # Fit linear regression
    X = hourly_counts[['hour']]
    y = hourly_counts['count']
    model = LinearRegression()
    model.fit(X, y)
    hourly_counts['predicted'] = model.predict(X)

    # Predict next 24 hours
    next_24 = pd.DataFrame({'hour': np.arange(0, 24)})
    next_24['predicted'] = model.predict(next_24[['hour']])
    next_24['predicted'] = next_24['predicted'].clip(lower=0)  # no negative predictions

    # Save to Excel with chart
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        hourly_counts.to_excel(writer, sheet_name='HistoricalCheckins', index=False)
        next_24.to_excel(writer, sheet_name='Next24hPrediction', index=False)

    # Plot chart
    plt.figure(figsize=(10, 5))
    plt.plot(hourly_counts['hour'], hourly_counts['count'], label='Historical', marker='o')
    plt.plot(hourly_counts['hour'], hourly_counts['predicted'], label='Fitted', linestyle='--')
    plt.plot(next_24['hour'], next_24['predicted'], label='Next 24h Prediction', linestyle=':', marker='x')
    plt.xlabel('Hour')
    plt.ylabel('Check-ins')
    plt.title('Parking Slot Check-in Prediction')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('slot_demand_chart.png')
    plt.close()

    print("\n=== Predicted Slot Demand ===")
    print(next_24)
    print(f"\nPrediction Excel and chart saved: {excel_path}, slot_demand_chart.png")
    return next_24
