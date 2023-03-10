"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    initial_wolf_energy = 10
    initial_sheep_energy = 4

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_sheep=100,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=False,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
        initial_wolf_energy=10,
        initial_sheep_energy=4
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.initial_wolf_energy = initial_wolf_energy
        self.initial_sheep_energy = initial_sheep_energy

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
                "Energy_per_wolf" : lambda m: m.schedule.get_energy_count(Wolf) / (m.schedule.get_breed_count(Wolf)+1),
            }
        )

        for i in range (initial_sheep):
            pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))
            self.create_sheep(pos)
        
        for i in range (initial_wolves):
            pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))
            self.create_wolf(pos)

        for x in range (width):
            for y in range (height):
                self.create_grass((x,y))
                pass
            
        # Create sheep:
    def create_sheep(self,pos):
        a = Sheep(self.next_id(), pos, self, True, energy =  self.initial_sheep_energy)
        self.schedule.add(a)
        self.grid.place_agent(a, pos)

        # Create wolves
    def create_wolf(self,pos):
        a = Wolf(self.next_id(), pos, self, True, energy =  self.initial_wolf_energy)
        self.schedule.add(a)
        self.grid.place_agent(a, pos)

        # Create grass patches
    def create_grass(self,pos):
        a = GrassPatch(self.next_id(), pos, self, fully_grown = True, countdown = 0)
        self.schedule.add(a)
        self.grid.place_agent(a, pos)

    def step(self):
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        for x in range(step_count):
            self.step()