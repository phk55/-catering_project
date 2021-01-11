# encoding:utf-8
import datetime

def get_month_range(start_day, end_day):
    months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month

    month_range = ['%s-%s' % (start_day.year + mon // 12, mon % 12 + 1)
                   for mon in range(start_day.month - 1, start_day.month + months)]
    return month_range


if __name__ == '__main__':
    months=get_month_range(datetime.date(2015, 1, 31), datetime.datetime.now())
    print(months)