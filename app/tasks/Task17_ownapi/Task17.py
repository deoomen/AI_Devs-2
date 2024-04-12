import os

class Task17:
    '''
    Task 17 - ownapi
    '''

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 17 - ownapi')
        self.AI_Devs.authorize('ownapi')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        self.AI_Devs.answer(os.getenv('NGROK_URL'))
