import os, sys
sys.path.append(os.path.dirname(__file__))

import csv
import numpy
from data_pull import *


def create_julia_matrix():
    companies = ["UNH", "ANIK", "NXPI", "MSFT", "ATVI", "NFLX", "AMZN", "GOOG",
                 "AAPL", "FB", "IDCC", "SUPN", "AGX", "SIMO", "MPH",
                 "MASI", "NTES", "THO", "CMCSA", "CM", "KINS", "MLVF",
                 "FIZZ", "PF", "TSLA", "MG", "BWXT", "KBAL", "FIVE"]

    cov_values = []
    avg_rets = []
    test_returns = []

    for company in companies:
        print(company)
        stock_data = google_pull(company)
        data, test_data = parse_monthly(stock_data, 1, 2014, 1, 2016, 12)
        prices = list(reversed(data))
        returns = [(prices[i]-prices[i+1])/prices[i+1] for i in range(len(prices)-1)]
        temp_returns = [(test_data[0][1]-prices[0])/prices[0]] + \
                       [(test_data[i][1]-test_data[i-1][1])/test_data[i-1][1]
                        for i in range(1, len(test_data))]
        test_returns.append(temp_returns)
        avg_rets.append(sum(returns) / float(len(returns)))
        cov_values.append(returns)

    values = [list(i) for i in zip(*cov_values)]
    cov_table = numpy.cov(values, rowvar=False).tolist()
    test_values = [list(i) for i in zip(*test_returns)]

    return (cov_table + [avg_rets], test_values)

def create_csv(matrix):
    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(matrix)

def main():
    matrix, test_values = create_julia_matrix()
    print(matrix)
    create_csv(matrix)

def main2():
    matrix, test_values = create_julia_matrix()
    w = [2.03619e-7,9.87886e-8,2.5367e-7,1.66346e-7,0.099995,9.11837e-7,3.19385e-7,1.09336e-7,1.32102e-7,3.94456e-7,2.48793e-7,1.53393e-7,9.4048e-8,2.88793e-6,0.3,1.16019e-7,0.299999,7.34302e-8,7.29761e-8,5.66724e-8,8.57135e-8,2.07396e-7,0.299998,1.98928e-7,1.01188e-7,8.77943e-8,6.17194e-8,5.69994e-8,7.87954e-8]
    print([weight*100 for weight in w])
    for x in test_values:
        sum = 0
        for i in range(len(w)):
            sum += x[i] * w[i]
        print(sum*100)

if __name__ == '__main__':
    main2()
