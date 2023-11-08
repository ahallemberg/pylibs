class Table:
    """
    Klasse for å representere en tabell som kan printes ut i python
    """

    def __init__(self, columnNames: list[str], dataset: list[list[str]], padding: int = 5, divider: bool = False, frame: bool = False) -> None: 
        """
        Initialiser Table klassen 

        Parameters
        ----------
        columnNames : list[str]
            liste med navn på hver kolonne

        dataset : list[list[str]]]
            2d liste med tabell data hvor hver liste representerer en rad, og hver verdi i listen en kolonne\n

        padding : int, optional
            Antall mellomrom mellom hver kolonne noe som gir en padding effekt
        
        divider : bool, optional
            Om raddeler  skal være med
        
        frame: bool, optional
            Om ramme skal være med
        
        Raises
        ------
        IndexError
            Hvis antall kolonner gitt fra lengden av columnNames, ikke stemmer med antall kollonner i dataset. Dvs at hver liste i 2d lista dataset, må ha samme lengde og være like lang som columnNames

        Examples
        -------
        >>> table = Table(["Kolonne1", "Kolonne2", "Kolonne3"], [["10", "20", "30"], ["40", "50", "60"], ["70", "80", "90"]], divider = True, frame = True)
        >>> print(table)
        ┌────────────────────────────────────┐
        │ Kolonne1     Kolonne2     Kolonne3 │ 
        │ ════════     ════════     ════════ │ 
        │ 10           20           30       │ 
        │ ────────     ────────     ──────── │ 
        │ 40           50           60       │ 
        │ ────────     ────────     ──────── │ 
        │ 70           80           90       │ 
        └────────────────────────────────────┘  
        """

        self.__columnNames = columnNames 
        self.__dataset = dataset
        self.__padding = padding
        self.__frame = frame
        self.__divider = divider
        self.__string = ""
    
        for data in self.__dataset: # looper gjennom dataset altså hver rad, og sjekker om antallet verdier i listen, altså kolonner, samsvarer med antallet kolonnenavn
            if(len(data) != len(self.__columnNames)):
                raise IndexError("Antall kolonner stemmer ikke med lengden av dataset")

    def __getColumnLengths(self) -> list[int]:
        """
        Metode for å kalkulere lengste string i hver kolonne

        Returns
        -------
        list[int]
            Liste med tallene for lengste string i hver kolonne
        """
        cindex = 0 # kolonne index
        columnLengths: list[int] = [] # liste med lengden på lengste tekst hver kolonne
        while cindex < len(self.__columnNames): # looper gjennom hver kolonne
            columnLength = len(self.__columnNames[cindex]) # setter kolonnelengde til lengden av navnet på kolonnen
            for data in self.__dataset: # looper gjennom hver rad
                if len(data[cindex]) > columnLength: # sjekker om lengden av teksten i neste rad i kolonnen er størst
                    columnLength = len(data[cindex]) # setter lengden av kolonnen til den lengste tesktene i kolonnen
            
            columnLengths.append(columnLength) # legger til lengden av gitt kolonne til liste med lengder av alle kolonnene
            cindex+=1 # legger til 1 slik at lengden av neste kolonne beregnes

        return columnLengths 

    def __hoizontalFrame(self, columnLengths: list[int], isTop: bool) -> None:
        """
        Metode for å legge til ramme i hosisontal retning

        Parameters
        ----------
        columnLengths : int
            Liste med bredden til hver kolonne

        isTop : bool
            Om det er border top eller bottom som blir lagt til
        """
        self.__string += " "
        if isTop:
            self.__string += "┌"
        else:
            self.__string += "└"

        for _ in range(sum(columnLengths) + (len(columnLengths)- 1) * self.__padding + 2): # legger til dash for sumen av bredden til alle kolonnene pluss padding mellom de pluss 2 for å få border til å gå ett hakk ut på hver side
            self.__string += "─"

        if isTop:
            self.__string += "┐"
            self.__string +=  "\n"
        else:
            self.__string += "┘"

    def __rowDivider(self, columnLengths: list[int], sepSymbol: str) -> None:
        """
        Metode for å legge til en raddeler

        Parameters
        ----------
        columnLengths : int
            Liste med bredden til hver kolonne

        sepSymbol : bool
            symbol som skal brukes for å separere rader
        """

        if self.__frame: 
            self.__string += " │ "

        for cindex, length in enumerate(columnLengths): # looper gjennom lengden av hver kolonne
            if cindex == len(columnLengths) - 1: # hvis siste kolonne
                self.__string += sepSymbol * length # legg til symbolet like mange ganger som lengden av kolonnen
            else:
                self.__string += (sepSymbol * length).ljust(length + self.__padding) # legg til symbolet like mange ganger som lengden av kolonnen og legg til padding

        if self.__frame:
            self.__string += " │ \n"

        else: 
            self.__string += "\n"

    def __addRow(self, row: list[str], columnLengths: list[int], lastRow: bool, sepSymbol: str|None = None) -> None:
        """
        Metode for å legge til rad
        
        Parameters
        ----------
        row : list[str]
            Data for rad som skal legges til

        columnLengths : int
            Liste med bredden til hver kolonne

        sepSymbol : bool
            symbol som skal brukes for å separere rader
        """

        if self.__frame:
            self.__string += " │ "
        
        for cindex in range(len(row)): # looper gjennom hver kolonne index i raden
            if cindex < len(row) - 1: # alle kolonner bortsett fra siste
                self.__string += row[cindex].ljust(columnLengths[cindex] + self.__padding) # juster teksten slik at den tar opp hele kolonnen og legg til padding mellom hver kolonne
            else: # siste kolonne
                self.__string += row[cindex].ljust(columnLengths[cindex]) # juster teksten slik at den tar opp hele kolonnen men ikke legg til padding

        if self.__frame:
            self.__string += " │ \n"

        elif not lastRow:
            self.__string += "\n"
        
        if self.__divider: 
            if sepSymbol:
                self.__rowDivider(columnLengths, sepSymbol) # hvis divider er satt til True og sepSymbol er gitt, legg til raddeler

    
    def __str__(self) -> str: 
        """
        Returnerer string representasjonen av objektet
        """
 
        columnLengths = self.__getColumnLengths() # Liste med kalkulert lengden på lengste string i hver kolonne
        
        if self.__frame: # hvis frame skal være med
            self.__hoizontalFrame(columnLengths, True) # legg til hosisontal frame for toppen

        self.__addRow(self.__columnNames, columnLengths, False, "═") # legger til raden med kolonnenavn
        [self.__addRow(row, columnLengths, True) if index == len(self.__dataset) - 1 else self.__addRow(row, columnLengths, False, "─") for index, row in enumerate(self.__dataset)] # looper gjennom hver rad i dataset og legger til

        if self.__frame: # hvis frame skal være med
            self.__hoizontalFrame(columnLengths, False) # legg til hosisontal frame for bunnen

        return self.__string # returner string representasjonen for objektet