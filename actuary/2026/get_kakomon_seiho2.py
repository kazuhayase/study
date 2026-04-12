import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import time

def download_seibo2_custom_naming():
    target_url = "https://www.actuaries.jp/lib/collection/"
    save_dir = "actuary_past_exams_seibo2"
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 命名規則の正規表現パターン
    # 1. 平成元年〜11年: H*seiho2.pdf (例: H10seiho2.pdf)
    # 2. 平成12年〜29年: HyyH.pdf (例: H20H.pdf)
    # 3. 2018年以降: YYYYH.pdf (例: 2019H.pdf)
    patterns = [
        r'H\d{1,2}seiho2\.pdf$',
        r'H\d{2}H\.pdf$',
        r'20\d{2}H\.pdf$'
    ]

    try:
        response = requests.get(target_url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.find_all('a')
        print(f"--- 指定の命名規則に基づき生保2のダウンロードを開始します ---")

        for link in links:
            href = link.get('href')
            if not href or not href.endswith('.pdf'):
                continue
            
            # ファイル名部分のみを抽出
            filename_in_url = href.split('/')[-1]
            
            # 昭和（Sxx）が含まれる場合はスキップ
            if filename_in_url.startswith('S'):
                continue

            # いずれかのパターンに合致するかチェック
            is_target = any(re.search(p, filename_in_url) for p in patterns)
            
            if is_target:
                file_url = urljoin(target_url, href)
                # 保存用ファイル名はURLのファイル名を活かす
                save_path = os.path.join(save_dir, filename_in_url)
                
                if os.path.exists(save_path):
                    print(f"スキップ (既存): {filename_in_url}")
                    continue

                print(f"ダウンロード中: {filename_in_url}")
                if download_file(file_url, save_path):
                    time.sleep(1) # サーバー負荷軽減

        print("\n指定されたすべてのファイルの確認が完了しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

def download_file(url, save_path):
    try:
        res = requests.get(url, stream=True, timeout=15)
        res.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"失敗: {url} - {e}")
        return False

if __name__ == "__main__":
    download_seibo2_custom_naming()
