import os
from pprint import pprint
from openai import OpenAI

class Task03:
    """
    Task 03 - blogger
    """

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 03 - blogger')
        self.AI_Devs.authorize('blogger')

        task = self.AI_Devs.getTask()
        print('The task is: ', task)

        answer = []
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        messages = [
            {
                'role': 'system',
                'content': 'Jesteś profesjonalnym kucharzem. Twoja specjalizacja to pizza włoska. Twoim zadaniem będzie stworzenie przepisu na najlepszą pizzę Margherita na świecie. Wszystkie Twoje odpowiedzi mają dotyczyć tylko tego rodzaju pizzy. Odpowiadaj zawsze w języku polskim.',
            },
        ]
        tokensUsed = 0

        for chapter in task['blog']:
            messages.append(
                {
                    'role': 'user',
                    'content': chapter,
                }
            )
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
            messages.append(
                {
                    'role': response.choices[0].message.role,
                    'content': response.choices[0].message.content,
                }
            )
            answer.append(response.choices[0].message.content)
            tokensUsed += response.usage.total_tokens
            pprint(answer)
            print('Tokens used: {}'.format(tokensUsed))

            choice = input('Continue? [y]/n ')

            if 'y' != choice:
                exit(1)

        self.AI_Devs.answer(answer)
