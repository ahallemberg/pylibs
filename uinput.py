class ExitInputState(Exception):
    pass

class ExitProgram(Exception):
    pass

class Init:
    """
    Klasse for å initalisere module
    """
    commands: dict[str, Exception] = {}

    @staticmethod
    def setCommands(commands: dict[str, Exception]) -> None:
        """
        Static method for å sette ulike kommandoer som raise gitt exception ved input

        Parameters
        ----------
        commands : dict[str, ExitInputState|ExitProgram]
            dict med key-value-pairs hvor key er hvilken input fra bruker som raiser gitt exception gitt som value
        """
        newDict: dict[str, Exception] = {} # lager ny dict for commands
        for cmd, exception in commands.items(): # looper gjennom key-value-pairs i dict
            if not issubclass(exception, Exception): # sjekker om riktig exception er gitt
                raise TypeError("Value i commands dict må være av typen Exception")

            if not isinstance(cmd, str): # sjekker om cmd er string
                raise TypeError("key i commands dict må være str")
            
            newDict[cmd.lower()] = exception # setter key-value-pair for dict

        Init.commands = newDict # setter commands til newDict

class Input:
    """
    Klasse for å be om og manipulere data fra bruker

    Properties
    ----------
    int : int
        Input fra bruker som int
    float : float
        Input fra bruker som int
    str: str 
        Input fra bruker som str

    Methods
    -------
    cases(dict[int, list[str]])
        Get case for brukerinput
   
    """

    def __init__(self, inputText: str = "", strictMode: bool = False, inputErrorMsg: str = "Uglydig input", checkForCommands: bool = True) -> None:

        """
        Initialiser input klasse

        Parameters
        ----------
        inputText: str, optional
            Tekst som skrives til konsoll før input
        
        strictMode: bool, optional
            True: programmet skal raise ValueError exception når bruker taster ugyldig input
            False: programmet ber bruker om å taste input inn på nytt

        inputErrorMsg: str, optional
            Tekst som blir skrevet til bruker før bruker blir spurt om å taste inn input på nytt hvis strictMode er satt til False
        """
    
        self.__inputText = inputText # text som blir printet før input
        self.__strictMode = strictMode # om strictMode
        self.__inputErrorMsg = inputErrorMsg # error msg on exception hvis strictMode er False
        self.__checkForCommands = checkForCommands # om det skal sjekkes for spesielle kommandorer gitt fra Init.commands fra input for brukeren
    

    def __input(self) -> str:
        """
        Metode for å be om input fra bruker

        Returns
        -------
        str
            formatted user input
        """

        if self.__checkForCommands:
            return self.__checkCommands(self.__format(input(self.__inputText)))

        else: 
            return self.__format(input(self.__inputText))
            

    def __format(self, string: str) -> str:
        """
        Metode for å formatere text. Gjør til lowercase og fjerner whitespace

        Parameters
        ----------
        string : str
            string som skal formateres

        Returns
        -------
        str
            formatted text
        """

        return string.lower().strip()


    def __checkCommands(self, inputFromUser: str) -> str:
        """
        Metode for å sjekke om input fra bruker er en gitt kommando hvis Init.setCommands er kalt

        Parameters
        ----------
        inputFromUser : str
            input fra bruker

        Returns
        -------
        str
            samme string som inputFromUser param
        
        Raises
        ------
        Gitt Exception i Init.setCommands hvis input fra bruker stemmer med en kommando 
        """

        for cmd, exception in Init.commands.items(): # looper gjennom key-value-pairs i Init.commands for å sjekke om inputFromUser er lik en av kommandoene og rais da exception
            if inputFromUser == cmd:
                raise exception 

        return inputFromUser # hvis ikke exception ble raised, return inputFromUser    


    def case(self, cases: dict[int|str, list[str]]) -> int|str:
        """
        Returner case (int|str) for bruker input

        Parameters
        ----------
        cases: dict[int, list[str]]
            Dictionary for ulike caser ut fra input
        
        Returns
        -------
        int|str
            Tallet på case som matcher input

        Raises
        ------
        ValueError
            Hvis strictMode er True, og bruker taster inn input som ikke stemmer med noen av casene
        
        Examples
        --------
        >>> Input("Hva er din favorittmatrett? ").case({1: ["Taco", "Burrito", "Enchilada"], 2: ["Lasagne", "Pasta", "Pizza"], 3: ["Paella", "Gazpacho", "Paella"]})
        >>> pizza
        3
        """

        for key, valueList in cases.items(): # looper gjennom key-value-pairs i cases
            newList = [] # ny liste for case values 
            for value in valueList: # looper gjennom hver value i valueList
                newList.append(self.__format(value)) # legger til formatert value til newList
            
            cases[key] = newList # oppdaterer values for key til newList

        if self.__strictMode == True: # strict mode, ikke catch ValueError
            return getCase(self.__input(), cases)

        else: # ikke strict mode, catch ValueError og be bruker på nytt          
            while True:
                try:
                    return getCase(self.__input(), cases)

                except ValueError:
                    print(self.__inputErrorMsg)

    @property
    def int(self) -> int:
        """
        Integer value av input

        Raises
        ------
        ValueError
            Hvis strictMode er True og input fra bruker ikke kan konverteres til int
        """

        if self.__strictMode: # strict mode, ikke catch ValueError
            return int(self.__input())

        else: # ikke strict mode, catch ValueError og be bruker på nytt
            while True:
                try:
                    return int(self.__input())

                except ValueError:
                    print(self.__inputErrorMsg + ". Må kunne konverteres til int")

    @property
    def float(self) -> float:
        """
        Float value av input

        Raises
        ------
        ValueError
            Hvis strictMode er True og input fra bruker ikke kan konverteres til float
        """

        if self.__strictMode: # strict mode, ikke catch ValueError
            return float(self.__input())
            
        else: # ikke strict mode, catch ValueError og be bruker på nytt
            while True:
                try:
                    return int(self.__input())

                except ValueError:
                    float(self.__inputErrorMsg + ". Må kunne konverteres til float")
    
    @property
    def str(self) -> str:
        """
        String value av input
        """

        return self.__input()


def getCase(matchText: str, cases: dict[int|str, list[str]]) -> int|str:
    """
    Funksjon for å returnere key på case hvis matchText stemmer overens med en av verdiene i casene

    Parameters
    ----------
    cases: dict[int, list[str]]
        Dictionary for ulike caser ut fra matchText
        
    Returns
    -------
    int|str
        Tallet på case som matcher input

    Raises
    ------
    ValueError
        Hvis matchText ikke stemmer overens med noen av casene
    """

    for key, values in cases.items(): # looper gjennom caser
        if matchText in values: # sjekker om bruker input matcher en av de godkjente verdiene til casene
            return key # returnerer key på case

    raise ValueError("matchText stemmer ikke overens med noen av casene")