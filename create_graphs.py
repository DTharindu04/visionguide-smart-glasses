import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# 1. Find the latest CSV file automatically
list_of_files = glob.glob('thesis_data_*.csv') 
if not list_of_files:
    print("Error: No data files found! Run main.py first.")
    exit()

latest_file = max(list_of_files, key=os.path.getctime)
print(f"Analyzing data from: {latest_file}")

# 2. Load Data
df = pd.read_csv(latest_file)

# Clean up column names (remove extra spaces)
df.columns = df.columns.str.strip()

# 3. GRAPH 1: System Latency (FPS Stability)
# This proves your system is fast enough for real-time use
plt.figure(figsize=(10, 5))
plt.plot(df['Time_Sec'], df['FPS'], color='green', linewidth=2)
plt.title('System Performance: FPS over Time', fontsize=14)
plt.xlabel('Time (seconds)', fontsize=12)
plt.ylabel('Frames Per Second (FPS)', fontsize=12)
plt.axhline(y=10, color='r', linestyle='--', label='Minimum Usable FPS (10)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('graph_fps_performance.png')
print("✅ Saved 'graph_fps_performance.png'")

# 4. GRAPH 2: Detection Frequency
# This shows what objects were detected most often
# We need to parse the string lists like "['Person', 'Chair']"
all_detections = []
for item in df['Detected_Objects']:
    # Clean the string to get a real list
    clean_item = item.replace("[", "").replace("]", "").replace("'", "").strip()
    if clean_item: # If not empty
        objects = [x.strip() for x in clean_item.split(",")]
        all_detections.extend(objects)

for item in df['Detected_Person']:
    clean_item = item.replace("[", "").replace("]", "").replace("'", "").strip()
    if clean_item and clean_item != "Person": # specific names
        all_detections.append("Recognized Face")

if all_detections:
    plt.figure(figsize=(8, 6))
    pd.Series(all_detections).value_counts().plot(kind='bar', color='orange')
    plt.title('Object Detection Distribution', fontsize=14)
    plt.xlabel('Object Class', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.tight_layout()
    plt.savefig('graph_object_counts.png')
    print("✅ Saved 'graph_object_counts.png'")
else:
    print("⚠️ No objects were detected, so skipping the second graph.")

print("\nAnalysis Complete. Open the PNG files to see your results!")