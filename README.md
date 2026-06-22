本專案基於 Raspberry Pi 5，整合 DHT11 溫濕度感測器與 I2C 1602 LCD 顯示器，實作一套簡易的環境監測與即時通知系統。系統可即時讀取溫濕度資料，並在數值異常時透過 LINE Messaging API 發送通知。

---

## Features

* 即時讀取溫度與濕度資料
* LCD 顯示環境資訊
* 異常時透過 LINE 發送通知
* 基本錯誤處理（避免感測器讀取失敗導致程式中斷）
* 簡單冷卻機制避免重複通知

---

## Hardware Setup

* Raspberry Pi 5
* DHT11 Temperature & Humidity Sensor (GPIO 4)
* I2C 1602 LCD (SDA: GPIO 2, SCL: GPIO 3)
* LED (GPIO 17)
* Button (GPIO 27)

---

## Requirements

請先建立虛擬環境並安裝以下套件：

```bash
pip install adafruit-circuitpython-dht
pip install RPLCD
pip install requests
```

---

## How to Run

1. 啟用 I2C

```bash
sudo raspi-config
```

2. 執行程式

```bash
python main.py
```

---

## Notes

* DHT11 可能偶爾讀取失敗，程式會使用前一次資料避免中斷
* LINE 通知設有間隔時間，避免重複推播
* LCD 顯示為簡化版資訊呈現
