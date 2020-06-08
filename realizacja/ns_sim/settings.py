"""
These are adjustable parameters of the simulation.
Here you should define constants and parameters of the environment, e.g. road-cell size, time step etc.
"""
import queue


class Config:
    """
    Config class variables should be default parameters
        of the simulation when none are set by the user
    """
    D_CELL_SIZE = 7  # meters
    D_TIME_STEP = 1  # seconds
    D_VISIBILITY = 30  # CELL_SIZEs
    D_SIMULATION_DURATION = 50  # TIME_STEPs
    D_SIM_START_TIME = 0
    D_SIM_DAYTIME_PHASES = [(0, 0.025)]  # contains tuples of (phase_starting_time, phase_spawn_chance_modifier)

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
        self.sim_start_time = kwargs.get(
            "sim_start_time") if "sim_start_time" in kwargs else Config.D_SIM_START_TIME  # time of day (in seconds) at which simulation starts
        self.sim_daytime_phases = kwargs.get("sim_daytime_phases") if "sim_daytime_phases" in kwargs else Config.D_SIM_DAYTIME_PHASES
        self.simulation_duration = kwargs.get(
            "simulation_duration") if "simulation_duration" in kwargs else Config.D_SIMULATION_DURATION

    def __str__(self):
        return f"Cell size: {self.cell_size}\nTime step: {self.time_step}\nStarting at: {self.sim_start_time}\nDuration: {self.simulation_duration}\nPhases: {self.sim_daytime_phases}"