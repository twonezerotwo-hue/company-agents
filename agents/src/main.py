from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

class SampleAgent: 
    def __init__(self):
        self.agent = Agent(
            role="Developer",
            goal="Help with coding tasks",
            backstory="You are a helpful developer"
        )
    
    def run(self, task_description):
        return f"Task completed: {task_description}"

if __name__ == "__main__": 
    agent = SampleAgent()
    result = agent.run("Test task")
    print(result)
