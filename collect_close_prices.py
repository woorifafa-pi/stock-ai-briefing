import datetime
import yfinance as yf

# 1. 야후 파이낸스 티커(Ticker)로 변경
target_items = {
    "^KS11": "코스피 지수",
    "KRW=X": "원/달러 환율",
    "069500.KS": "KODEX 200",
    "TSLA": "테슬라(TSLA)",
    "458730.KS": "Tiger 미국배당다우존스",
    "490590.KS": "RISE 미국AI밸류체인"
}

kst_tz = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(kst_tz)
current_time = now.strftime("%Y-%m-%d %H:%M:%S")
log_lines = [f"=== [데이터 수집 시점: {current_time}] ==="]

# 2. 데이터 수집 로직 (yfinance 적용)
for ticker, name in target_items.items():
    try:
        stock = yf.Ticker(ticker)
        # 오늘 하루치 최신 데이터만 빠르고 정확하게 가져오기
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

text_to_append = "\n".join(log_lines) + "\n\n"
file_name = "정기_종목종가_모니터링.txt"

with open(file_name, "a", encoding="utf-8") as f:
    f.write(text_to_append)

print(f"✅ 야후 파이낸스 기반 파일 업데이트 완료: {file_name}")
