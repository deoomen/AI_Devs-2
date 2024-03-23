class Task01:
    """
    Task 01 - helloapi
    """

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 01 - helloapi')
        self.AI_Devs.authorize('helloapi')

        task = self.AI_Devs.getTask()
        print('The task is: ', task['msg'])

        self.AI_Devs.answer(task['cookie'])
