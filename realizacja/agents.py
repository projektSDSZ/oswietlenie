class Vehicle:
    def __init__(self, **kwargs):
        """

        :param kwargs:
        """

        '''
        WYJAŚNIENIA
        --> Słowniki argumentów ułatwią zmianę ilości parametrów jakie 
            przyjmuje konstruktor. Jeżeli na którymś etapie 
            zechcemy wyrzucić lub dodać jakieś pole to wystarczy
            dopisać/usunąć linijkę typu self.xyz = kwargs.get("xyz")...
        '''

        self.pos = kwargs.get("x") if "x" in kwargs else 0  # current position x(t)
        self.vel = kwargs.get("v") if "v" in kwargs else 0  # current velocity v(t)
        self.acc = kwargs.get("a") if "a" in kwargs else 0  # current acceleration a(t)

        self.behav = kwargs.get("behav") if "behaviour" in kwargs else 0.  # probability of taking a sudden random,
        # the human element, e.g. braking out of fear

        self.dest = kwargs.get("dest") if "dest" in kwargs else 0  # destination, number of possible sinks that agent
        # will ignore before choosing the one through
        # which he leaves
