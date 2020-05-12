"""
These are adjustable parameters of the simulation.
Here you should define constants and parameters of the environment, e.g. road-cell size, time step etc.
"""


class Config:
    """
    Config class variables should be default parameters
        of the simulation when none are set by the user
    """
    D_CELL_SIZE = 7  # meters
    D_TIME_STEP = 1  # seconds
    D_VISIBILITY = 30  # CELL_SIZEs
    D_SIMULATION_DURATION = 100  # TIME_STEPs

    def __init__(self, **kwargs):
        """
        Pass a dictionary of arguments, fall back on class
            variables for default values
        """

        '''
        WYJAŚNIENIA
        --> Config to klasa, która będzie służyć do zmiany ustawień
            symulacji

        --> Słowniki argumentów ułatwią zmianę ilości parametrów jakie 
            przyjmuje konstruktor. Jeżeli na którymś etapie 
            zechcemy wyrzucić lub dodać jakieś pole to wystarczy
            dopisać/usunąć linijkę typu self.xyz = kwargs.get("xyz")...
        '''

        self.cell_size = kwargs.get("cell_size") if "cell_size" in kwargs else Config.D_CELL_SIZE  # meters
        self.time_step = kwargs.get("time_step") if "time_step" in kwargs else Config.D_TIME_STEP  # seconds
        self.visibility = kwargs.get("visibility") if "visibility" in kwargs else Config.D_VISIBILITY  # CELL_SIZEs
        self.simulation_duration = kwargs.get(
            "simulation_duration") if "simulation_duration" in kwargs else Config.D_SIMULATION_DURATION
