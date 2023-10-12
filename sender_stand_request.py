import requests

from yandex_api_stand_tests import configuration


def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH, json=body)

def get_users_table():
        return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)

def get_docs():
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)

def get_logs():
        return requests.get(configuration.URL_SERVICE + configuration.LOG_MAIN_PATH)

response = get_users_table()
print(response.status_code)
print(response.text)



