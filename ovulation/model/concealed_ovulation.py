import mesa
import ovulation.agent.female as women
import ovulation.agent.male as men


class ConcealedOvulationModel(mesa.Model):
    def __init__(self, config):
        super().__init__()

        self.config = config
        self.running = True

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "AvgMaleInvestment": lambda m: sum(
                    a.investment_resources for a in m.agents if isinstance(a, men.MaleAgent)
                )
                / m.config["simulation"]["n_agents"],
                "TotalFemaleSuccess": lambda m: sum(
                    a.offspring_success_score for a in m.agents if isinstance(a, women.FemaleAgent)
                ),
            }
        )

        sim_conf = self.config["simulation"]
        soc_conf = self.config["social"]

        num_agents = sim_conf["n_agents"]
        concealed_frac = soc_conf["concealed_fraction"]

        # Create Female Agents
        for i in range(num_agents):
            a = women.FemaleAgent(f"F{i}", self)
            # Determine logic based on fraction
            a.is_ovulation_concealed = i < num_agents * concealed_frac
            self.agents.add(a)

        # Create Male Agents
        for j in range(num_agents, 2 * num_agents):
            m = men.MaleAgent(f"M{j}", self)
            self.agents.add(m)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
