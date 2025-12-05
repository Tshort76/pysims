import argparse
import sys

import toml
import ovulation.model.concealed_ovulation as m


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Concealed Ovulation ABM")
    parser.add_argument(
        "config_file",
        nargs="?",
        default="configs/default_config.toml",
        help="Path to the TOML configuration file (default: config.toml)",
    )
    args = parser.parse_args()

    try:
        print(f"Loading configuration from: {args.config_file}")
        configs = toml.load(args.config_file)

        print(configs)

        model = m.ConcealedOvulationModel(configs)

        steps = configs["simulation"]["n_steps"]
        print(f"Running simulation for {steps} steps...")

        for _ in range(steps):
            model.step()

        results = model.datacollector.get_model_vars_dataframe()
        print("\nFinal Results (Last 5 Steps):")
        print(results.tail())

        print("\nSimulation Complete.")

    except FileNotFoundError:
        print(f"Error: Configuration file '{args.config_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
