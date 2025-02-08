import logging
import os
from logger_config import setup_logging

# スクリプト名を取得
script_name = os.path.splitext(os.path.basename(__file__))[0]

# ロギング設定を適用
setup_logging(script_name)

logger = logging.getLogger(__name__)
logger.info("This is a general log message.")
logger.info("This message contains specific_data and will be logged to a separate file.")
logger.info("This message contains Text and will be logged to a separate file.")
logger.info("This message contains Table and will be logged to a separate file.")
logger.info("This message contains [Exception] and will be logged to a separate file.")
logger.info("This message contains Tabs and will be logged to a separate file.")
