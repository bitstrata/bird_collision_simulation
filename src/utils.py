import matplotlib.pyplot as plt
import pandas as pd

def plot_results(results, output_path="collision_results.png"):
    """Plot aggregated results from parallel simulations."""
    collisions = [df["Collisions"] for df in results]
    avg_collisions = pd.concat(collisions, axis=1).mean(axis=1)
    plt.figure(figsize=(10, 5))
    plt.plot(avg_collisions, label="Average Collisions")
    plt.xlabel("Step")
    plt.ylabel("Number of Collisions")
    plt.title("Bird-Turbine Collision Simulation")
    plt.legend()
    plt.savefig(output_path)
    plt.close()