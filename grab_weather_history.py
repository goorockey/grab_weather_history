#coding: utf-8

import argparse
from pyquery import PyQuery as pq
from datetime import date, timedelta
from dateutil.parser import parse as parse_time

url_pattern = 'http://www.wunderground.com/history/airport/%(airport)s/%(date)s/DailyHistory.html?format=1'

def grab_data(file_target, airport, start_date, end_date=None):
    has_insert_header = False
    try:
        with open(file_target, 'wb') as fout:
            delta = timedelta(days=1)
            while start_date <= end_date:
                url = url_pattern % {
                    "airport": airport,
                    "date": start_date.strftime('%Y/%m/%d'),
                }

                print url

                try:
                    doc = pq(url=url, headers={'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'})
                    data = doc[0].text_content().split('\n')
                    if not doc:
                        print 'Failed to grab data of ' + str(start_date)
                        continue
                except:
                    print 'Failed to grab data of ' + str(start_date)
                    continue

                if not has_insert_header:
                    fout.write('Date,' + data[0].encode('utf8') + '\n')

                data = [ str(start_date) + ',' + d.encode('utf8') for d in data[1:] if len(d) ]

                fout.write('\n'.join(data))

                has_insert_header = True
                start_date += delta

    except Exception as e:
        print e
        print 'Failed to save data to %s(%s)' % (file_target, str(e))

def parse_args():
    parser = argparse.ArgumentParser(description='Grab weather history from wunderground.com')
    parser.add_argument('--airport', dest='airport', default='ZHHH', help='Target airport.Default is ZHHH.')
    parser.add_argument('-f', dest='file', default='wunderground%s.csv' %  date.today().strftime('%Y%m%d'), help='Output file.')
    parser.add_argument('--start', dest='start', default=date.today(), help='Start date(YYYY-MM-DD). Optional. Default is today.')
    parser.add_argument('--end', dest='end', help='End date(YYYY-MM-DD). Optional. Default is today.')

    args = parser.parse_args()

    if not isinstance(args.start, date):
        args.start = parse_time(args.start).date()

    if args.end is not None and not isinstance(args.end, date):
        args.end = parse_time(args.end).date()

    if args.end is None:
        args.end = date.today()

    if args.start > args.end:
        args.end = args.start

    return args

if __name__ == '__main__':
    args = parse_args()
    grab_data(args.file, args.airport, args.start, args.end )
