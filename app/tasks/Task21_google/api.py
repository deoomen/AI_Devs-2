import sys
import logging
from flask import Flask, jsonify, request
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from serpapi import GoogleSearch

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

    search_phrase = llm.invoke(
        [
            SystemMessage(
                content=(
                    'Rephrase user input that it can be written in Google to find website address. Be strict, use only keywords. Do not add anything.'
                    'User input will be in polish.'
                    'Examples:'
                    '###'
                    'User: Gdzie mogę sprawdzić aktualny kurs dolara?'
                    'AI: kursy walut'
                    'User: Szukam adresu strony na której mogę zapisać się na newsletter Adama Nowaka?'
                    'AI: Adam Nowak newsletter'
                    '###'
                )
            ),
            HumanMessage(content=question)
        ]
    ).content
    logging.info('Search phrase: {}'.format(search_phrase))

    search = GoogleSearch({
        "q": search_phrase,
        "location": "Warsaw,Poland",
        "api_key": os.getenv('SERP_API_KEY')
    })
    answer = search.get_dict()['organic_results'][0]['link']

    logging.info('Answer is: {}'.format(answer))

    return answer
