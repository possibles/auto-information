import os
import yfinance as yf
import pandas as pd
from openai import OpenAI
from datetime import datetime, timedelta

def run():
    print(">>> [Task 2] 正在获取股票行情...")
    tickers = ["NVDA", "AMD", "TSM", "INTC", "QCOM", "ASML"]
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)
    
    try:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False, group_by='ticker')
    except Exception as e:
        return f"### 📈 半导体股市概览\n\n❌ 获取股票数据失败: {str(e)}\n\n"

    stock_info_list = []
    for ticker in tickers:
        try:
            # 处理 yfinance 返回的数据结构
            if isinstance(data.columns, pd.MultiIndex):
                df = data[ticker]
            else:
                df = data
            
            if df.empty or len(df) < 2:
                continue
                
            last_row = df.iloc[-1]
            prev_row = df.iloc[-2]
            
            close = last_row['Close']
            prev_close = prev_row['Close']
            
            # 避免除以零
            if prev_close == 0:
                change_pct = 0
            else:
                change_pct = ((close - prev_close) / prev_close) * 100
            
            stock_info_list.append({
                "symbol": ticker,
                "price": round(close, 2),
                "change": round(change_pct, 2)
            })
        except Exception:
            continue

    if not stock_info_list:
        return "### 📈 半导体股市概览\n\n暂无数据。\n\n"

    api_key = os.environ.get('LLM_API_KEY')
    if not api_key:
         # 如果没Key，至少返回原始数据
         stocks_str = "\n".join([f"- {s['symbol']}: ${s['price']} ({'+' if s['change']>0 else ''}{s['change']}%)" for s in stock_info_list])
         return f"### 📈 半导体股市概览\n\n{stocks_str}\n\n"

    client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    
    stocks_str = "\n".join([f"- {s['symbol']}: ${s['price']} ({'+' if s['change']>0 else ''}{s['change']}%)" for s in stock_info_list])
    
    prompt = f"你是金融分析师。以下是主要半导体公司最新股价变动：\n{stocks_str}\n\n"
    prompt += "请用中文简要总结市场情绪，按点列出：\n1. 整体趋势\n2. 表现最好和最差的公司\n格式要求：Markdown 列表。"

    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        summary = response.choices[0].message.content
        return f"### 📈 半导体股市概览\n\n{summary}\n\n"
    except Exception as e:
        return f"### 📈 半导体股市概览\n\n{stocks_str}\n\n❌ AI 分析失败: {str(e)}\n\n"
