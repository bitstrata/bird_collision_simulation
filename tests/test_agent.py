import pytest
from src.agents import Agent

def test_agent_moves_and_loses_energy():
    agent = Agent(pos=(0,0), energy=10)
    agent.move((1,0))
    assert agent.pos == (1,0)
    assert agent.energy == 9

def test_agent_dies_when_energy_zero():
    agent = Agent(pos=(0,0), energy=1)
    agent.move((1,0))
    assert not agent.alive
