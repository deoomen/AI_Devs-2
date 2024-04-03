import logging
import os
from requests import get
from tenacity import retry, stop_after_attempt, wait_exponential
from tools.UserAgents import Rotator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class Task10:
    '''
    Task 10 - scraper
    '''

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 10 - scraper')
        self.AI_Devs.authorize('scraper')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        question = task['question']
        knowledge = self.getKnowledge(task['input'])

        chat = ChatOpenAI(model='gpt-3.5-turbo', openai_api_key=os.getenv('OPENAI_API_KEY'))
        messages = [
            SystemMessage(content='Answer questions as truthfully using the context below and nothing more. I will answer always in Polish. My aswers are short and strict. Context ###{}###'.format(knowledge)),
            HumanMessage(content=question),
        ]
        response = chat.invoke(messages)
        print(response)

        self.AI_Devs.answer(response.content)

    @retry(reraise=True, stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, min=2, max=10))
    def getKnowledge(self, knowledgeUrl: str) -> str:
        logging.info('Fetching knowledge...')
        rotator = Rotator()
        userAgent = rotator.get()

        with get(knowledgeUrl, headers={'User-Agent': userAgent.__str__()}) as response:
            if 200 != response.status_code:
                raise RuntimeError('Unexpected http status code: {}'.format(response.status_code))

            return response.text
