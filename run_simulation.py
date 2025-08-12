from src.config_loader import ConfigLoader
from src.simulation import Simulation

if __name__ == "__main__":
    config = ConfigLoader("data/config.json")
    sim = Simulation(config)
    final_prob = sim.run(steps=50)
    print(f"Final collision probability: {final_prob:.4f}")
