import mesa
from contagion.agent.human import HumanAgent

class VirusModel(mesa.Model):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.running = True

        # 1. Setup Spatial Grid (MultiGrid allows multiple people in one cell)
        width = config["grid"]["width"]
        height = config["grid"]["height"]
        self.grid = mesa.space.MultiGrid(width, height, torus=True)

        # 2. Setup Data Collection
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Susceptible": lambda m: self.count_state(m, "Susceptible"),
                "Infected": lambda m: self.count_state(m, "Infected"),
                "Recovered": lambda m: self.count_state(m, "Recovered"),
            }
        )

        # 3. Create and Place Agents
        num_agents = config["simulation"]["n_agents"]
        init_infected = config["virus"]["initial_infected_fraction"]

        for i in range(num_agents):
            a = HumanAgent(f"Person_{i}", self)

            # Infect a random fraction initially
            if self.random.random() < init_infected:
                a.state = "Infected"

            self.agents.add(a)

            # Place agent on a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

    @staticmethod
    def count_state(model, state_name):
        """Helper to count agents in a specific state."""
        count = 0
        for agent in model.agents:
            if agent.state == state_name:
                count += 1
        return count
