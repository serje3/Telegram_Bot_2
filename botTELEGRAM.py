from config_bot import BOT_SETTINGS
import telebot
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import random

HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'}

def get_html(name):
    session = requests.Session()
    html = session.get(
        'https://yandex.ru/images/search?text='+name.replace(" ","%20"), headers = HEADERS)
    return html,session


def get_elements(name):
    html,session = get_html(name)
    soup = BeautifulSoup(html.text,'html.parser')
    items = soup.find_all('img')
    return items, session

def random_element(name):
    items, session = get_elements(name)
    element = random.choice(items[1:])

    return element.get('src'), session

class BOT_MAIN(telebot.TeleBot):
    def __init__(self):
        super().__init__(BOT_SETTINGS.TOKEN, parse_mode=None)
        msg_hndl = super().message_handler
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)

        markup.row("Фотография")

        @msg_hndl(commands=['start'])
        def handle_start(msg):
            bot.send_message(msg.chat.id, f"prevet {msg.chat.username}", reply_markup=markup)


        @msg_hndl(func=lambda message:True,content_types=['text'])
        def handle_reg(msg):
            img_name = self.get_img(msg.text)
            if img_name == 'Ошибочька':
                bot.send_message(msg.chat.id,'Ошибочька')
            else:
                bot.send_photo(msg.chat.id, open(img_name,'rb'))



    @staticmethod
    def get_img(name):
        img_url, session = random_element(name)
        img_name = 'img_2.jpg'
        try:
            img = 'http://'+img_url.replace('http://','')
            img = session.post(img.replace('////','//'),headers = HEADERS)
            session.close()
        except ConnectionError as e:
            print(e)
            return 'Ошибочька'

        with open(img_name,'wb') as target:
            target.write(img.content)
        return img_name




bot = BOT_MAIN()
bot.polling()
