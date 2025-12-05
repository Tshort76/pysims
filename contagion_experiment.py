import mesa
import toml
import argparse
import sys

# --- Agent Class ---


class HumanAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(model)
        self.state = "Susceptible"  # States: Susceptible, Infected, Recovered

    def step(self):
        self.move()

        if self.state == "Infected":
            self.infect_others()
            self.try_to_recover()

    def move(self):
        # 1. Get possible neighboring cells (Moore neighborhood includes diagonals)
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        # 2. Pick one and move there
        new_position = self.model.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def infect_others(self):
        # 1. Get other agents in the same cell
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        # 2. Try to infect susceptible cellmates
        infection_rate = self.model.config["virus"]["infection_probability"]

        for mate in cellmates:
            if mate.state == "Susceptible":
                if self.model.random.random() < infection_rate:
                    mate.state = "Infected"

    def try_to_recover(self):
        recovery_rate = self.model.config["virus"]["recovery_probability"]
        if self.model.random.random() < recovery_rate:
            self.state = "Recovered"


# --- Model Class ---


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


# --- Driver Function ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run COVID-19 SIR ABM")
    parser.add_argument("config_file", nargs="?", default="virus_config.toml")
    args = parser.parse_args()

    try:
        print(f"Loading configuration from: {args.config_file}")
        config_data = toml.load(args.config_file)

        model = VirusModel(config_data)
        steps = config_data["simulation"]["n_steps"]

        print(f"Running simulation for {steps} steps...")
        for _ in range(steps):
            model.step()

        # Output results
        results = model.datacollector.get_model_vars_dataframe()
        print("\nFinal Results (Last 5 Steps):")
        print(results.tail())

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
