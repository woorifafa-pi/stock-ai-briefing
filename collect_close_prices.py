import datetime
import FinanceDataReader as fdr

target_items = {
    "KS11": "코스피 지수",
    "USD/KRW": "원/달러 환율",
    "069500": "KODEX 200",
    "TSLA": "테슬라(TSLA)",
    "458730": "Tiger 미국배당다우존스",
    "490590": "RISE 미국AI밸류체인"
}

now = datetime.datetime.now()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")
log_lines = [f"=== [데이터 수집 시점: {current_time}] ==="]

for ticker, name in target_items.items():
    try:
        df = fdr.DataReader(ticker)
        if not df.empty:
            latest_close = df.iloc[-1]["Close"]
            if ticker == "TSLA":
                price_format = f"${latest_close:,.2f}"
            elif ticker == "KS11":
                price_format = f"{latest_close:,.2f} pt"
            elif ticker == "USD/KRW":
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

print(f"✅ 파일 업데이트 완료: {file_name}")
