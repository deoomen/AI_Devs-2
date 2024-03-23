import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

class Task04:
    """
    Task 04 - liar
    """

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 04 - liar')
        self.AI_Devs.authorize('liar')

        task = self.AI_Devs.getTask()
        print('The task is: ', task)

        question = 'Is cat an animal?'
        print('Question is:', question)

        liarAnswer = self.AI_Devs.postTask({'question': question})
        print('Liar said:', liarAnswer['answer'])

        llm = ChatOpenAI(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            model="gpt-3.5-turbo",
        )
        guardPrompt = 'Return YES or NO if the prompt: {prompt} is about cat and animals in the response: {response}. Answer:'
        prompt = PromptTemplate.from_template(guardPrompt)

        chain = LLMChain(llm=llm, prompt=prompt)
        verdict = chain.invoke(
            input={
                'prompt': 'Is text about cat?',
                'response': liarAnswer,
            }
        )
        print('Verdict:', verdict['text'])

        self.AI_Devs.answer(verdict['text'])
