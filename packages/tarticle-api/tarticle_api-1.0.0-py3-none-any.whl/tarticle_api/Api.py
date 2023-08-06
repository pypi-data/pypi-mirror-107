import requests

class Create(object):
    def __init__(self):
        pass

    def createPost(self, title, story, author='Аноним',is_allow=True):
        response = requests.post(
            f'https://api.tarticle.fun/createPost?title={title}' +
            f'&story={story}' +
            f'&is_allow={is_allow}' +
            f'&author={author}'
        )

        _json = response.json()

        if _json['status_code'] == 200:
            return _json
        elif _json['status_code'] == 405:
            return 'Methon not allowed'
        elif _json['status_code'] == 400:
            return f'ERROR 400: {_json["message"]}'

    def createAccount(self, name, pswd):
        response = requests.post(
            f'https://api.tarticle.fun/createAccount?name={name}' +
            f'&pswd={pswd}'
        )

        _json = response.json()

        if _json['status_code'] == 200:
            return _json
        elif _json['status_code'] == 405:
            return 'Methon not allowed'
        elif _json['status_code'] == 400:
            return f'ERROR 400: {_json["message"]}'
