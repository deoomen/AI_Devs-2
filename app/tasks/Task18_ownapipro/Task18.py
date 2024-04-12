import os

class Task18:
    '''
    Task 18 - ownapipro
    '''

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 18 - ownapipro')
        self.AI_Devs.authorize('ownapipro')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        self.AI_Devs.answer(os.getenv('NGROK_URL'))
