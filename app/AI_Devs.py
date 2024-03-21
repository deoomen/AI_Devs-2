import logging
import os
import requests

class AI_Devs:

    headers = {
        'Content-Type': 'application/json'
    }
    apiKey = None
    apiUrl = os.getenv('API_URL')
    token = None

    def __init__(self, apiKey: str) -> None:
        self.apiKey = apiKey

    def authorize(self, taskName: str) -> None:
        response = requests.post(
            self.apiUrl + 'token/' + taskName,
            headers = self.headers,
            json = {
                'apikey': self.apiKey
            },
        )
        json = self.parseResponse(response)
        self.token = json['token']

    def parseResponse(self, response: requests.Response) -> dict:
        if response.status_code != 200:
            raise RuntimeError('Unexpected HTTP status code: {}; Content: {}'.format(response.status_code, response.text))

        json = response.json()

        if json['code'] != 0:
            raise RuntimeError('Something went wrong :( Content: %s', json)

        return json

    def getTask(self) -> dict:
        response = requests.get(
            self.apiUrl + 'task/' + self.token,
            headers = self.headers,
        )
        json = self.parseResponse(response)

        return json

    def answer(self, answer: str) -> None:
        response = requests.post(
            self.apiUrl + 'answer/' + self.token,
            headers = self.headers,
            json = {
                'answer': answer
            }
        )
        json = self.parseResponse(response)

        logging.info(json['msg'])
