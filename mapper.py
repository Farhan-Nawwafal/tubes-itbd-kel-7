import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    columns = line.split(',')
    
    if len(columns) < 14 or "pickup" in columns[2]:
        continue
        
    try:
        # 1. Ambil data mentah
        pickup_dt = datetime.strptime(columns[2], "%Y-%m-%d %H:%M:%S")
        dropoff_dt = datetime.strptime(columns[3], "%Y-%m-%d %H:%M:%S")
        distance = float(columns[5])
        fare = float(columns[13])
        p_lon, p_lat = float(columns[6]), float(columns[7])
        d_lon, d_lat = float(columns[10]), float(columns[11])
        
        # 2. DATA CLEANING (Filter Outliers)
        if distance <= 0 or fare <= 0: continue
        if not (40.0 <= p_lat <= 41.5) or not (-74.5 <= p_lon <= -73.0): continue
        
        # --- INSIGHT 1: Temporal (Demand) ---
        hour = pickup_dt.strftime("%H")
        day = pickup_dt.strftime("%A")
        dtype = "Weekend" if pickup_dt.weekday() >= 5 else "Weekday"
        print(f"T_HOUR_{hour}\t1")
        print(f"T_DAY_{day}\t1")
        print(f"T_TYPE_{dtype}\t1")
        
        # --- INSIGHT 2: Spatial (Hotspots & Flow) ---
        # Grid 3 desimal (~110m) untuk mengelompokkan lokasi
        p_loc = f"{round(p_lat,3)},{round(p_lon,3)}"
        d_loc = f"{round(d_lat,3)},{round(d_lon,3)}"
        print(f"S_PICKUP_{p_loc}\t1")
        print(f"S_DROPOFF_{d_loc}\t1")
        print(f"S_FLOW_{p_loc} to {d_loc}\t1")
        
        # --- INSIGHT 3: Kinerja (Speed) ---
        duration_hr = (dropoff_dt - pickup_dt).total_seconds() / 3600
        if duration_hr > 0:
            print(f"P_SPEED_{hour}\t{distance},{duration_hr}")
            
    except:
        continue