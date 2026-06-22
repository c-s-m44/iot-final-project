import time
import board
import adafruit_dht
from RPLCD.i2c import CharLCD

print("Hardware test started...")

# 初始化
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2)
lcd.clear()

dht_device = adafruit_dht.DHT11(board.D4)

try:
    while True:
        try:
            temp = dht_device.temperature
            humi = dht_device.humidity

            if temp is not None and humi is not None:
                print(f"Temp: {temp}C, Humi: {humi}%")

                lcd.cursor_pos = (0, 0)
                lcd.write_string(f"T:{temp:.1f}C".ljust(16))

                lcd.cursor_pos = (1, 0)
                lcd.write_string(f"H:{humi:.1f}%".ljust(16))

        except RuntimeError:
            print("Sensor read failed, retrying...")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(2)

except KeyboardInterrupt:
    print("Test stopped")
    lcd.clear()
    dht_device.exit()
