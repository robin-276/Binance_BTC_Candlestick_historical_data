

import os
import requests
import zipfile
from io import BytesIO

# ==========================
# CONFIG
# ==========================
symbol = "BTCUSDT"
timeframes = ["1m", "3m", "5m", "15m", "30m",
              "1h", "2h", "4h", "6h", "8h", "12h",
              "1d", "1w", "1M"]

start_year, start_month = 2020, 1
end_year, end_month = 2025, 8   # Until Aug 2025

base_url = "https://data.binance.vision/data/futures/um/monthly/klines"

# ==========================
# DOWNLOAD LOCATION
# ==========================
# 🔽 Paste your folder path here (e.g. r"C:\Users\joser\Downloads\binance_data_2")
download_location = r" your download locatio from you pc , copy and paste here  "

save_root = os.path.abspath(download_location)
os.makedirs(save_root, exist_ok=True)


# ==========================
# HELPER FUNCTION
# ==========================
def download_and_extract(url, save_folder):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with zipfile.ZipFile(BytesIO(r.content)) as z:
                for file_name in z.namelist():
                    if file_name.endswith(".csv"):
                        save_path = os.path.join(save_folder, os.path.basename(file_name))
                        with z.open(file_name) as src, open(save_path, "wb") as dst:
                            dst.write(src.read())
                        print(f"✅ Saved: {save_path}")
        else:
            print(f"❌ Not available: {url}")
    except Exception as e:
        print(f"⚠️ Error downloading {url}: {e}")


# ==========================
# MAIN LOOP
# ==========================
for interval in timeframes:
    folder = os.path.join(save_root, interval)
    os.makedirs(folder, exist_ok=True)

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if (year == end_year and month > end_month):
                break

            month_str = f"{month:02d}"
            filename = f"{symbol}-{interval}-{year}-{month_str}.zip"

            url = f"{base_url}/{symbol}/{interval}/{filename}"

            print(f"⬇️ Downloading {filename} ...")
            download_and_extract(url, folder)

print("\n🎉 All downloads completed! Files saved in:", save_root)
