from logging import getLogger
import inspect

### https://github.com/pistatium/about_python_logging
import json
from logging.config import dictConfig

# 設定ファイルから読み込む
with open('logging.json') as f:
    dictConfig(json.load(f))

logger = getLogger('app')
    
def varlog(name):
    # 変数が定義されているスコープを取得
    frame = inspect.currentframe().f_back
    variable_value = frame.f_globals.get(name) or frame.f_locals.get(name)
    
    if variable_value is not None:
        logger.info(f'{name}={variable_value}')
    else:
        logger.warning(f'{name} is not defined')
