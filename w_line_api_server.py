import logging
from waitress import serve
from line_api_server import app


# 設定 logging（寫入檔案並同時輸出到 console）
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("line_api_server.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

serve(app, host='0.0.0.0', port=5000)