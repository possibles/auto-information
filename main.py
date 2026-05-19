import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tasks import task_papers
from tasks import task_stocks
from utils.push_helper import send_to_pushdeer

def main():
    print("🚀 开始执行每日情报任务...")
    
    final_report = ""
    
    # --- 执行任务 1: 论文 ---
    try:
        paper_md = task_papers.run()
        final_report += paper_md
    except Exception as e:
        final_report += f"### 📚 论文任务出错\n\n{str(e)}\n\n"
        
    # --- 执行任务 2: 股票 ---
    try:
        stock_md = task_stocks.run()
        final_report += stock_md
    except Exception as e:
        final_report += f"### 📈 股票任务出错\n\n{str(e)}\n\n"
        
    # --- 添加页脚 ---
    footer = f"\n---\n> 🤖 由 AI 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    final_report += footer
    
    # --- 推送 ---
    title = f"📅 每日半导体情报 ({datetime.now().strftime('%m-%d')})"
    send_to_pushdeer(title, final_report)
    print("✅ 任务全部完成。")

if __name__ == "__main__":
    main()
