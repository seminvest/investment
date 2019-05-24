import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
from pprint import pprint


def get_btc_historic_data(start_date=None, end_date=None):
    if start_date is None or end_date is None or len(str(start_date)) != 8 or len(str(end_date)) != 8:
        print('No valid date range.')
        return []
    else:
        req_url = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start={}&end={}'.format(start_date, end_date)
        data = {
            'start': start_date,
            'end': end_date
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'coinmarketcap.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/64.0.3257.0 Safari/537.36'
        }

        while True:
            try:
                page = requests.get(
                    url=req_url,
                    headers=headers,
                    data=data
                ).content
                break
            except:
                sleep(1)

        soup = BeautifulSoup(page, 'html.parser')

        head = [
            i.get_text().strip() for i in soup.select('#historical-data > div > div.table-responsive > table > thead > tr > th')
        ]

        rows_data = soup.select('#historical-data > div > div.table-responsive > table > tbody > tr > td')

        rows_data = [
                list(i) for i in zip(*[iter(rows_data)] * len(head))
            ]
        data_list = []
        for row in rows_data:
            try:
                data_list.append(dict(zip(head,
                                          [
                                              datetime.strptime(row[0].get_text().strip(), '%b %d, %Y'),
                                              float(row[1].get_text().strip()),
                                              float(row[2].get_text().strip()),
                                              float(row[3].get_text().strip()),
                                              float(row[4].get_text().strip()),
                                              int(row[5].get_text().strip().replace(',', '')),
                                              int(row[6].get_text().strip().replace(',', ''))
                                          ])))
            except Exception as e:
                pass
        return data_list


pprint(get_btc_historic_data('20160101', '20171103'))
pprint(get_btc_historic_data('20161231', '20170101'))
pprint(get_btc_historic_data('20160708', '20171206'))
