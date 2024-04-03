import logging
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from tools.Errors import WrongAnswerError

class Task11:
    '''
    Task 11 - whoami
    '''

    AI_Devs = None
    chat = None
    messages = []

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 11 - whoami')
        self.AI_Devs.authorize('whoami')

        self.chat = ChatOpenAI(model='gpt-3.5-turbo', openai_api_key=os.getenv('OPENAI_API_KEY'))
        self.messages = [
            SystemMessage(
                content=(
                    'Answer questions as truthfully using the context below and nothing more. If you don\'t know the answer, say with single character "?" and nothing more. Your task is to guess what character the user is asking about.'
                    'Answer only with name of persion. Do not add anything more.'
                    'If you guess wrong, the user gives you another hint and you have to try to guess again.'
                )
            )
        ]

        hint = ''

        for tryCount in range(1, 10):
            try:
                logging.info('Trying: {}'.format(tryCount))
                hint += self.AI_Devs.getTask()['hint']
                logging.info('Hint: {}'.format(hint))
                guess = self.guess(hint)
                logging.info('Guess: {}'.format(guess))

                if guess == '?':
                    continue

                self.AI_Devs.answer(guess)

                break
            except WrongAnswerError:
                hint = 'Wrong answer. Another hint: '

                continue

        print(self.messages)

    def guess(self, hint: str) -> str:
        self.messages.append(HumanMessage(content=hint))
        response = self.chat.invoke(self.messages)
        self.messages.append(AIMessage(content=response.content))

        return response.content
