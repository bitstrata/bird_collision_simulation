import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from shapely.geometry import Point
import geopandas as gpd

def visualize(simulation, steps=50, save_path=None):
    """
    Animate agents and turbines over time.
    
    Args:
        simulation: Simulation object
        steps: Number of steps to run and visualize
        save_path: If given, saves animation as mp4
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Turbine positions
    turbines = simulation.turbines.gdf
    turbine_x = [pt.x for pt in turbines.geometry]
    turbine_y = [pt.y for pt in turbines.geometry]
    ax.scatter(turbine_x, turbine_y, c='red', s=100, marker='^', label='Turbines')

    # Agent positions
    agent_positions = [(agent.pos[0], agent.pos[1]) for agent in simulation.agents]
    scat = ax.scatter([x for x, y in agent_positions],
                      [y for x, y in agent_positions],
                      c='blue', s=20, alpha=0.6, label='Agents')

    ax.set_title("Bird Collision Simulation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.set_aspect('equal', 'box')

    def update(frame):
        simulation.step()
        alive_positions = [(agent.pos[0], agent.pos[1]) for agent in simulation.agents if agent.alive]
        scat.set_offsets(alive_positions)
        ax.set_title(f"Step {frame+1}/{steps} | Alive: {len(alive_positions)}")
        return scat,

    anim = FuncAnimation(fig, update, frames=steps, interval=200, blit=True)
    
    if save_path:
        anim.save(save_path, writer='ffmpeg', fps=5)
    plt.show()
