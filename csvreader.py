import os, csv

class InvalidDataStructure(Exception):
    pass

class CSVReader:
    """
    Klasse for å manipulere CSV-fil

    Properties
    ----------
   
    data_set : list[list[str]]
        Datasettet for csv dataen. 2D liste. 

    headers : list[list[str]]
        Liste med alle headerer for csv data

    ERROR_MODE : int
        Hvor strengt feil med datastrukturen skal rapporteres

    Methods
    -------
    check_for_errors(message)
        Sjekker om oppdatert datastrukturen inneholder feil
    
    validate_data()
        Validerer om datastrukturen er gyldig

    insert_row(row, index)
        Legg til rad i datasettet 
    
    remove_row(index)
        Fjern en rad med gitt index fra datasettet 
    
    get_row(index)
        Hent rad fra datasettet med gitt index fra datasettet 

    insert_column(column, index)
        Legg til kolonne i datasettet 
    
    remove_column(index)
        Fjern en kolonne med gitt index fra datasettet 

    get_column(index)
        Hent kolonne fra datasettet med gitt index fra datasettet 

    get_column_lengths()
        Liste med lengde på lesngste data i hver kolonne 

    write(delimiter)
        Skriv til csv fil kollonnenavn og datasettet
    
    read(delimiter, header)
        Henter data fra csv fil
    
    print()
        Printer ut data til objektet
    """
    __current_dir = os.path.join(os.getcwd(), os.path.dirname(__file__)) # dir path 
    __file_path: str 
    ERROR_MODE_OFF = 0 # Ingen error
    ERROR_MODE_BASIC = 1
    ERROR_MODE_STRICT = 2
    ERROR_MODES = [ERROR_MODE_OFF, ERROR_MODE_BASIC, ERROR_MODE_STRICT]
    __ERROR_MODE: int
    __headers: list[list[str]]
    __data_set: list[list[str]]

    def __init__(self, file_path: str, relative_path: bool = True) -> None:
        """
        Initialiser CSVReader

        Parameters
        ----------
        file_path : str
            Path til csv-fil

        relative_path : bool, optional
            Om path til csv-fil skal være relativ
        """
        self.__ERROR_MODE = self.ERROR_MODE_OFF
        self.__headers = [] 
        self.__data_set = [] 
        
        if relative_path == True: 
            self.__file_path = os.path.realpath(os.path.join(self.__current_dir, file_path)) # abs path til fil ut fra mappe til fil som blir kjørt
        else:
            self.__file_path = file_path # abs path til fil ut fra hva bruker har gitt som param

    @property 
    def ERROR_MODE(self) -> int:
        """
        ERROR_MODE property

        Returns
        -------
        int
        """
        return self.__ERROR_MODE
    
    @ERROR_MODE.setter 
    def ERROR_MODE(self, mode: int) -> None:
        """
        Setter metode for ERROR_MODE property
        """
        if mode not in self.ERROR_MODES: # hvis bruker prøver å sette ERROR_MODE til en ikke godkjent verdi, raise Exception 
            raise ValueError(f"ERROR_MODE kan være {self.ERROR_MODES}, ikke {mode}")
        
        self.__ERROR_MODE = mode

    @property
    def data_set(self) -> list[list[str]]:
        """
        data_set property

        Returns
        -------
        list[list[str]]
        """
        return self.__data_set
    
    @data_set.setter
    def data_set(self, data_set: list[list[str]]) -> None:
        """
        Setter metode for data_set
        """
        self.__data_set = data_set # setter data_set attributen til data_set gitt av bruker
        if self.__ERROR_MODE != self.ERROR_MODE_OFF: # hvis error mode ikke er off
            try:
                self.validate_data() # sjekker om data er gyldig

            except InvalidDataStructure as e: # data er ikke gyldig
                print("Ugyldig data for å oppdatere attributen .data_set")
                if self.__ERROR_MODE == self.ERROR_MODE_BASIC: # printer bare ut feilen hvis error mode er basic
                    print(e)
                else: # raiser exception hvis ikke
                    raise e

    @property
    def headers(self) -> list[list[str]]:
        """
        headers property

        Returns
        -------
        list[list[str]]
        """
        return self.__headers
    
    @headers.setter 
    def headers(self, headers: list) -> None:
        """
        Setter metode for headers
        """
        self.__headers = headers 

        if self.__ERROR_MODE != self.ERROR_MODE_OFF: # hvis error mode ikke er off
            try:
                self.validate_data() # sjekker om data er gyldig

            except InvalidDataStructure as e: # data er ikke gyldig
                print("Ugyldig data for å oppdatere attributen .headers")
                if self.__ERROR_MODE == self.ERROR_MODE_BASIC: # printer bare ut feilen hvis error mode er basic
                    print(e)
                else: # raiser exception hvis ikke
                    raise e
    def __len__(self) -> int:
        """
        Returnerer lengde av data list
        """
        return len(self.data_set)
    
    def validate_data(self) -> None:
        """
        Metode for å validere om data er godkjent
        """
        if len(self.__headers) > 0:
            r_length = len(self.__headers[0])

        elif len(self.__data_set[0]) > 0:
            r_length = len(self.__data_set[0])

        else:
            raise InvalidDataStructure("Ingen kolonnenavn eller datasett gitt")
    
        for index, header in enumerate(self.__headers):
            if len(header) != r_length:
                raise InvalidDataStructure(f"Lengden på header med index {index} stemmer ikke overens med lengden på første header")
        
        for index, row in enumerate(self.__data_set):
            if len(row) != r_length:
                raise InvalidDataStructure(f"Antall kolonner for rad med index {index} stemmer ikke overens med antall kolonner gitt av headers eller første rad")
            
    def check_for_errors(self, message: str) -> None:
        """
        Metode for å sjekke om nylig oppdatert data inneholder feil

        Parameters
        ----------
        message : str 
            Melding som blir printet ved feil hvis ERROR_MODE er på et høyere nivå enn off
        """
        if self.__ERROR_MODE != self.ERROR_MODE_OFF: # hvis error mode ikke er off
            try: 
                self.validate_data()

            except InvalidDataStructure as e: # data er ikke gyldig
                print(message)
                if self.__ERROR_MODE == self.ERROR_MODE_BASIC: # printer bare ut feilen hvis error mode er basic
                    print(e)
                else: # raiser exception hvis ikke
                    raise e
                
    def insert_row(self, row: list[str], index: int) -> None:
        """
        Metode for å legge til en ny rad i datasett

        Parameters
        ----------
        row : list[str]
            Liste med data for raden
        index : int
            Indeks hvor raden skal legges til før
        """

        self.__data_set.insert(index, row)
        self.check_for_errors("Ugyldig data for å legge til ny rad")

    def remove_row(self, index: int) -> None:
        """
        Metode for å fjerne en rad i datasett

        Parameters
        ----------
        index : int
            Indeks hvor raden som skal fjernes
        """
        try:
            self.__data_set.pop(index)

        except IndexError as e: # catcher Index Error og printer ut melding før exception blir raised
            print(f"Ugyldig index for rad. datasettet har {len(self.__data_set)} rad(er)")
            raise e
        
    def get_row(self, index: int) -> list[str]:
        """
        Metode for å hente gitt rad fra datasettet

        Parameters
        ----------
        index : int
            Indeks hvor raden som skal hentes
        """
        if len(self.__data_set) == 0:
            raise IndexError("data_set er tom, og har derfor ingen rader som kan hentes")
        try:
            return self.__data_set[index]
        except IndexError:
            raise IndexError(f"row_index ute av range for data_set")
    
    def insert_column(self, column: list[str], index: int) -> None:
        """
        Metode for å legge til en ny kolonne i headers og dataset

        Parameters
        ----------
        row : list[str]
            Liste med data for raden
        index : int
            Indeks hvor raden skal legges til før
        """
        item_index = 0
        for header in self.__headers:
            header.insert(index, column[item_index])
            item_index += 1
        
        for row in self.__data_set:
            row.insert(index, column[item_index])
            item_index += 1
        
        self.check_for_errors("Ugyldig data for å legge til ny kolonne")
    
    def remove_column(self, column_index: int) -> None:
        """
        Metode for å fjerne en kolonne i datasett

        Parameters
        ----------
        index : int
            Indeks for kolonnen som skal fjernes
        """
        try:
            for header in self.__headers: # looper gjennom hver header 
                header.pop(column_index) # fjerner verdi med column_index
            
            for row in self.__data_set: # looper gjennom hve rad i datasett
                row.pop(column_index)
        
        except IndexError as e: # catcher Index Error og printer ut melding før exception blir raised
            print(f"Ugyldig index for kolonne. datasettet har {len(self.get_column_lengths())} kolonne(r)")
            raise e


    def get_column(self, column_index: int) -> list[str]:
        """
        Metode for å hente gitt kolonne fra datasettet
        
        Parameters
        ----------
        index : int
            Indeks for kolonnen som skal hentes
        """
        if len(self.__data_set) == 0:
            raise IndexError("data_set er tom, og har derfor ingen kolonner som kan hentes")
        try:
            column_list = []
            for row in self.__data_set:
                column_list.append(row[column_index])
            
            return column_list
        except IndexError:
               raise IndexError("column_index ute av range for data_set")
        
    def write(self, delimiter: str = ",") -> None:
        """
        Metode for å skrive til gitt csv-fil med informasjon gitt fra kolonnenavn og datasett
        
        Parameters
        ----------
        delimiter : str, optional
            Kolonnesperator som brukes i csv fil
    
        """
        with open(self.__file_path, "w") as f: # åpner fil i write mode
            csv_writer = csv.writer(f, delimiter=delimiter)
            [csv_writer.writerow(header) for header in self.__headers] # skriver header
            [csv_writer.writerow(row) for row in self.__data_set] # skriver rad

    def read(self, delimiter:str = ",", header: int|list[int]|None = None) -> None:
        """
        Les data fra gitt csv-fil
        
        Parameters
        ----------
        delimiter : str, optional
            Kolonnesperator som brukes i csv fil

        header: int|list[int]|None, optional
            Hvis filen inneholder headere 
        """
        with open(self.__file_path, "r") as f:
            if type(header) == int:
                header = [index for index in range(header)] #type:ignore

            elif header == None:
                header = []
      
            csv_reader = csv.reader(f, delimiter=delimiter) 
            for index, row in enumerate(csv_reader):
                if index in header: #type:ignore
                    self.__headers.append(row)
                else:
                    self.__data_set.append(row)
   

    def get_column_lengths(self) -> list[int]:
        """
        Metode for å hente lengde på kolonner fra dataset
        """
        if len(self.__headers) > 0:
            c_lengths = [0 for _ in range(len(self.__headers[0]))]

        else:
            c_lengths = [0 for _ in range(len(self.__data_set[0]))]
        
        for head in self.__headers:
            for cindex, data in enumerate(head):
                if len(data) > c_lengths[cindex]:
                    c_lengths[cindex] = len(data)
        
        for row in self.__data_set:
            for cindex, data in enumerate(row):
                if len(data) > c_lengths[cindex]:
                    c_lengths[cindex] = len(data)

        return c_lengths

    def print(self) -> None:
        """
        Print ut kolonnenavn og datasettt som tabell
        """
        try:
            self.validate_data()

        except InvalidDataStructure as e:
            print("Kan ikke printe ut data da strukturen ikke stemmer overens")
            raise e
        
        column_lengths = self.get_column_lengths()
        padding = 5

        for header in self.__headers: # printer ut headers
            for index, data in enumerate(header):
                print(f"{data:<{column_lengths[index] + padding}}", end="")
            print("")

        for index, clength in enumerate(column_lengths): # printer ut skiller mellom headers og datasett 
            if index != len(column_lengths) - 1:
                [print("=", end="") for _ in range(clength)]
                print(" "*padding, end="")

            else:
                [print("=", end="") for _ in range(clength)]

        
        print("")
        for row in self.__data_set: # printer ut datasettt
            for index, value in enumerate(row):
                print(f"{value:<{column_lengths[index] + padding}}", end="")

            print("")