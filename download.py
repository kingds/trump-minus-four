import sys
sys.path.append("/path/to/store/downloaded/tweets")
import Exporter
import time
import os

# Set up the dates to scan
years = [2016]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 16]

username = "realdonaldtrump"

# Loop through all dates
for year in years:
    for month in months:
        for day in range(1, days[month - 1] + 1):
            print month, day
            if month == "04" and day == 4:
                print "Skipping 2016-04-04"
                continue
            until_day = str(day+1).zfill(2)
            day = str(day).zfill(2)            
            month = str(month).zfill(2)
            since_date = "%s-%s-%s" % (year, month, day)
            until_date = "%s-%s-%s" % (year, month, until_day)
            csv_file = "downloaded_tweets/%s-%s-%s.csv" % (year, month, day)
            if not os.path.exists(csv_file):
                args = ["--username", username, "--since", since_date, "--until", until_date, csv_file]
                Exporter.main(args)
                os.rename("output_got.csv", csv_file)
                print "Downloaded " + since_date
                time.sleep(1)
            else:
                print "Already downloaded " + since_date
            
