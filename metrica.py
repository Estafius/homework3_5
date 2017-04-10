from urllib.parse import urljoin
import requests


AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = '4dcdbc1768e24a24a0adf924b5b24981'  # Your app_id here

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

TOKEN = 'AQAAAAAUJ0LYAAQw7bg_PVCe9kjVu9ozx0O6lo0'  # Your token here


class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    token = None

    def __init__(self, token):
        self.token = token

    def get_header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
            'User-Agent': 'asdasdasd'
        }

    @property
    def counter_list(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        counter_list = [c['id'] for c in response.json()['counters']]
        return counter_list

    def get_count(self, counter_id,option_metrica):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:' + option_metrica
        }

        response = requests.get(url, params, headers=headers)
        items_count = response.json()['data'][0]['metrics'][0]
        return items_count


def main():
    metrika = YandexMetrika(TOKEN)
    list_count = ['visits', 'pageviews', 'users']
    for counter in metrika.counter_list:
        for option_metrica in list_count:
            print('Number of ', option_metrica, '= ', int(metrika.get_count(counter, option_metrica)))

main()