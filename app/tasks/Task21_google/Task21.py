import os

class Task21:
    '''
    Task 21 - google
    '''

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 21 - google')
        self.AI_Devs.authorize('google')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        self.AI_Devs.answer(os.getenv('NGROK_URL'))
