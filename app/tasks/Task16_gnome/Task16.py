import logging
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

class Task16:
    '''
    Task 16 - gnome
    '''

    AI_Devs = None
    memory = []
    llm = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs
        self.llm = ChatOpenAI(model='gpt-4-vision-preview', openai_api_key=os.getenv('OPENAI_API_KEY'), temperature=0)

    def run(self) -> None:
        print('Task 16 - gnome')
        self.AI_Devs.authorize('gnome')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        response = self.llm.invoke(
            [
                HumanMessage(
                    content=[
                        {
                            'type': 'text',
                            'text': 'What is colour of hat on gnome head? Tell me in POLISH. If any errors, on image is not gnome or there is no hat, return "ERROR". Be strict. Use short answer.'
                        },
                        {
                            'type': 'image_url',
                            'image_url': task['url']
                        }
                    ]
                )
            ]
        )
        logging.info(response.response_metadata)
        self.AI_Devs.answer(response.content)
