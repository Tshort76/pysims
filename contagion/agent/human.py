import mesa

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