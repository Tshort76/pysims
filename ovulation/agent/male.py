import mesa


class MaleAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(model)
        self.sex = "male"
        self.is_investing = False
        self.investment_resources = 0

        self.configs = self.model.config["behavior"]

    def decide_to_invest(self, concealed):
        if concealed:
            certainty = self.configs["paternity_certainty_concealed"]
        else:
            certainty = self.configs["paternity_certainty_overt"]

        if certainty > self.configs["investment_threshold"]:
            self.investment_resources += 1
            return True
        return False

    def step(self):
        if self.is_investing:
            self.investment_resources += self.configs["investment_increment"]
