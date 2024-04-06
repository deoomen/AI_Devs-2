import logging
import os
from langchain_openai import OpenAIEmbeddings
from requests import get
import json
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from langchain_community.document_loaders import JSONLoader
from uuid import uuid4

class Task12:
    '''
    Task 12 - search
    '''

    AI_Devs = None
    memory = []
    memoryFile = 'tasks/Task12_search/unknow.news-archiwum_aidevs.json'
    embeddingsModel = None
    collectionName = 'ai_devs'
    qdrant = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs
        self.qdrant = QdrantClient(host='db_vector', port=6333)
        self.embeddingsModel = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))

    def run(self) -> None:
        print('Task 12 - search')
        self.AI_Devs.authorize('search')

        task = self.AI_Devs.getTask()
        print('The task is:', task)
        question = task['question']
        print('The question is:', question)

        # load memory if exist
        if os.path.exists(self.memoryFile):
            with open(self.memoryFile, 'r') as file:
                self.memory = json.load(file)

        # check collection exist
        if False == self.qdrant.collection_exists(self.collectionName):
            self.qdrant.recreate_collection(
                collection_name=self.collectionName,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

        # load collection
        collection = self.qdrant.get_collection(self.collectionName)

        # check points in collection exist
        if 0 == collection.points_count:
            url = task['msg'].split(' - ')[1]
            self.fillCollection(url)

        # find answer for question
        embeddedQuestion = self.embeddingsModel.embed_query(question)
        results = self.qdrant.search(
            collection_name=self.collectionName,
            query_vector=embeddedQuestion,
            limit=1
        )
        article = self.findInMemoryByUuid(results[0].payload['uuid'])

        if article is None:
            logging.error('Answer not found!')
            exit(1)
        else:
            logging.info('Article: {}'.format(article['url']))
            self.AI_Devs.answer(article['url'])

    def getKnowledge(self, knowledgeUrl: str) -> str:
        logging.info('Fetching knowledge...')

        with get(knowledgeUrl) as response:
            if 200 != response.status_code:
                raise RuntimeError('Unexpected http status code: {}'.format(response.status_code))

            return response.text

    def fillCollection(self, url: str) -> None:
        # load data
        knowledge = self.getKnowledge(url)

        # add uuid to data
        self.memory = json.loads(knowledge)

        for item in self.memory:
            item['uuid'] = uuid4().__str__()

        knowledge = json.dumps(self.memory)

        # load docuemnts
        with open(self.memoryFile, 'w') as file:
            file.write(knowledge)

        loader = JSONLoader(
            file_path=self.memoryFile,
            jq_schema='.[].title',
            text_content=False
        )
        documents = loader.load()

        points = []
        embeddingContents = []

        # metadata
        for index in range(0, len(documents)):
            documents[index].metadata['uuid'] = self.memory[index]['uuid']
            embeddingContents.append(documents[index].page_content)

        # embedding
        embeddings = self.embeddingsModel.embed_documents(embeddingContents)

        # prepare points
        for index in range(0, len(documents)):
            points.append(
                PointStruct(
                    id=documents[index].metadata['uuid'],
                    vector=embeddings[index],
                    payload=documents[index].metadata
                )
            )

        # upsert
        self.qdrant.upsert(self.collectionName, points, True)

    def findInMemoryByUuid(self, uuid: str) -> dict|None:
        for item in self.memory:
            if item['uuid'] == uuid:
                return item

        return None
