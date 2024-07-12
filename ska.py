import time
import requests
import json
from urllib.parse import urlparse

import telebot
import datetime

PRICE = 19.1


def get_course():
    url = 'https://api.cryptorank.io/v1/currencies?api_key=f4fd2781179331f3621470c4b3db233dc560de1cc2e38255204af5b432e7&ids=187369,160758'
    r = requests.get(url)
    val = json.loads(r.text)['data']
    TON = 0
    NOT = 0
    for v in val:
        # print(v)

        if v['values']:
            if v['values']['USD']:

                if v['id'] == 187369:
                    NOT = v['values']['USD']['price']
                    # if type(NOT) == float:
                        # NOT = float('{:.2f}'.format(NOT))
                        # NOT = round(NOT, 2)
                    # print(NOT)

                elif v['id'] == 160758:
                    TON = v['values']['USD']['price']
                    # if type(TON) == float:
                        # TON = round(TON, 2)
                    #     TON = float('{:.2f}'.format(TON))
                    # print(TON)

    return {'TON': TON or 0, 'NOT': NOT or 0}


def print_log(e):
    a = str(datetime.datetime.now() + datetime.timedelta(hours=0))
    print(e)
    a = open('logs//' + a + '-excep.txt', 'w')
    a.write(e)
    a.close()


def get_one():
    url = 'https://api.getgems.io/graphql'
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru',
        'Host': 'api.getgems.io',
        'Origin': 'https://getgems.io',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://getgems.io/',
        'x-gg-client': 'v:1 l:ru',
        'Priority': 'u=3, i',
        'x-auth-token': '',
        'x-aws-waf-token': '52d02336-2708-425c-a513-a0040ef9dbc0:EQoAiAxSywwRAAAA:PfBmKbh4eCtGh5QUs/0RlEdiYajeYsWsr/Q9+546HY0fxFfds/1hmzLaGyjGTyceqBvJe3QhRRbQ6kIkbU7OLK1HCnCxyNBO4UzszbJ0eR84Awf1XMf8u6enyLg0nAZeuHidlEfQ25ss6oz5cpMChukQ37x1JzZTpCJhUDpauky/EZR6JW1SKOdD4HHnB2coqftQdT/kD4xeLvvHtuQSabgbVwqWFWSnJmrW3eMhuKc='
    }

    params = {
        'operationName': 'nftSearch',
        'variables': '{"query":"{\\"$and\\":[{\\"collectionAddress\\":\\"EQDmkj65Ab_m0aZaW8IpKw4kYqIgITw_HRstYEkVQ6NIYCyW\\"},{\\"saleType\\":\\"fix_price\\"}]}","attributes":null,"sort":"[{\\"isOnSale\\":{\\"order\\":\\"desc\\"}},{\\"price\\":{\\"order\\":\\"asc\\"}},{\\"index\\":{\\"order\\":\\"asc\\"}}]","count":30}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"566aab5b51f3a22f10b7ae0acbed38d14f7466f042a8dcbf98b260ba6c52bd33"}}'
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                ans = response.text
                di = json.loads(ans)
                name = di['data']['alphaNftItemSearch']['edges'][0]['node']['name']
                price = int(di['data']['alphaNftItemSearch']['edges'][0]['node']['sale']['fullPrice']) / 10 ** 9
                adr_col = di['data']['alphaNftItemSearch']['edges'][0]['node']['address']
                adr_id = di['data']['alphaNftItemSearch']['edges'][0]['node']['ownerAddress']
                add = 'https://getgems.io/collection/' + adr_col + '/' + adr_id
                return {'name': name, 'price': price, 'address': add}
            except Exception as e:
                print(e)
                return None
        else:
            print('Ошибка запроса:', response.status_code)
            print_log('Ошибка запроса: ' + str(response.status_code))
            return ('Ошибка запроса:', response.status_code)
    except Exception as ex:
        print('/RESP Ошибка запроса:', str(ex))
        print_log('/RESP Ошибка запроса: ' + str(ex))
        return ('/RESP Ошибка запроса:', str(ex))


TOKEN_BOT = '2137380397:AAE5M-KsMuWxMQtJftw1WA4rhYJtWLrPRz4'
PUBLIC_ID = '@ftnotifi'
try:
    bot = telebot.TeleBot(TOKEN_BOT)
    ntime = '00:00'
    bot.edit_message_text(chat_id=PUBLIC_ID, message_id=3, text='starting')
except Exception as ebot:
    print_log('STARTBOT:::' + str(ebot))
while True:
    obj = get_one()
    try:
        # print(obj)
        if obj['price'] < PRICE:
            pr = get_course()
            print(obj)
            try:
                PREMES = f"- 10kNOT: ${pr['NOT'] * 10000}\n- Vaucher: ${pr['TON'] * obj['price']}\n"
                plus = pr['NOT'] * 10000 - pr['TON'] * obj['price'] - pr['TON'] * 0.3
                if type(plus) == float:
                    # plus = float('{:.2f}'.format(plus))
                    plus = round(plus, 2)
                if plus >= 15:
                    margin = f"💚 ${plus}\n"
                elif plus >= 10:
                    margin = f"💛 ${plus}\n"
                else:
                    margin = f"❌ ${plus}\n"

                MES = margin + PREMES + f"<b>{obj['price']} - {obj['name']}</b>\n {obj['address']}"
                bot.send_message(PUBLIC_ID, MES, parse_mode='HTML')
            except:
                bot.send_message((PUBLIC_ID, 'AAAAAAAAAAAA'))
        else:
            print(obj['price'])
    except:
        print('a')
    n = (datetime.datetime.now() + datetime.timedelta(hours=0)).strftime('%H:%M')
    if n != ntime:
        ntime = n
        try:
            bot.edit_message_text(chat_id=PUBLIC_ID, message_id=3, text=ntime + ' ' + str(obj['price']))
        except:
            bot.edit_message_text(chat_id=PUBLIC_ID, message_id=3, text=ntime)
    time.sleep(22)
