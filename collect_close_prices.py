import os
import datetime
import requests
import yfinance as yf

target_items = {
    "^KS11": "코스피 지수",
    "KRW=X": "원/달러 환율",
    "069500.KS": "KODEX 200",
    "TSLA": "테슬라(TSLA)",
    "458730.KS": "Tiger 미국배당다우존스",
    "490590.KS": "RISE 미국AI밸류체인"
}

# 한국 시간(KST) 계산
kst_tz = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(kst_tz)
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

# [수정 반영] 현재 시간에 따라 오전/오후 수집 타이틀 자동 분류
if now.hour < 12:
    run_type = "오전 7시 수집"
else:
    run_type = "저녁 5시 수집"

log_lines = [f"=== [{run_type} 시점: {current_time}] ==="]

for ticker, name in target_items.items():
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1d")
        
        if not df.empty:
            latest_close = float(df["Close"].iloc[-1])
            if ticker == "TSLA":
                price_format = f"${latest_close:,.2f}"
            elif ticker == "^KS11":
                price_format = f"{latest_close:,.2f} pt"
            elif ticker == "KRW=X":
                price_format = f"{latest_close:,.2f} 원"
            else:
                price_format = f"{int(latest_close):,} 원"
            log_lines.append(f"■ {name} ({ticker}) : {price_format}")
        else:
            log_lines.append(f"■ {name} ({ticker}) : 데이터 수집 실패")
    except Exception as e:
        log_lines.append(f"■ {name} ({ticker}) : 에러 발생 ({str(e)})")

text_to_append = "\n".join(log_lines) + "\n"

# 구글 문서(Apps Script Webhook)로 데이터 전송
webhook_url = os.environ.get("DOCS_WEBHOOK_URL")

if webhook_url:
    payload = {"text": text_to_append}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print(f"✅ 구글 문서에 {run_type} 데이터 전송 완료!")
        else:
            print(f"❌ 전송 실패: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 요청 중 에러 발생: {e}")
else:
    print("❌ 에러: 깃허브 Secrets에 DOCS_WEBHOOK_URL이 등록되지 않았습니다.")
