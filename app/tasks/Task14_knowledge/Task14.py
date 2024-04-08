import logging
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from requests import get
import json

class Task14:
    '''
    Task 14 - knowledge
    '''

    AI_Devs = None
    memory = []
    chat = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs
        self.chat = ChatOpenAI(model='gpt-3.5-turbo', openai_api_key=os.getenv('OPENAI_API_KEY'))

    def run(self) -> None:
        print('Task 14 - knowledge')
        self.AI_Devs.authorize('knowledge')

        task = self.AI_Devs.getTask()
        print('The task is:', task)
        question = task['question']
        print('The question is:', question)

        # specify question type
        question_type = self.chat.invoke(
            [
                SystemMessage(
                    content=(
                        'Your task is to specify context(currency|population|general) of user question.'
                        'If you don\'t know the answer, say with single character "?" and nothing more.'
                        'All user questions will be in polish language.'
                        'Examples:'
                        '###'
                        'User: Jaki jest kurs dolara?'
                        'AI: currency'
                        'User: Ile ludzi mieszka w Polsce?'
                        'AI: population'
                        'User: Czy kura to dinozaur?'
                        'AI: general'
                        '###'
                    )
                ),
                HumanMessage(content=question)
            ]
        ).content
        logging.info('Question type: {}'.format(question_type))

        if question_type == 'currency':
            currency = self.chat.invoke(
                [
                    SystemMessage(
                        content=(
                            'Your task is to write currency name from user input as three letter currency code according to ISO 4217 standard. User use polish. You will translate country name to english.'
                            'If you don\'t know the answer, say with single character "?" and nothing more.'
                            'Examples:'
                            '###'
                            'User: Jaki jest kurs dolara?'
                            'AI: USD'
                            '###'
                        )
                    ),
                    HumanMessage(content=question)
                ]
            ).content
            logging.info('Currency: {}'.format(currency))

            if currency == '?':
                raise RuntimeError('Model don\'t recognize currency')

            with get('http://api.nbp.pl/api/exchangerates/rates/A/{}/'.format(currency)) as response:
                if 200 != response.status_code:
                    raise RuntimeError('Unexpected http status code: {}'.format(response.status_code))

                answer = json.loads(response.text)['rates'][0]['mid']

        elif question_type == 'population':
            country = self.chat.invoke(
                [
                    SystemMessage(
                        content=(
                            'Your task is to write country name from user input. User use polish. You will translate country name to english.'
                            'If you don\'t know the answer, say with single character "?" and nothing more.'
                            'Examples:'
                            '###'
                            'User: Ile ludzi mieszka w Polsce?'
                            'AI: Polska'
                            '###'
                        )
                    ),
                    HumanMessage(content=question)
                ]
            ).content.lower()
            logging.info('Country: {}'.format(country))

            if country == '?':
                raise RuntimeError('Model don\'t recognize country')

            with get('https://restcountries.com/v3.1/name/{}'.format(country)) as response:
                if 200 != response.status_code:
                    raise RuntimeError('Unexpected http status code: {}'.format(response.status_code))

                answer = json.loads(response.text)[0]['population']

        elif question_type == 'general':
            answer = self.chat.invoke(
                [
                    SystemMessage(
                        content=(
                            'Answer questions as truthfully and nothing more. Be strict. Short answer. If you don\'t know the answer, say with single character "?" and nothing more.'
                        )
                    ),
                    HumanMessage(content=question)
                ]
            ).content

        else:
            raise RuntimeError('Invalid question type')

        self.AI_Devs.answer(answer)
