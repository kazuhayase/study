import tqdm
import logging
import logging.config

import os

# 環境変数の読み込み
GMAIL_USER = os.getenv("GMAIL_USER")
BLOGGER_PASSWORD = os.getenv("BLOGGER_PASSWORD")

print(f"GMAIL_USER: {GMAIL_USER}")
print(f"BLOGGER_PASSWORD: {BLOGGER_PASSWORD}")


import time
from selenium import webdriver
#from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36")
#options.add_argument("--headless")  # ヘッドレスモードを有効にする場合
options.add_argument("--disable-blink-features=AutomationControlled")

# ブラウザの起動
driver = webdriver.Chrome(options=options)
driver.delete_all_cookies()
driver.refresh()

driver.get("https://accounts.google.com/signin")

#time.sleep(3)  # ロード待ち

# メールアドレスの入力
email_input = driver.find_element(By.NAME, "identifier")
email_input.send_keys(GMAIL_USER)
email_input.send_keys(Keys.RETURN)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 3)
try:
    # 「別の方法を試す」をクリック
    alternate_method_button = wait.until(
        # EC.element_to_be_clickable((By.XPATH, "//div[text()='別の方法を試す']"))
        EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'別の方法')]"))
    )
    driver.execute_script("arguments[0].click();", alternate_method_button)
    #alternate_method_button.click()
except Exception as e:
    print(f"「別の方法を試す」ボタンが見つかりません: {e}")

#time.sleep(10)  # ロード待ち
print(f"「別の方法を試す」ボタンをクリックしました")

wait = WebDriverWait(driver, 3)
try:
    # パスワードログインを選択
    password_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='パスワードを入力']"))
        #EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'パスワード')]"))
    )
    password_option.click()
    #driver.execute_script("arguments[0].click();", password_option)
except Exception as e:
    print(f"[パスワード]ボタンが見つかりません: {e}")
    exit(1)

print(f"「パスワードを入力」ボタンをクリックしました")

wait = WebDriverWait(driver, 10)
try:
    # 「パスワードを表示する」ボタンを探す
    show_password_checkbox = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'パスワードを表示する')]"))
    )
    # クリックしてパスワードを表示
    show_password_checkbox.click()
    
    # パスワードの入力
    password_input = wait.until(
        EC.presence_of_element_located((By.NAME, "Passwd"))
        )
    password_input.click() 
    password_input.send_keys(BLOGGER_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    #driver.execute_script("arguments[0].value = arguments[1];", password_input, BLOGGER_PASSWORD)
except Exception as e:
    print(f"[パスワード] が見つかりません: {e}")
    exit(1)

#time.sleep(5)  # 完了を待つ

import pyaudio
import wave

# 録音の設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
# RATE = 48000
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
OUTPUT_FILENAME = "output.wav"

# 録音の開始
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=16)  # ここでデバイスインデックスを指定
print("Recording...")

frames = []

import argparse

parser = argparse.ArgumentParser(description="コマンドライン引数のテスト")
parser.add_argument("url", type=str, help="URLを指定")
#parser.add_argument("--age", type=int, help="年齢を指定（オプション）")

args = parser.parse_args()

print(f"URL: {args.url}")
#if args.age:
#    print(f"年齢: {args.age}")

# Seleniumでブラウザを自動化
driver = webdriver.Chrome()
driver.get(args.url)  # ここにURLを入力してください

# play2関数を呼び出す
play_button = driver.find_element(By.ID, "play2")  # ここに適切なセレクタを入力してください
play_button.click()

# 録音を開始
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# 録音の終了
stream.stop_stream()
stream.close()
audio.terminate()

# 録音ファイルの保存
wf = wave.open(OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# ブラウザを閉じる
driver.quit()
