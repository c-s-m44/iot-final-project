import time
import board
import adafruit_dht
import requests
import os
from RPLCD.i2c import CharLCD

# =========================

# LINE 設定（請使用環境變數）

# =========================

LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# =========================

# 警報參數設定

# =========================

ALERT_TEMP_THRESHOLD = 25.0   # 溫度警報門檻
ALERT_HUMI_THRESHOLD = 50.0   # 濕度警報門檻
ALERT_COOLDOWN = 60           # 冷卻時間（秒）

last_alert_time = 0  # 上一次發送警報時間

print("System started. Reading sensor data...")

# =========================

# 初始化硬體

# =========================

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2)
lcd.clear()

dht_device = adafruit_dht.DHT11(board.D4)  # DHT11 接在 GPIO 4

# 預設值（避免第一次讀取失敗）

current_temp = 25.0
current_humi = 50.0

# =========================

# LINE 通知函式

# =========================

def send_line_alert():
global last_alert_time

```
if not LINE_ACCESS_TOKEN or not LINE_USER_ID:
    print("[LINE] Token or User ID not set.")
    return

current_time = time.time()

# 冷卻機制（避免短時間內重複發送）
if current_time - last_alert_time < ALERT_COOLDOWN:
    print("[LINE] Alert skipped (cooldown)")
    return

url = "https://api.line.me/v2/bot/message/push"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
}

message = (
    f"【環境異常警報】\n"
    f"溫度：{current_temp:.1f}°C\n"
    f"濕度：{current_humi:.1f}%"
)

payload = {
    "to": LINE_USER_ID,
    "messages": [
        {
            "type": "text",
            "text": message
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("[LINE] Alert sent")
        last_alert_time = current_time
    else:
        print(f"[LINE Error] {response.text}")
except Exception as e:
    print(f"[LINE Error] Network issue: {e}")
```

# =========================

# 主程式

# =========================

try:
while True:
# 讀取感測器資料
try:
temp_read = dht_device.temperature
humi_read = dht_device.humidity

```
        if temp_read is not None and humi_read is not None:
            current_temp = temp_read
            current_humi = humi_read

            print(f"[Sensor] Temp: {current_temp}C, Humi: {current_humi}%")

            # 溫度警報
            if current_temp >= ALERT_TEMP_THRESHOLD:
                send_line_alert()

            # 濕度警報
            if current_humi >= ALERT_HUMI_THRESHOLD:
                send_line_alert()

    except RuntimeError:
        # DHT11 偶爾讀取失敗時使用前一次資料
        print("[Sensor] Read failed, using previous value")
    except Exception as e:
        print(f"[Sensor Error] {e}")

    # LCD 顯示溫度
    lcd.cursor_pos = (0, 0)
    lcd.write_string(f"T:{current_temp:.1f}C".ljust(8))
    time.sleep(2)

    # LCD 顯示濕度
    lcd.cursor_pos = (0, 0)
    lcd.write_string(f"H:{current_humi:.1f}%".ljust(8))
    time.sleep(2)
```

except KeyboardInterrupt:
print("\nProgram stopped by user")
lcd.clear()
dht_device.exit()

except Exception as e:
print(f"[Error] {e}")
