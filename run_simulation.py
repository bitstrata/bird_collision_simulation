from src.config_loader import ConfigLoader
from src.simulation import Simulation
from visualize_simulation import visualize  # import the above function

if __name__ == "__main__":
    config = ConfigLoader("data/config.json").config
    sim = Simulation(config)
    
    # Run and visualize 50 steps
    visualize(sim, steps=50)
    
    # Final collision probability
    final_prob = sim.prior_prob
    print(f"Final collision probability: {final_prob:.4f}")

