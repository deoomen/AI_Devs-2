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

    answer = llm.invoke(
        [
            SystemMessage(content='Answer questions as truthfully as you can. If you don\'t know the answer, say with single character "?" and nothing more. Be strict. Use short answer'),
            HumanMessage(content=question)
        ]
    ).content

    logging.info('Answer is: {}'.format(answer))

    return answer
