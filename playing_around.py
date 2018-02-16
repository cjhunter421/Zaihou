import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import urllib
import calendar
import matplotlib.pyplot as plt

import numpy

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def download_data(symbol, start_month, start_year, end_month, end_year, test_length, exchange=''):
    interval = 86400
    symbol = symbol.upper()
    if exchange:
        exchange = '&x=' + exchange.upper()
    url = 'https://www.google.com/finance/getprices?'
    url += 'q={0}{1}&i={2}&p={3}&f=d,c'.format(symbol, exchange, str(interval), "50Y")
    csv = urllib.request.urlopen(url).readlines()
    time = []
    data = []
    time_index = []
    prev_value = None
    prev_month = None
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
        year = time_.year
        month = time_.month
        day_ = time_.day
        if calendar.monthrange(year, month)[-1] == day_:
            #print(year, month, day_, float(value))
            time.append(time_)
            data.append(float(value))
            time_index.append((month, year))
        elif time and (prev_month != month and prev_value[0] != time[-1]):
            #print(prev_value[0].year, prev_value[0].month, prev_value[0].day, prev_value[1])
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
            test_data.append(((time[i].month, time[i].day, time[i].year),
                              data[i]))
    except Exception:
        pass
    return (data[start_index:end_index+1], test_data)

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '14JTVEZNYwl1nO1Xj6u2EizRSa9ChNKC6CJP4rzeqopg'
    rangeName = 'Dan_Fooling_Around!C2:D26'

    values = [
        [
            "1","2"
        ],
        [
            "2","3"
        ],
        [
            "=A2+A3","=B2+B3"
        ]
    ]
    data = [
        {
            'range': 'Dan_Fooling_Around!AJ2:AK4',
            'values': values
        },
    ]
    body = {
      'valueInputOption': 'USER_ENTERED',
      'data': data
    }

    result = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheetId, body=body).execute()

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[1]))

def num_rows_to_letters(x):
    letter = ""
    first = ord("A")
    f_i = (x-1) // 26
    s_i = (x-1) % 26
    if f_i > 0:
        letter += chr(first + f_i - 1)
    letter += chr(first + s_i)
    return letter

def main2():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '14JTVEZNYwl1nO1Xj6u2EizRSa9ChNKC6CJP4rzeqopg'

    cov_values = []
    avg_rets = []
    test_returns = []

    """ companies = ["UNH", "ANIK", "NXPI", "MSFT", "ATVI", "NFLX", "AMZN",   "GOOG","AAPL", "FB", "IDCC", "SUPN", "AGX", "SIMO", "MPH",
         "MASI", "NTES", "THO", "CMCSA", "CM", "KINS", "MLVF",
                 "FIZZ", "PF", "TSLA", "MG", "BWXT", "KBAL", "FIVE"]
    """

    companies = ["VOO", "YY", "SIMO", "AMAT", "RENX", "DY", "DQ", "BA", "HA", "UNH", "SUPN", "FONR", "GILD", "NLY", "CM", "EVR", "K", "PAHC", "PETS", "FIZZ", "SGRY", "FOXF", "ULTA", "BBY", "LOPE", "SBGI", "FL", "ITRN", "HOFT", "BABA", "AAPL", "FB", "AMZN", "PAYC", "DAN", "BWXT", "AGX", "NTES", "SWK", "JPM", "NTRI", "THO", "NVR", "KHC", "WD"]

    for company in companies:
        print(company)
        data, test_data = download_data(company, 4, 2016, 4, 2017, 1)
        prices = list(reversed(data))
        returns = [(prices[i]-prices[i+1])/prices[i+1] for i in range(len(prices)-1)]
        temp_returns = [(test_data[0][1]-prices[0])/prices[0]] + \
                       [(test_data[i][1]-test_data[i-1][1])/test_data[i-1][1]
                        for i in range(1, len(test_data))]
        test_returns.append(temp_returns)
        avg_rets.append(sum(returns) / float(len(returns)))
        #values.append([company] + prices + [""] + returns)
        cov_values.append(returns)
        # print(company)
        # print(len(returns))

    values = [list(i) for i in zip(*cov_values)]
    test_values = [list(i) for i in zip(*test_returns)]
    cov_table = numpy.cov(values, rowvar=False).tolist()
    cov_header = [[""] + companies] + [[company] for company in companies]
    avg_rets_table = [["Average Returns:"] + avg_rets]
    weights = [["Weights:"] + [.03 for a in avg_rets]]
    weights_header = [[""] + companies]

    avg_rets_row = len(cov_table) + 3

    results = []

    w_f = "C{0}:{1}{0}".format(str(avg_rets_row + 2),
                               num_rows_to_letters(len(weights[0])+1))
    ar_f = "C{0}:{1}{0}".format(str(avg_rets_row),
                                num_rows_to_letters(len(weights[0])+1))
    rfr_f = "B" + str(avg_rets_row + 5)
    pm_f = "B" + str(avg_rets_row + 6)
    psd_f = "B" + str(avg_rets_row + 7)
    size = len(weights[0]) - 1
    cv_f = "C2:{0}{1}".format(num_rows_to_letters(size+2),
                              str(size+1))

    formula = "=SUM({0})".format(w_f)
    results.append(["Total Weight:", formula])
    results.append(["Risk Free Rate:", 0.0073])
    formula = "=SUMPRODUCT({0},{1})-{2}".format(w_f, ar_f, rfr_f)
    results.append(["Mean Portfolio Return:", formula])
    formula = "=SQRT(MMULT(MMULT({0},{1}),TRANSPOSE({0})))".format(w_f, cv_f)
    results.append(["Portfolio SD:", formula])
    formula = "={0}^2".format(psd_f)
    results.append(["Portfolio Variance:", formula])
    formula = "=IF({0}=0,0,{1}/{0})".format(psd_f, pm_f)
    results.append(["Mean Sharpe Ratio:", formula])

    test_results_row = avg_rets_row + 11

    for i in range(len(test_values)):
        r_f = "C{0}:{1}{0}".format(str(test_results_row+i),
                                   num_rows_to_letters(len(test_values[i])+2))
        month, day, year = test_data[i][0]
        test_values[i] = ["{0}/{1}".format(month, year)] + \
                         ["=SUMPRODUCT({0},{1})".format(w_f, r_f)] + \
                         test_values[i]

    data = [
        {
            'range': 'NextGen!B1',
            'values': cov_header
        },
        {
            'range': 'NextGen!C2',
            'values': cov_table
        },
        {
            'range': 'NextGen!B' + str(avg_rets_row),
            'values': avg_rets_table
        },
        {
            'range': 'NextGen!B' + str(avg_rets_row + 1),
            'values': weights_header
        },
        {
            'range': 'NextGen!B' + str(avg_rets_row + 2),
            'values': weights
        },
        {
            'range': 'NextGen!A' + str(avg_rets_row + 4),
            'values': results
        },
        {
            'range': 'NextGen!A' + str(test_results_row),
            'values': test_values
        }
    ]

    body = {
      'valueInputOption': 'USER_ENTERED',
      'data': data
    }

    result = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheetId, body=body).execute()


if __name__ == '__main__':
    main2()
