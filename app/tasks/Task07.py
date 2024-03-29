import os
from requests import get
from openai import OpenAI

class Task07:
    '''
    Task 07 - whisper
    '''

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 07 - whisper')
        self.AI_Devs.authorize('whisper')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role': 'system',
                    'content': '''
You are a tool to fetch URLs from user messages. Return only full valid URL and nothing else. Do not add anything.

Examples:
###
User: hey, this is my site: https://site.com/home
Assistant: https://site.com/home
###
'''
                },
                {
                    'role': 'user',
                    'content': task['msg']
                },
            ]
        )
        recordingUrl = response.choices[0].message.content
        filename = os.path.basename(recordingUrl)

        with get(recordingUrl, stream=False) as response:
            with open(filename, 'wb') as file:
                file.write(response.content)

        audio_file= open(filename, 'rb')
        transcription = client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            language='pl'
        )

        print(transcription.text)
        self.AI_Devs.answer(transcription.text)
