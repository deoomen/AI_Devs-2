import os
from openai import OpenAI

class Task06:
    '''
    Task 06 - embedding
    '''

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 06 - embedding')
        self.AI_Devs.authorize('embedding')

        task = self.AI_Devs.getTask()
        print('The task is:', task)
        sentence = 'Hawaiian pizza'

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.embeddings.create(
            input=sentence,
            model='text-embedding-ada-002'
        )

        self.AI_Devs.answer(response.data[0].embedding)
