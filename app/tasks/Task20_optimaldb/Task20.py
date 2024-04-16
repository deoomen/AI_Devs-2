import os
from requests import get
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class Task20:
    '''
    Task 20 - optimaldb
    '''

    AI_Devs = None
    chat = None
    memory_file = 'tasks/Task20_optimaldb/3friends.json'
    memory_file_optimal = 'tasks/Task20_optimaldb/3friends-optimal.json'

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs
        self.chat = ChatOpenAI(model='gpt-3.5-turbo', openai_api_key=os.getenv('OPENAI_API_KEY'))

    def run(self) -> None:
        print('Task 20 - optimaldb')
        self.AI_Devs.authorize('optimaldb')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        database = self.getDatabase(task['database'])
        database = self.getDatabase('')
        database_optimal = {}
        with open(self.memory_file_optimal, 'r') as file:
            database_optimal = json.load(file)
        system_prompt = SystemMessage(
            content=(
                'Twoim zadaniem się streszczenie informacji podanych przez użytkownika.'
                'Streść podany tekst do około 1/3 długości zachowując kontekst wypowiedzi.'
                'Usuń wszystkie słowa, który nie mają znaczenia dla kontekstu zdania. Usuń też imię z wypowiedzi.'
                'Skrócone zdanie musi pozwalać wyciągnąć te same wnioski co oryginalny tekst.'
                'Zwróć dokładnie tylko streszczoną informację i nic więcej.'
                'Zasady:'
                '1. Wypowiedź musi być krótsza niż treść użytkownika.'
                '2. Sens wypowiedzi musi zostać zachowany.'
                '3. Usuń imię z wypowiedzi.'
                'Przykład:'
                '###'
                'User: Podczas ostatniej konferencji technologicznej, program który stworzył Zygfryd wygrał nagrodę za innowacyjność w użyciu JavaScript. Ulubionym instrumentem muzycznym Zygfryda jest ukulele, na kt\u00f3rym gra po nocach. Zygfryd hoduje rzadki gatunek storczyka.'
                'AI: Zygfryd: wygrał nagrodę za innowacyjność w użyciu JavaScript, ulubiony instrument to ukulele, hoduje stroczyki.'
                '###'
                'Weź głęboki wdech i zastanów się jeszcze raz czy można skrócić wypowiedź bardziej.'
            )
        )

        for person, informations in database.items():
            database_optimal[person] = []
            short_info = self.chat.invoke([system_prompt, HumanMessage(content=' '.join(informations))]).content
            database_optimal[person].append(short_info)

        with open(self.memory_file_optimal, 'w') as file:
            json.dump(database_optimal, file)

        self.AI_Devs.answer(json.dumps(database_optimal))

    def getDatabase(self, url: str) -> dict:
        # load memory if exist
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as file:
                return json.load(file)

        with get(url) as response:
            if 200 != response.status_code:
                raise RuntimeError('Unexpected http status code: {}'.format(response.status_code))

            with open(self.memory_file, 'w') as file:
                file.write(response.text)

            return json.loads(response.text)
