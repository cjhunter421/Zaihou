import datetime
import urllib.request
import calendar


def google_pull(symbol, exchange=''):
    interval = 86400
    symbol = symbol.upper()
    if exchange:
        exchange = '&x=' + exchange.upper()
    url = 'https://www.google.com/finance/getprices?'
    url += 'q={0}{1}&i={2}&p={3}&f=d,c'.format(symbol, exchange, str(interval), "50Y")
    csv = urllib.request.urlopen(url).readlines()
    results = []
    for line in csv:
        line = line.decode('utf-8').strip()
        if line.count(',') != 1 or '=' in line:
            continue
        offset, value = line.split(',')
        if offset[0] == 'a':
            day = float(offset[1:])
            offset = 0
        else:
            offset = float(offset)
        interval = float(interval)
        time_ = datetime.datetime.fromtimestamp(day+(interval*offset))
        results.append((time_, value))
    return results

def parse_monthly(stock_data, start_month, start_year, end_month, end_year,
                  test_length):
    time = []
    data = []
    time_index = []
    prev_value = None
    prev_month = None
    for time_, value in stock_data:
        year = time_.year
        month = time_.month
        day_ = time_.day
        if calendar.monthrange(year, month)[-1] == day_:
            time.append(time_)
            data.append(float(value))
            time_index.append((month, year))
        elif time and (prev_month != month and prev_value[0] != time[-1]):
            time.append(prev_value[0])
            data.append(prev_value[1])
            time_index.append((prev_value[0].month, prev_value[0].year))
        prev_month = month
        prev_value = (time_, float(value))
    start_index = time_index.index((start_month, start_year))
    end_index = time_index.index((end_month, end_year))
    test_data = []
    try:
        for i in range(end_index+1,end_index+1+test_length):
            test_data.append(((time[i].year, time[i].month, time[i].day), data[i]))
    except Exception as e:
        pass
    return (data[start_index:end_index+1], test_data)
