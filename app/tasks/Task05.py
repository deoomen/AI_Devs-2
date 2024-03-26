import os
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate

class Task05:
    '''
    Task 05 - inprompt
    '''

    AI_Devs = None
    model = 'gpt-3.5-turbo'

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 05 - inprompt')
        self.AI_Devs.authorize('inprompt')

        task = self.AI_Devs.getTask()
        print('The task is:', task['msg'])
        question = task['question']
        print('Question is:', question)
        data = task['input']

        name = self.getName(question)
        filteredData = self.filterData(data, name)
        answer = self.getAnswer(filteredData, question)

        self.AI_Devs.answer(answer)

    def getName(self, question: str) -> str:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    'role': 'system',
                    'content': 'Return only name'
                },
                {
                    'role': 'user',
                    'content': question
                }
            ],
            temperature=1,
            max_tokens=256,
        )

        return response.choices[0].message.content

    def filterData(self, data: dict, name: str) -> dict:
        return [item for item in data if name in item]

    def getAnswer(self, data: dict, question: str) -> str:
        llm = ChatOpenAI(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            model=self.model,
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    (
                        "Answer questions as truthfully using the context below and nothing more. If you don't know the answer, say \"don't know\"."
                        "Separator between context is single |."
                        "context###{}###".format(" | ".join(data))
                    )
                ),
                ('human', '{question}')
            ]
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.invoke(
            input={
                'question': question
            }
        )

        return response['text']
