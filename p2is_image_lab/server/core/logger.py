import logging
import os
from datetime import datetime

# Initialize logging directory relative to server root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Define log file name with current date
log_file = os.path.join(LOG_DIR, f"p2is_audio_{datetime.now().strftime('%Y%m%d')}.log")

# Setup logger
logger = logging.getLogger("P2IS_Audio_Lab")
logger.setLevel(logging.DEBUG)

# Avoid duplicate handlers if module is reloaded
if not logger.handlers:
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)

def get_logger():
    return logger
