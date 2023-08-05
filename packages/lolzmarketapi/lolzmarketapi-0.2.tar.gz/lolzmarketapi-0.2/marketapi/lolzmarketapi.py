########################
# By BotFather
# By lolz.guru/botfather
########################

import requests
from bs4 import BeautifulSoup

class Api:
    def __init__(self, cookies, userAgent):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,da;q=0.6',
            'cache-control': 'max-age=0',
            'cookie': cookies,
            'referer': 'https://lolz.guru/',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': userAgent
        }

        response = requests.get('https://lolz.guru/market/', headers=self.headers)

        soup = BeautifulSoup(response.text, 'lxml')

        self.profileUrl = soup.find('div', class_='Menu JsOnly').find('a')['href']

        if 'members' in self.profileUrl:
            self.profileId = self.profileUrl.split("members/")[1].replace("/","")
        else:
            name = self.profileUrl.split("lolz.guru/")[1].replace("/","")
            response = requests.get(url="https://lolz.guru/api/index.php?users/find&username="+name).json()
            self.profileId = response['users'][0]['user_id']

        response = requests.get('https://lolz.guru', headers=self.headers)

        soup = BeautifulSoup(response.text, 'lxml')

        self.xfToken = soup.find('input', {'name':'_xfToken'})['value']

    def getBal(self):
        response = requests.get(f'https://lolz.guru/market/user/{self.profileId}/payments', headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        bal = soup.find('span', class_='balanceValue').text
        try:
            balHold = soup.find('span', class_='balanceNumber muted').text.replace("\n","").replace("	","")
        except:
            balHold = 0
        return [bal, balHold]

    def transfer(self, username, amount, comment='', secret_answer=''):
        res = requests.post("https://lolz.guru/market/balance/transfer", headers=self.headers, data={'username_receiver': username, 'amount': amount, 'currency': 'rub', 'comment': comment, 'secret_answer': secret_answer, '_xfRequestUri': '/market/balance/transfer', '_xfNoRedirect': '1', '_xfResponseType': 'json', '_xfToken': self.xfToken})
        return res.text
    
    def getPayments(self, page):
        response = requests.get(f'https://lolz.guru/market/user/{self.profileId}/payments?type=money_transfer&page={page}', headers=self.headers)
        base = BeautifulSoup(response.text, 'lxml')
        soup = base.find_all('div', class_='item')
        payments = []
        for i in range(len(soup)):
            titleAction = soup[i].find('div', class_='titleAction').text.replace("\n","").replace("  ","")
            try:
                date = soup[i].find('abbr', class_='DateTime muted').text
            except:
                date = ""
            try:
                com = soup[i].find('div', class_='muted comment').text.replace("\n","").replace("  ","")
            except:
                com = ""
            try:
                count = soup[i].find('span', class_='out').text
            except:
                count = soup[i].find('span', class_='in').text
            payments.append([titleAction, date, com, count])
        return payments
    
    def parseMarket(self, url, page):
        response = requests.get(f'{url}/&page={page}', headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('div', class_='marketIndexItem')
        parsed = []
        for i in range(len(items)):
            title = items[i].find('a','marketIndexItem--Title').text
            href = items[i].find('a','marketIndexItem--Title')['href']
            price = items[i].find('div', class_='marketIndexItem--Price').text.replace("\n","")
            parsed.append([title, price, 'https://lolz.guru/'+href])
        return parsed

    def bookAccount(self, account_id, log):
        response = requests.get(f'https://lolz.guru/market/{account_id}', headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        lnk = soup.find('div', class_='mn-30-0-0').find('a')['href']
        result = requests.get('https://lolz.guru/'+lnk, headers=self.headers)
        if log == 1:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                lnk = soup.find('div', class_='mn-30-0-0').find('a')['href']
                if 'buy' in lnk:
                    return "Success"
                else:
                    return "Error"
            except:
                return "Error"

    def unbookAccount(self, account_id):
        requests.get(f'https://lolz.guru/market/{account_id}/cancel-buy?_xfToken={self.xfToken}', headers=self.headers)
        return "Completed"
        
    def buyAccount(self, account_id, bron):
        if bron == 0:
            self.bookAccount('https://lolz.guru/market/'+str(account_id), 0)
        response = requests.post(f'https://lolz.guru/market/{account_id}/confirm-buy', data={'_xfToken': self.xfToken, '_xfConfirm': '1'}, headers=self.headers)
        
    def accountInfo(self, account_id):
        response = requests.get('https://lolz.guru/market/'+str(account_id), headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h1', 'marketItemView--titleStyle').text
        title = title.split('\n')[1].replace("\t","")
        price = soup.find('span', class_='value').text
        seller = soup.find('div', class_='marketItemView--sidebarUser--Username').find('a').find('span').text
        try:
            garant = soup.find('span', class_='simpleGurantee').text.replace("\n", "").replace("\t", "")
        except:
            garant = ""
        if garant == "":
            try:
                garant = soup.find('span', class_='extendedGuarantee').text.replace("\n", "").replace("\t", "")
            except:
                garant = ""
        createDate = soup.find('abbr', class_='DateTime').text
        lnk = soup.find('div', class_='mn-30-0-0').find('a')['href']
        if 'balance' in lnk:
            canBuy = 1
        else:
            canBuy = 0
        return [title, price, seller, createDate, garant, canBuy]