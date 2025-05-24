# memory/memory_module.py

class AgentMemory:
    def __init__(self):
        self.memory = {
            "CitizenBot": [],
            "BusinessBot": [],
            "PoliticianBot": [],
            "ActivistBot": [],
            "JournalistBot": [],
            "JudgeBot": []
        }

    def get_memory(self, agent_name):
        return self.memory.get(agent_name, [])

    def add_to_memory(self, agent_name, message):
        if agent_name in self.memory:
            self.memory[agent_name].append(message)
        else:
            self.memory[agent_name] = [message]

    def clear_all(self):
        for key in self.memory:
            self.memory[key] = []
