# PySims - Agent-Based Model Simulations

Agent-Based Model (ABM) simulations built with the Mesa framework for exploring complex social and biological phenomena.

## Overview

This repository contains two independent simulation experiments:

1. **Contagion Experiment**: SIR (Susceptible-Infected-Recovered) epidemic model with spatial dynamics
2. **Ovulation Experiment**: Evolutionary biology simulation exploring concealed vs. overt ovulation strategies

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup

1. Clone the repository:
```bash
git clone git@github.com:Tshort76/pysims.git
cd pysims
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Contagion Experiment

Simulates disease spread on a spatial grid where agents move randomly and can infect nearby susceptible individuals.

```bash
# use the default configs at configs/contagion_config_000.toml
python contagion_experiment.py

# or specify path to configurations file
python contagion_experiment.py configs/contagion_config_000.toml
```

#### Configuration
[configs/contagion_config_000.toml](configs/contagion_config_000.toml):

```toml
[simulation]
n_agents = 200          # Number of agents in the simulation
n_steps = 100           # Total simulation steps to run

[grid]
width = 20              # Grid width
height = 20             # Grid height

[virus]
initial_infected_fraction = 0.5  # Fraction of initially infected agents (0.0 to 1.0)
infection_probability = 0.2      # Probability of infection per contact
recovery_probability = 0.1       # Probability of recovery per step when infected
```

### Ovulation Experiment

Explores the evolutionary dynamics of concealed ovulation through male investment decisions based on paternity certainty.

**Run with default configuration:**
```bash
# use the default configs at configs/ovulation_config_000.toml
python ovulation_experiment.py

# or specify path to configurations file
python ovulation_experiment.py configs/ovulation_config_000.toml
```

#### Configuration
[configs/ovulation_config_000.toml](configs/ovulation_config_000.toml):

```toml
[simulation]
n_agents = 50           # Number of female agents (males = n_agents)
n_steps = 500           # Total simulation steps
random_seed = 42        # Random seed for reproducibility

[biology]
cycle_length = 14       # Length of fertility cycle
fertile_day = 7         # Day of peak fertility in cycle
base_offspring_success = 1.0  # Baseline reproductive success score

[social]
concealed_fraction = 0.5      # Fraction of females with concealed ovulation (0.0 to 1.0)
rivalry_cost_factor = 0.2     # Reproductive penalty for overt females from rivalry

[behavior]
paternity_certainty_overt = 0.8      # Male certainty when ovulation is visible
paternity_certainty_concealed = 0.3  # Male certainty when ovulation is hidden
investment_threshold = 0.4           # Minimum certainty required for male investment
investment_increment = 0.1           # Resource increment per step when investing
```

## Architecture

Both simulations follow the Mesa ABM framework pattern:

- **Model**: Contains the simulation environment, grid/space, agent collection, and data collectors
- **Agents**: Individual entities with behaviors that execute each step
- **Step execution**: Models call `agents.shuffle_do("step")` to randomize agent activation order
- **Data collection**: Mesa's `DataCollector` tracks metrics via lambda functions

## License

See [LICENSE](LICENSE) file for details.
