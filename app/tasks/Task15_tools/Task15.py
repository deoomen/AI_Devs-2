import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from datetime import date
from langchain.chains.structured_output import create_openai_fn_runnable

class Task15:
    '''
    Task 15 - tools
    '''

    AI_Devs = None
    memory = []
    llm = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs
        self.llm = ChatOpenAI(model='gpt-3.5-turbo-0125', openai_api_key=os.getenv('OPENAI_API_KEY'), temperature=0)

    def run(self) -> None:
        print('Task 15 - tools')
        self.AI_Devs.authorize('tools')

        task = self.AI_Devs.getTask()
        print('The task is:', task)
        question = task['question']
        print('The question is:', question)

        messages = [
            SystemMessage(content='Fact: Today is {}'.format(date.today().isoformat())),
            HumanMessage(content=question)
        ]
        structured_llm = create_openai_fn_runnable([ToDo, Calendar], self.llm)
        result = structured_llm.invoke(messages)

        self.AI_Devs.answer(result.run())


class ToDo(BaseModel):
    """Add task to user ToDo list"""

    title: str = Field(description='Task title')

    def run(self) -> dict:
        return {
            "tool": "ToDo",
            "desc": self.title
        }

# class AddTask(BaseTool):
#     args_schema: Type[BaseModel] = ToDo
#     name: str = 'addTask'
#     description: str = 'Add task to user ToDo list'

#     def _run(self, task: str, **kwargs: Any) -> Any:
#         return '{"tool":"ToDo","desc":"{}"}'.format(task)

class Calendar(BaseModel):
    """Add reminder to user calendar"""

    title: str = Field(description='Reminder title')
    date: str = Field(description='Date of event in YYYY-MM-DD format')

    def run(self) -> dict:
        return {
            "tool": "Calendar",
            "desc": self.title,
            "date": self.date
        }

# class AddReminder(BaseTool):
#     args_schema: Type[BaseModel] = Calendar
#     name: str = 'addReminder'
#     description: str = 'Add reminder to user calendar'

#     def _run(self, title: str, date: str, **kwargs: Any) -> Any:
#         return '{"tool":"Calendar","desc":"{}","date":"{}"}'.format(title, date)
