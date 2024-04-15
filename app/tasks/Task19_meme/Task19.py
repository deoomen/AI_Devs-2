import os
import requests
from pprint import pprint

class Task19:
    '''
    Task 19 - meme
    '''

    AI_Devs = None
    template_id = 'silly-otters-leave-wildly-1288'

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 19 - meme')
        self.AI_Devs.authorize('meme')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        memeUrl = self.prepareMeme(task['image'], task['text'])
        self.AI_Devs.answer(memeUrl)

    def prepareMeme(self, image: str, text: str) -> str:
        return requests.post(
            url='https://get.renderform.io/api/v2/render',
            headers={
                'Content-Type': 'application/json',
                'X-API-KEY': os.getenv('RENDERFORM_API_KEY')
            },
            json = {
                'template': self.template_id,
                'data': {
                    'image.src': image,
                    'title.text': text
                }
            }
        ).json()['href']
