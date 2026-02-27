import re
import json

def normalize_money(s):
    s = s.replace(" ", "").replace(",", ".")
    return float(s)

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 1️⃣ Все цены
money_pattern = r"\d{1,3}(?: \d{3})*,\d{2}"
prices = re.findall(money_pattern, text)
prices_float = [normalize_money(p) for p in prices]

# 2️⃣ Дата и время
datetime_pattern = r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})"
dt_match = re.search(datetime_pattern, text)

date = dt_match.group(1) if dt_match else None
time = dt_match.group(2) if dt_match else None

# 3️⃣ Метод оплаты
if "Банковская карта" in text:
    payment_method = "CARD"
elif "Нал" in text:
    payment_method = "CASH"
else:
    payment_method = None

# 4️⃣ ИТОГО
total_pattern = r"ИТОГО:\s*\n?(\d{1,3}(?: \d{3})*,\d{2})"
total_match = re.search(total_pattern, text)
total = normalize_money(total_match.group(1)) if total_match else None

# 5️⃣ Вывод JSON
result = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "total": total,
    "all_prices": prices_float
}

print(json.dumps(result, ensure_ascii=False, indent=2))