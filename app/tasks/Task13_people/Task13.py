import logging
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from requests import get
import json

class Task13:
    '''
    Task 13 - people
    '''

    AI_Devs = None
    memory = []
    memoryFile = 'tasks/Task13_people/people.json'
    chat = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs
        self.chat = ChatOpenAI(model='gpt-3.5-turbo', openai_api_key=os.getenv('OPENAI_API_KEY'))

    def run(self) -> None:
        print('Task 13 - people')
        self.AI_Devs.authorize('people')

        task = self.AI_Devs.getTask()
        print('The task is:', task)
        question = task['question']
        print('The question is:', question)

        # load memory if exist
        if os.path.exists(self.memoryFile):
            with open(self.memoryFile, 'r') as file:
                self.memory = json.load(file)
        else:
            url = task['data']
            self.fillMemory(url)

        # fetch user name
        messages = [
            SystemMessage(
                content=(
                    'Answer questions as truthfully using the context below and nothing more. If you don\'t know the answer, say with single character "?" and nothing more.'
                    'Your task is to rewrite EXACTLY first name and last name in basic form from user message and information about context(food|live|colour) of user question.'
                    'All user questions will be in polish language.'
                    'Answer in JSON format. Do not add anything more.'
                    'Examples:'
                    '###'
                    'User: Co lubi jeść Jan Kowalski?'
                    'AI: {"imie":"Jan","nazwisko":"Kowalski","context":"food"}'
                    'User: Gdzie mieszka Adam Nowak?'
                    'AI: {"imie":"Adam","nazwisko":"Nowak","context":"live"}'
                    'User: Gdzie mieszka Adam Rozkaz?'
                    'AI: {"imie":"Adam","nazwisko":"Rozkaz","context":"live"}'
                    'User: Jaki jest ulubiony kolor Tomka Rusinka?'
                    'AI: {"imie":"Tomasz","nazwisko":"Rusin","context":"colour"}'
                    'User: Jaki jest ulubiony kolor Krysia Rusinka?'
                    'AI: {"imie":"Krystyna","nazwisko":"Rusin","context":"colour"}'
                    '###'
                )
            ),
            HumanMessage(content=question)
        ]
        response = self.chat.invoke(messages).content

        if response == '?':
            raise RuntimeError('Model can\'t fetch user name')

        user = json.loads(response)
        logging.info(user)

        # find user
        userItem = self.findInMemory(user)

        if userItem is None:
            raise RuntimeError('User not found')

        # specify action
        if user['context'] == 'colour':
            answer = userItem['ulubiony_kolor']
        else:
            # ask AI for answer
            if user['context'] == 'live':
                context = userItem['live']
                system_prompt = 'Write only the name o city.'
            elif user['context'] == 'food':
                context = userItem['food']
                system_prompt = 'Write only food name.'

            logging.info('Context: {}'.format(context))
            messages = [
                SystemMessage(
                    content=(
                        'Answer questions as truthfully using the context below and nothing more. If you don\'t know the answer, say with single character "?" and nothing more.'
                        'Be strict. Use short answer. Do not add anything more.'
                        '{} Context:###{}###'.format(system_prompt, context)
                    )
                ),
                HumanMessage(content=question)
            ]
            answer = self.chat.invoke(messages).content

        # send answer
        self.AI_Devs.answer(answer)

    def getKnowledge(self, knowledgeUrl: str) -> str:
        logging.info('Fetching knowledge...')

        with get(knowledgeUrl) as response:
            if 200 != response.status_code:
                raise RuntimeError('Unexpected http status code: {}'.format(response.status_code))

            return response.text

    def fillMemory(self, url: str) -> None:
        # load data
        knowledge = self.getKnowledge(url)

        # add uuid to data
        self.memory = json.loads(knowledge)

        for item in self.memory:
            about_me = item['o_mnie'].split('.')
            item['food'] = about_me[0].strip()
            item['live'] = about_me[1].strip()
            item['hobby'] = about_me[2].strip()

        knowledge = json.dumps(self.memory)

        with open(self.memoryFile, 'w') as file:
            file.write(knowledge)

    def findInMemory(self, user: dict) -> dict|None:
        for item in self.memory:
            if item['imie'] == user['imie'] and item['nazwisko'] == user['nazwisko']:
                return item

        return None
