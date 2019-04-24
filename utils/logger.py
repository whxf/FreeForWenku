# -*- coding:utf-8 -*-
import sys

sys.path.append('../')  # 新加入的

import logging
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(level=logging.DEBUG)

log_path = os.path.join('log', 'error.log')
file_handler = logging.FileHandler(log_path, mode='a', encoding='utf=8')
file_handler.setFormatter(formatter)
file_handler.setLevel(level=logging.ERROR)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

print(os.getcwd())