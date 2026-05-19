import os
import arxiv
from openai import OpenAI

def run():
    print(">>> [Task 1] 正在获取 ArXiv 论文...")
    search = arxiv.Search(
        query="all:semiconductor OR all:electronics OR all:VLSI",
        max_results=3,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "summary": result.summary[:1000],
            "link": result.entry_id
        })

    if not papers:
        return "### 📚 今日论文\n\n暂无最新相关论文。\n\n"

    api_key = os.environ.get('LLM_API_KEY')
    if not api_key:
        return "### 📚 今日论文\n\n❌ LLM API Key 未配置。\n\n"

    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    prompt = "你是半导体专家。请简要总结以下3篇最新论文，每篇格式如下：\n"
    prompt += "### [标题]\n- **核心创新**: (一句话)\n- **关键点**: (1-2点)\n- [链接](URL)\n\n"
    
    for p in papers:
        prompt += f"标题: {p['title']}\n摘要: {p['summary']}\n---\n"

    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        summary = response.choices[0].message.content
        return f"### 📚 今日前沿论文\n\n{summary}\n\n"
    except Exception as e:
        return f"### 📚 今日前沿论文\n\n❌ AI 总结失败: {str(e)}\n\n"
