# dates.py

from datetime import datetime, date, timedelta, timezone

# 1️⃣ Current Date & Time
print("---- Example 1: Current DateTime ----")
now = datetime.now()
print(now)

# 2️⃣ Create specific date
print("\n---- Example 2: Create Date ----")
d = date(2026, 3, 11)
print(d)

# 3️⃣ Formatting Date
print("\n---- Example 3: Formatting ----")
formatted = now.strftime("%d.%m.%Y %H:%M")
print(formatted)

# 4️⃣ Parsing String to Date
print("\n---- Example 4: Parsing ----")
date_string = "2026-03-11"
parsed = datetime.strptime(date_string, "%Y-%m-%d")
print(parsed)

# 5️⃣ Time Difference
print("\n---- Example 5: Date Difference ----")
d1 = date(2026, 1, 1)
d2 = date(2026, 1, 10)
difference = d2 - d1
print("Days:", difference.days)

# 6️⃣ timedelta
print("\n---- Example 6: timedelta ----")
future = now + timedelta(days=7)
print(future)

# 7️⃣ Timezone UTC
print("\n---- Example 7: Timezone ----")
utc_time = datetime.now(timezone.utc)
print(utc_time)