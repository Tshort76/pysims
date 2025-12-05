import argparse
import logging
import logging.config
import sys

import toml
from contagion.model.virus import VirusModel

# Configure logging
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run COVID-19 SIR ABM")
    parser.add_argument("config_file", nargs="?", default="configs/contagion_config_000.toml")
    args = parser.parse_args()

    try:
        log.debug(f"Loading configuration from: {args.config_file}")
        config_data = toml.load(args.config_file)

        model = VirusModel(config_data)
        steps = config_data["simulation"]["n_steps"]

        log.debug(f"Running simulation for {steps} steps...")
        for _ in range(steps):
            model.step()

        # Output results
        results = model.datacollector.get_model_vars_dataframe()
        print(f"\nResults (Last 5 Steps):\n\n{results.tail()}")

    except FileNotFoundError:
        log.error(f"Configuration file '{args.config_file}' not found.")
        sys.exit(1)
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
