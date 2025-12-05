import mesa


class FemaleAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(model)

        bio_conf = self.model.config["biology"]
        self.cycle_len = bio_conf["cycle_length"]
        self.fertile_day = bio_conf["fertile_day"]
        self.is_ovulation_concealed = False  # Will be set during creation

        self.cycle_day = self.model.random.randint(1, self.cycle_len)
        self.offspring_success_score = 0
        self.partner_id = None
        self.sex = "female"

    def step(self):
        self.cycle_day = (self.cycle_day % self.cycle_len) + 1
        is_fertile = self.cycle_day == self.fertile_day

        if is_fertile:
            rivalry_penalty = 0
            if not self.is_ovulation_concealed:
                rivalry_penalty = self.model.config["social"]["rivalry_cost_factor"]

            potential_mate = self.model.random.choice(self.model.agents)

            if potential_mate.sex == "male":
                self.mate(potential_mate, rivalry_penalty)

    def mate(self, male, penalty):
        if male.decide_to_invest(self.is_ovulation_concealed):
            base = self.model.config["biology"]["base_offspring_success"]
            final_success = base * (1 - penalty)
            self.offspring_success_score += final_success
            male.is_investing = True
            self.partner_id = male.unique_id
