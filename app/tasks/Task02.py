import os
from openai import OpenAI

class Task02:
    """
    Task 02 - moderation
    """

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 02 - moderation')
        self.AI_Devs.authorize('moderation')

        task = self.AI_Devs.getTask()
        print('The task is: ', task)

        answer = []
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        for sentence in task['input']:
            result = client.moderations.create(
                input=sentence,
                model='text-moderation-latest'
            )
            answer.append(1 if result.results[0].flagged else 0)

        print(answer)
        self.AI_Devs.answer(answer)
