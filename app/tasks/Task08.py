class Task08:
    '''
    Task 08 - functions
    '''

    AI_Devs = None

    def __init__(self, AI_Devs) -> None:
        self.AI_Devs = AI_Devs

    def run(self) -> None:
        print('Task 08 - functions')
        self.AI_Devs.authorize('functions')

        task = self.AI_Devs.getTask()
        print('The task is:', task)

        functionDefinitionAddUser = {
            'name': 'addUser',
            'description': 'This function will add new user',
            'parameters': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'First name of user',
                    },
                    'surname': {
                        'type': 'string',
                        'description': 'Last name of user',
                    },
                    'year': {
                        'type': 'integer',
                        'description': 'Year of birth of user',
                    },
                }
            }
        }
        self.AI_Devs.answer(functionDefinitionAddUser)
