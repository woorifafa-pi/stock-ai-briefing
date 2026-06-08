import os
import requests
import google.generativeai as genai

file_path = "정기_종목종가_모니터링.txt"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        market_data = f.read()
except FileNotFoundError:
    print("데이터 파일이 없습니다. 수집이 먼저 진행되어야 합니다.")
    exit()

# Gemini API 연동
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

prompt = f"""
당신은 전문 금융 애널리스트입니다. 아래는 누적된 주식 및 지수 데이터입니다.
이 중 **가장 마지막에 수집된 최신 데이터**를 중심으로 글로벌 경제 뉴스 흐름과 엮어서, 
오늘 아침 투자자들을 위한 인사이트가 담긴 '주식/ETF 모닝 브리핑'을 3~4줄로 핵심만 요약해서 작성해주세요. 

[누적 마감 데이터]
{market_data}
"""

response = model.generate_content(prompt)
briefing_text = response.text

# 텔레그램으로 전송
bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]
send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

payload = {
    "chat_id": chat_id,
    "text": f"🌅 [AI 모닝 주식 브리핑]\n\n{briefing_text}",
    "parse_mode": "Markdown"
}

res = requests.post(send_url, json=payload)
if res.status_code == 200:
    print("✅ 텔레그램 브리핑 전송 완료!")
else:
    print("❌ 전송 실패:", res.text)
