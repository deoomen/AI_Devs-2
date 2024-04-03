# https://scrapfly.io/blog/user-agent-header-in-web-scraping/

from bs4 import BeautifulSoup
from requests import get
from ua_parser import user_agent_parser
from functools import cached_property
from time import time
import random

class UserAgent:
    '''container for a User-Agent'''

    def __init__(self, string) -> None:
        self.string: str = string
        # Parse the User-Agent string
        self.parsed_string: str = user_agent_parser.Parse(string)
        self.last_used: int = time()

    # Get the browser name
    @cached_property
    def browser(self) -> str:
        return self.parsed_string['user_agent']['family']

    # Get the browser version
    @cached_property
    def browser_version(self) -> int:
        return int(self.parsed_string['user_agent']['major'])

    # Get the operation system
    @cached_property
    def os(self) -> str:
        return self.parsed_string['os']['family']

    # Return the actual user agent string
    def __str__(self) -> str:
        return self.string

class Rotator:
    '''weighted random user agent rotator'''

    def __init__(self, scrap: bool = False):
        if scrap is True:
            url = 'https://www.useragentlist.net/'
            request = get(url)
            user_agents = []
            soup = BeautifulSoup(request.text, 'html.parser')
            for user_agent in soup.select('pre.wp-block-code'):
                user_agents.append(user_agent.text)
        else:
            with open('SampleUserAgents.txt', 'r') as file:
                user_agents.append(file.readlines())

        # Add User-Agent strings to the UserAgent container
        user_agents = [UserAgent(ua) for ua in user_agents]
        self.user_agents = user_agents

    # Add weight for each User-Agent
    def weigh_user_agent(self, user_agent: UserAgent):
        weight = 1_000
        # Add higher weight for less used User-Agents
        if user_agent.last_used:
            _seconds_since_last_use = time() - user_agent.last_used
            weight += _seconds_since_last_use
        # Add higher weight based on the browser
        if user_agent.browser == 'Chrome':
            weight += 100
        if user_agent.browser == 'Firefox' or 'Edge':
            weight += 50
        if user_agent.browser == 'Chrome Mobile' or 'Firefox Mobile':
            weight += 0
        # Add higher weight for higher browser versions
        if user_agent.browser_version:
            weight += user_agent.browser_version * 10
        # Add higher weight based on the OS type
        if user_agent.os == 'Windows':
            weight += 150
        if user_agent.os == 'Mac OS X':
            weight += 100
        if user_agent.os == 'Linux' or 'Ubuntu':
            weight -= 50
        if user_agent.os == 'Android':
            weight -= 100
        return weight

    def get(self):
        # Weigh all User-Agents
        user_agent_weights = [
            self.weigh_user_agent(user_agent) for user_agent in self.user_agents
        ]
        # Select a random User-Agent
        user_agent = random.choices(
            self.user_agents,
            weights=user_agent_weights,
            k=1,
        )[0]
        # Update the last used time when selecting a User-Agent
        user_agent.last_used = time()
        return user_agent
