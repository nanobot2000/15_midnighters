import pytz
import requests
from datetime import datetime


def load_attempts():
    api_url = 'http://devman.org/api/challenges/solution_attempts/'
    page = 1
    while True:
        attempts_response = requests.get(
            api_url,
            params={'page': page}
        ).json()
        yield from attempts_response['records']
        total_pages = attempts_response['number_of_pages']
        if page == total_pages:
            break
        else:
            page += 1


def get_midnighters(attempts):
    midnight_hour = 0
    morning_hour = 6
    midnighters = set()
    for attempt in attempts:
        time_zone = pytz.timezone(attempt['timezone'])
        attempt_time = datetime.fromtimestamp(attempt['timestamp'], time_zone)
        if midnight_hour <= attempt_time.hour < morning_hour:
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
