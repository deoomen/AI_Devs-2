import logging
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class Task17:
    '''
    Task 17 - ownapi
    '''

    AI_Devs = None
    memory = []
    llm = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs
        self.llm = ChatOpenAI(model='gpt-4-vision-preview', openai_api_key=os.getenv('OPENAI_API_KEY'), temperature=0)

    def run(self) -> None:
        print('Task 17 - ownapi')
        self.AI_Devs.authorize('ownapi')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        self.AI_Devs.answer(os.getenv('NGROK_URL'))
