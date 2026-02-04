import pandas as pd
import matplotlib.pyplot as plt
from parking_system.database.db import get_conn

def get_vehicle_logs():
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
        df['duration_minutes'] = (df['checkout_time'] - df['checkin_time']).dt.total_seconds() / 60
    return df

def generate_enhanced_report(file_path="phase3_report.xlsx"):
    df = get_vehicle_logs()
    if df.empty:
        print("No data to generate report.")
        return None

    # Revenue per slot type
    revenue_by_slot = df.groupby('slot_type')['amount'].sum()
    total_revenue = df['amount'].sum()
    total_vehicles = df['license_plate'].nunique()

    # Hourly check-ins
    df['checkin_hour'] = df['checkin_time'].dt.hour
    hourly_checkins = df.groupby('checkin_hour').size()

    # Save Excel with multiple sheets
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        pd.DataFrame({'total_vehicles': [total_vehicles], 'total_revenue': [total_revenue]}).to_excel(writer, sheet_name='Summary', index=False)
        revenue_by_slot.to_frame(name='Revenue').to_excel(writer, sheet_name='Revenue')
        hourly_checkins.to_frame(name='Check-ins').to_excel(writer, sheet_name='HourlyCheckins')

    # Generate chart for hourly check-ins
    plt.figure(figsize=(10, 5))
    hourly_checkins.plot(kind='bar', color='skyblue')
    plt.title('Hourly Check-ins')
    plt.xlabel('Hour')
    plt.ylabel('Number of Check-ins')
    plt.tight_layout()
    plt.savefig('hourly_checkins_chart.png')
    plt.close()

    print("\nGenerating enhanced parking reports...")
    print(f"Total Revenue: {total_revenue}, Total Vehicles: {total_vehicles}")
    print("Revenue per slot type:\n", revenue_by_slot)
    print("Hourly check-ins:\n", hourly_checkins)
    print(f"Report Excel and chart saved: {file_path}, hourly_checkins_chart.png")
    return df

# Alias for backward compatibility
export_reports = generate_enhanced_report
