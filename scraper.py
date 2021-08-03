import requests, lxml.html as html, os, datetime

from requests.api import request

HOME_URL = 'https://www.rosario3.com/'
XPATH_LINK_ARTICLE = '//a[@class="cover-link"]/@href'
XPATH_TITLE = '//h1[@class="main-title font-900"]/text()'
XPATH_RESUMEN = '//h2[@class = "bajada font-600"]/p/text()'
XPATH_CUERPO = '//div[@class = "article-body"]/p/text()'

def parse_notices(link, fecha):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                sumary = parsed.xpath(XPATH_CUERPO)[0]
                body = parsed.xpath(XPATH_CUERPO)
            except IndexError:
                return
            with open(f'{fecha}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n \n')
                f.write(sumary)
                f.write('\n \n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        
        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code== 200: 
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_ARTICLE)
            #print(links_to_notices)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices: 
                parse_notices(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve) 


def run():
    parse_home()

if __name__ == '__main__':
    run()