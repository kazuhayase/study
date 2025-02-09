import logging.config
import os
import json

def setup_logging(script_name, default_path='./conf/logging.json'):
    # スクリプト名からログファイル名を設定
    log_filename = f"./log/{script_name}.log"
    os.environ["log_filename"] = log_filename

    # ログ設定ファイルを読み込む
    with open(default_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # ファイルハンドラを追加
    file_handler = {
        "class": "logging.FileHandler",
        "level": "DEBUG",
        "formatter": "simple",
        "filename": log_filename
    }
    config['handlers'][script_name] = file_handler
    config['loggers']['']['handlers'].append(script_name)

    # ログ設定を適用
    logging.config.dictConfig(config)
