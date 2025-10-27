"""
报告生成模块
"""
import os
from datetime import datetime
from typing import List, Dict


OUTPUT_DIR = './aaa'

"""确保输出目录存在"""
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


report_time = datetime.now()
timestamp = report_time.strftime("%Y%m%d_%H%M%S")
filename = f"scan1_rep11or111t_{timestamp}.txt"
filepath = os.path.join(OUTPUT_DIR, filename)

with open(filepath, 'w', encoding='utf-8') as f:
    # 写入报告头
    f.write("╔" + "═" * 78 + "╗\n")
    f.write("║" + " " * 78 + "║\n")
    f.write("║" + "          🔒 InCloud GitHub 云上扫描器 - AI API Key 扫描报告".ljust(78) + "║\n")
    f.write("║" + " " * 78 + "║\n")
    f.write("╚" + "═" * 78 + "╝\n\n")
