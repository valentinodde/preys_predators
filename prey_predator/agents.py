from mesa import Agent
from prey_predator.random_walk import RandomWalker
import random

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.model = model
        #self.pos = pos

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        # handle energy
        self.energy = self.energy - 1
        if self.energy <= 0:
            self.model.remove_agent(self)
            self.model.schedule.remove(self)
            #self.kill_agents.remove(self)
            return

        # move
        self.random_move()

        # eat grass
        agents_cell = self.model.grid.get_cell_list_contents([self.pos])
        for agent in agents_cell:
            if isinstance(agent, GrassPatch):
                if agent.fully_grown:
                    agent.fully_grown = False
                    agent.countdown = self.model.grass_regrowth_time
                    self.energy = self.energy + self.model.sheep_gain_from_food
        test = random.random()

        # reproduce
        if test < self.model.sheep_reproduce:
            self.model.create_sheep(self.pos)
        
        



class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        # move
        self.random_move()

        # eat sheep
        agents_cell = self.model.grid.get_cell_list_contents([self.pos])
        for agent in agents_cell:
            if isinstance(agent, Sheep):
                agent.
                self.energy = self.energy + self.model.wolf_gain_from_food
                break
        test = random.random()

        # reproduce
        if test < self.model.sheep_reproduce:
            self.model.create_sheep(self.pos)


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        # ... to be completed
        self.fully_grown = fully_grown
        self.countdown = countdown

    def step(self):
        # ... to be completed