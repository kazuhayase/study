import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def download_actuary_textbooks():
    target_url = "https://www.actuaries.jp/examin/textbook/"
    save_dir = "actuary_textbooks"
    
    # 保存用ディレクトリの作成
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        response = requests.get(target_url)
        response.raise_for_status()
        # 文字化け防止（サイトのエンコーディングに合わせる）
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 取得対象のキーワード
        targets = ["保険１（生命保険）", "保険２（生命保険）"]
        
        # ページ内のすべてのテーブル行などを走査
        # サイト構成に基づき、対象テキストの後のリンクを探す
        current_category = None
        
        # 全ての要素から対象のセクションを特定してPDFをダウンロード
        for element in soup.find_all(['strong', 'td']):
            text = element.get_text(strip=True)
            
            # カテゴリの切り替え判定
            if any(t in text for t in targets):
                current_category = text
                print(f"\n--- {current_category} のダウンロードを開始します ---")
                continue
            
            # 他の主要カテゴリ（損保、年金など）に移ったら終了判定
            if current_category and text in ["『損保』", "『年金』", "製本された"]:
                current_category = None

            # 対象カテゴリ配下のリンクを処理
            if current_category:
                links = element.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and href.endswith('.pdf'):
                        file_url = urljoin(target_url, href)
                        file_name = f"{current_category}_{link.get_text(strip=True)}.pdf"
                        # OSで使えない文字を置換
                        file_name = file_name.replace('/', '_').replace(':', '_').replace(' ', '')
                        
                        file_path = os.path.join(save_dir, file_name)
                        
                        print(f"Downloading: {file_name}")
                        download_file(file_url, file_path)

    except Exception as e:
        print(f"エラーが発生しました: {e}")

def download_file(url, save_path):
    try:
        res = requests.get(url, stream=True)
        res.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"ファイル保存失敗: {url} - {e}")

if __name__ == "__main__":
    download_actuary_textbooks()
