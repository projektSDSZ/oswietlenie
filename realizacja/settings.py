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

        self.CELL_SIZE = kwargs.get("CELL_SIZE") if "CELL_SIZE" in kwargs else Config.D_CELL_SIZE  # meters
        self.TIME_STEP = kwargs.get("TIME_STEP") if "TIME_STEP" in kwargs else Config.D_TIME_STEP  # seconds
