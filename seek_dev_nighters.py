import pytz
import requests
from datetime import datetime


def load_attempts():
    api_url = 'http://devman.org/api/challenges/solution_attempts/'
    pages = requests.get(api_url).json().get('number_of_pages')
    for page in range(1, pages+1):
        yield from requests.get(api_url,
                                params={'page': page}).json().get('records')


def get_midnighters(attempts):
    midnighters = set()
    for attempt in attempts:
        time_zone = pytz.timezone(attempt['timezone'])
        attempt_time = datetime.fromtimestamp(attempt['timestamp'], time_zone)
        if 0 <= attempt_time.hour < 6:
            midnighters.add(attempt['username'])
    return midnighters


if __name__ == '__main__':
    attemps = load_attempts()
    midnighters = get_midnighters(attemps)
    print('Midnighters on Devman:')
    print('-----------------------')
    for index, midnighter in enumerate(midnighters, 1):
        print(index, midnighter)
    print('_______________________')
