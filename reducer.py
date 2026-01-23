import sys

data = {}

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    key, val = line.split('\t', 1)
    
    if key not in data:
        if key.startswith("P_SPEED"):
            data[key] = {'dist': 0.0, 'time': 0.0}
        else:
            data[key] = 0

    if key.startswith("P_SPEED"):
        d, t = val.split(',')
        data[key]['dist'] += float(d)
        data[key]['time'] += float(t)
    else:
        data[key] += int(val)

# Output menggunakan pemisah ";" agar tidak bentrok dengan koma koordinat
for k, v in data.items():
    if k.startswith("P_SPEED"):
        speed = v['dist'] / v['time'] if v['time'] > 0 else 0
        print(f"{k};{speed}")
    else:
        print(f"{k};{v}")