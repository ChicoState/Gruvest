''' Tequila Trader 2020 '''

import yfinance as yf
import argparse # Allows us to use command line arguments
import threading # multithreading
import csv # write to csv files
#import sys
#import uno
#import datetime

#pip3 install -e git+git://github.com/vonHacht/yfinance.git@master#egg=yfinance

# Function used in multithreading to collect information from yfinance
def parse_stock_pages(entities, symbol):
    proceed = 5
    while(proceed > 0):
        try:
            stock = yf.Ticker(symbol) # call to yfinance
            info = stock.info
            data = []

            items.append([
                info["longName"],
                info["symbol"],
                info["bid"],
                info["ask"],
                info["open"],
                info["dayLow"],
                info["dayHigh"],
                info["previousClose"],
                info["volume"],
                info["fiftyDayAverage"],
                info["twoHundredDayAverage"],
                info["dividendRate"],
                info["forwardPE"],
                info["beta"],
                info["trailingAnnualDividendYield"],
                info["payoutRatio"],
                info["fiftyTwoWeekHigh"],
                info["fiftyTwoWeekLow"],
                info["marketCap"],
                info["quoteType"],
                info["fiveYearAvgDividendYield"],
                info["enterpriseToRevenue"],
                info["forwardEps"],
                info["bookValue"],
                info["enterpriseToEbitda"],
                info["enterpriseValue"],
                info["lastSplitFactor"],
                info["earningsQuarterlyGrowth"]
            ])
            print(
                info["longName"],
                info["symbol"],
                info["bid"],
                info["ask"],
                info["open"],
                info["dayLow"],
                info["dayHigh"],
                info["previousClose"],
                info["volume"],
                sep=",")
            # info["fullTimeEmployees"], ----- Not all stocks have this listed
            #print(hist)
            proceed = 0
        except exception as e:
            proceed -= 1
            print("ERROR FOR %s: %s" %(symbol, e)) #sys.exc_info()

def main(doc):
    #if doc[-4:] != ".csv":
        #print("Error: Document is not a CSV File.")
        #quit()
    print("Fetching data for %s"%(doc))

    #start by loading up symbols from txt file
    stocksToLoad = open(doc + ".txt", "r")
    fromStocksToLoad = stocksToLoad.readlines()
    items = []
    fields = []
    threads = []
    #parse_stock_pages(items, fromStocksToLoad[0][:-1], fields, True)
    #amtStocks = len(fromStocksToLoad)
    #for i in range(1, amtStocks):
    for stock in fromStocksToLoad:
        #print(stock[:-1])
        #stock = fromStocksToLoad[i][:-1]
        th = threading.Thread(target=parse_stock_pages,args=[items, stock[:-1]])
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    # Write to CSV File
    fields = [
        'Name',
        'Symbol',
        'Bid',
        'Ask',
        'Open',
        'Day Low',
        'Day High',
        'Previous Close',
        'Volume',
        'Fifty Day Average',
        'Two Hundred Day Average',
        'Dividend Rate',
        'Forward PE',
        'Beta',
        'Trailing Annual Dividend Yield',
        'Payout Ratio',
        'Fifty Two Week High',
        'Fifty Two Week Low',
        'Market Cap',
        'Quote Type',
        'Five Year Avg Dividend Yield',
        'Enterprise To Revenue',
        'Forward Eps',
        'Book Value',
        'Enterprise To EBITDA',
        'Enterprise Value',
        'Last Split Factor',
        'Earnings Quarterly Growth'
        ]

    with open(doc + ".csv", 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing to file
        csvwriter.writerows(items)

    # close documents
    csvfile.close()
    stocksToLoad.close()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('document', help = 'CSV File')
    args = argparser.parse_args()
    doc = args.document
    #if doc[-4:] != ".csv":
        #print("Error: Document is not a CSV File.")
        #quit()
    main()
