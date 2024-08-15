import schedule
import sys
from datetime import datetime, timedelta

# 获取当前日期和时间
now = datetime.now()

# 计算3天后的日期
three_days_later = now + timedelta(days=3)

# 格式化日期为"24年8月18日13时-15时"
formatted_date = three_days_later.strftime("%y年{}月{}日13时-15时").format(three_days_later.month, three_days_later.day)

print(formatted_date)