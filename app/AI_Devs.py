import logging
import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from tools.Errors import WrongAnswerError

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
        logging.info('Authorized')

    def parseResponse(self, response: requests.Response) -> dict:
        if response.status_code == 406:
            json = response.json()
            raise WrongAnswerError(json['code'], json['msg'])
        elif response.status_code != 200:
            raise RuntimeError('Unexpected HTTP status code: {}; Content: {}'.format(response.status_code, response.text))

        json = response.json()

        if json['code'] != 0:
            raise RuntimeError('Something went wrong :( Content: %s', json)

        return json

    @retry(reraise=True, stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=2, max=10))
    def getTask(self) -> dict:
        response = requests.get(
            self.apiUrl + 'task/' + self.token,
            headers = self.headers,
        )
        logging.info('Task fetched')
        json = self.parseResponse(response)

        return json

    def postTask(self, payload: dict) -> dict:
        response = requests.post(
            self.apiUrl + 'task/' + self.token,
            data = payload,
        )
        logging.info('Task posted')
        json = self.parseResponse(response)

        return json

    def answer(self, answer: str) -> str:
        response = requests.post(
            self.apiUrl + 'answer/' + self.token,
            headers = self.headers,
            json = {
                'answer': answer
            }
        )
        logging.info('Answer sent: {}'.format(answer))
        json = self.parseResponse(response)

        logging.info(json['msg'])

        return json['msg']
