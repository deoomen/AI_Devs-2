import sys
import logging
from flask import Flask, jsonify, request
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

level = logging.INFO
root = logging.getLogger()
root.setLevel(level)
stdoutFormatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s - [%(module)s/%(filename)s::%(funcName)s:%(lineno)d]')
stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setLevel(level)
stdoutHandler.setFormatter(stdoutFormatter)
root.addHandler(stdoutHandler)

app = Flask(__name__)
llm = ChatOpenAI(model='gpt-3.5-turbo', openai_api_key=os.getenv('OPENAI_API_KEY'), temperature=0)
memory = []

@app.route('/', methods=['GET', 'POST'])
def home():
    logging.info('Method: {}'.format(request.method))
    logging.info('JSON: {}'.format(request.json))

    answer = processQuestion(request.json['question'])
    response = {
        'reply': answer
    }

    return jsonify(response)

def processQuestion(question: str) -> str:
    logging.info('Question is: {}'.format(question))

    # specify question type
    question_type = llm.invoke(
        [
            SystemMessage(
                content=(
                    'Your task is to specify context(question|information) of user input.'
                    'If you don\'t know the answer, say with single character "?" and nothing more.'
                    'All user input will be in polish language.'
                    'Examples:'
                    '###'
                    'User: Jaki jest kurs dolara?'
                    'AI: question'
                    'User: Lubię placki'
                    'AI: information'
                    '###'
                )
            ),
            HumanMessage(content=question)
        ]
    ).content
    logging.info('Type: {}'.format(question_type))

    if question_type == 'question':
        answer = llm.invoke(
            [
                SystemMessage(content=(
                    'Answer questions as truthfully as you can. Extend your knowledge using the context below. If you don\'t know the answer, say with single character "?" and nothing more. Be strict. Use short answer.'
                    'Context:$$${}$$$'.format(' '.join(memory))
                )),
                HumanMessage(content=question)
            ]
        ).content
    elif question_type == 'information':
        memory.append('Użytkownik powiedział: "{}".'.format(question))
        answer = 'Ok. Zapamiętane!'
    else:
        raise RuntimeError('Model WTF')

    logging.info('Answer is: {}'.format(answer))

    return answer
