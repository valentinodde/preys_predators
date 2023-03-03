from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep
import os


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    if type(agent) is Sheep:
        portrayal["Color"] = "white"
        portrayal["r"] = 0.5
        portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/sheep.png"
    

        # ... to be completed

    elif type(agent) is Wolf:
        portrayal["Color"] = "black"
        portrayal["r"] = 0.5
        portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/wolf.png"

    elif type(agent) is GrassPatch:
        portrayal["Shape"] = "rect" 
        portrayal["h"] = 1
        portrayal["w"] = 1
        if agent.fully_grown:
            portrayal["Color"] = "rgb(19,109,21)"
            portrayal["Shape"] = f"{os.path.dirname(os.path.realpath(__file__))}/grass2.png"


        else:
            portrayal["Color"] = "rgb(55,217,128)"

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}],
    #[{"Label": "Energy_per_wolf", "Color": "#AA0000"}],
    data_collector_name='datacollector'
)

model_params = {"initial_wolves": UserSettableParameter("slider", "Initial wolves", 10, 1, 100, 1),
                "initial_sheep": UserSettableParameter("slider", "Initial sheep", 30, 1, 100, 1),
                "initial_wolf_energy": UserSettableParameter("slider", "Initial wolf Energy", 10, 1, 100, 1),
                "initial_sheep_energy": UserSettableParameter("slider", "Initial sheep Energy", 4, 1, 100, 1),
                "grass_regrowth_time": UserSettableParameter("slider", "Grass regrowth time", 30, 1, 100, 1),
                "sheep_gain_from_food": UserSettableParameter("slider", "Sheep gain from food", 4, 1, 100, 1),
                "wolf_gain_from_food": UserSettableParameter("slider", "Wolf gain from food", 20, 1, 100, 1),
                "wolf_reproduce": UserSettableParameter("slider", "Wolf reproduce rate", 0.05, 0, 1, 0.01),
                "sheep_reproduce": UserSettableParameter("slider", "Sheep reproduce rate", 0.04, 0, 1, 0.01),}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
