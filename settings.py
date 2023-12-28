import json, os
from pylibs.uinput import Input 


class NotInitializedError(Exception):
    """
    Exception som kan bli raised hvis Settings objekt må ha blitt initialisert før en gitt metode kalles
    """
    pass


class NotInitializedJSONFileError(Exception):
    """
    Exception som kan bli raised hvis Settings objekt må ha blitt initialisert for JSON fil før en gitt metode kalles
    """
    pass


class Settings:
    """
    Klasse for å lage et settings objekt for å tracke ulike settings og lagre de
    """

    def __init__(self) -> None:
        self.__initialized: bool = False
        self.__initializedJSONFile: bool = False
        self.__json_path: str = ""


    def init(self, settings: dict[str, dict[str, object]]) -> None:
        """
        Metode for å initialisere hvilke settings objektet skal tracke

        Parameters
        ----------
        settings : dict[str, dict[str, object]]
            Dictionary med hvilke innstillinger som objektet skal tracke
            Key til key-value-pair dict er navnet på instillingen som skal trackes, og kan senere brukes som key for .get og .set metode. 
            Value i key-value-pair må også være et dict med keys "default_value" for standardverdi, og "options" for alle mulige verdiene for instillingen. Ønsker du at 
            en option skal returnere f.eks en referanse til en funksjon bruker du en dict med key for navnet på option og value som return verdi 
        
        Raises
        ------
        TypeError
            Hvis typen av settings param ikke er dict og hvis value i key-value-pairs i settings ikke er av typen dict
        
        ValueError
            Hvis settings param ikke har riktig format

        Examples
        -------
        >>> settings = Settings()
        >>> settings.init(
            {
                "img_size": {"default_value": "large", "options": [{"large": refToLargeFunc},{"medium": refToMediumFunc},{"small": refToSmallFunc}]},
                "volume_level": {"default_value": 5 , "options": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
                "toggle": {"default_value": True , "options": [True, False]},
            }
        ) 
        """

        if type(settings) != dict: # sjekker om settings param ikke er av riktig type
            raise TypeError(f"settings param må være av typen dict ikke {type(settings)}")

        self.__settings: dict[str, dict[str, object]] = dict()
        for key, value in settings.items():
            if type(value) != dict: # sjekker om verdien av key-value pair i settings ikke er av riktig type
                raise TypeError(f'Verdien av key-value pairs må være av typen dict for settings param ikke {type(value)} for key "{key}"')
            
            if "default_value" not in value.keys(): # sjekker om key med default_value mangler
                raise ValueError(f'Dictionary for key "{key}" må ha en key-value-pair med key "default_value" for å fastsette en standardverdi')
            
            if "options" not in value.keys(): # sjekker om key med options mangler
                raise ValueError(f'Dictionary for key "{key}" må ha en key-value-pair med key "options" for å fastsette hvilke verdier instillingen "{key}" kan ha')

            if type(value["options"]) != list:
                raise ValueError(f'Typen av "options" i dictionary med key "{key}" må være av typen list ikke {type(value["options"])}')
            
            defaultValuePresentedInOptions = False
            for index, option in enumerate(value["options"]): # type: ignore
                if type(option) == dict: # sjekker om typen av option er dict
                    if len(option) > 1: # sjekker om det er flere enn 1 key-value-pairs
                        raise ValueError(f'Option med index {index} for "{key}" kan være av typen dict men må bare bestå av en key-value-pair hvor key er den lagrede verdien og value er verdien som blir returnert nå .get kalles')
                    
                    if list(option.keys())[0] == value["default_value"]: # key for option er default value
                        defaultValuePresentedInOptions = True
                        break
                    
                    elif list(option.values())[0] == value["default_value"]: # default value er satt til return value for en av option, og ikke key
                        raise ValueError(f'default_value for "{key}" kan være key til option med index {index}, men ikke value, da dette er return verdien for instillingen')
                
                else: # option er ikke dict
                    if option == value["default_value"]: # sjekk om option er default value
                        defaultValuePresentedInOptions = True
                        break
            
            if not defaultValuePresentedInOptions: # default value er ikke presentert i listen med options
                raise ValueError(f'"default_value" med verdi {value["default_value"]} i dictionary med key "{key}" må være representert i "options" som verdi i listen eller som key i en av key-value-pair veriene i listen')
                        
            self.__settings[key] = {"value": value["default_value"], "options": value["options"] } # type: ignore data for gitt key er gyldig så legg til i settings dictionary
                
        self.__initialized = True # setter attribute for initalisation til True da alt gikk vellykket
    

    def initJSONFile(self, json_path: str) -> None:
        """
        Metode for å knytte settings objektet til json fil for å synce instillingene

        Parameters
        ----------
        json_path : str
            path til json fil
        
        Raises
        ------
        NotInitializedError
            Hvis objektet ikke har blit initialiser med .init metoden

        ValueError
            Hvis fil ikke eksisterer med gitt path eller at fil ikke er en json fil for
        """

        if not self.__initialized: # sjekker om objektet ikke er initialisert
            raise NotInitializedError(f"Settings objektet {self} må være initialisert med .init method før .initJSONFile method kan kalles")

        if not os.path.isfile(json_path): # sjekker om det eksisterer en fil med gitt path
            raise ValueError(f'Det finnes ingen fil med path "{json_path}" fra cwd "{os.getcwd()}"')

        if not json_path.endswith(".json"): # sjekker om fil er av typen json
            raise ValueError(f'Filen må være json fil, ikke {json_path.split(".")[-1:]} fil')

        self.__json_path = json_path 
        self.__initializedJSONFile = True
        self.__getStoredSettings() # henter lagrede innstillinger


    def get(self, key: str, literalValue: bool = False) -> object:
        """
        Metode for å hente verdi for key-value-pair

        Parameters
        ----------
        key : str
            key til key-value-pair

        literalValue : bool, optional
            om den faktiske verdien skal returneres eller den verdien som ble satt til return value for option hvis option er av typen dict

        Returns
        -------
        object 
            Verdi eller return value for setting

        Raises
        ------
        NotInitializedError
            Hvis objektet ikke har blit initialiser med .init metoden
        """

        if not self.__initialized: # hvis ikke objektet er initialisert
            raise NotInitializedError(f"Settings objektet {self} må være initialisert med .init method før .get method kan kalles")
        
        if key not in self.__settings.keys(): # sjekker om objektet har key-value-pair med gitt key
            raise KeyError(f'Settings har ikke key-value-pair med key "{key}"')

        if literalValue: # hvis faktiske verdi skal returnees
            return self.__settings[key]["value"]

        for option in self.__settings[key]["options"]: # type: ignore Looper gjennom hver option    
            if type(option) == dict: # hvis option er av typen dict
                if list(option)[0] == self.__settings[key]["value"]: # hvis key til option er samme som verdien i settings med gitt key 
                    return option[self.__settings[key]["value"]] # returner option gitte return value
            
        return self.__settings[key]["value"] # hvis ikke finner option med key lik value, returner vlue

    
    def getOption(self, key: str, index: int, literalValue: bool = False) -> object:
        """
        Metode for å hente verdi til option

        Parameters
        ----------
        key : str
            key til key-value-pair
        
        index : int
            index til option i options list som ble gitt i .init metoden med gitt key

        literalValue : bool, optional
            om den faktiske verdien skal returneres eller den verdien som ble satt til return value for option hvis option er av typen dict
        
        Returns
        -------
        object 
            Verdi eller return value for option

        Raises
        ------
        NotInitializedError
            Hvis objektet ikke har blit initialiser med .init metoden

        IndexError
            hvis index er ute av range til options list
        
        KeyError
            hvis objektet ikke har en key-value-pair med gitt key
        """

        if not self.__initialized: # hvis ikke objektet er initialisert
            raise NotInitializedError(f"Settings objektet {self} må være initialisert med .init method før .getOption method kan kalles")

        if key not in self.__settings.keys(): # sjekker om objektet har key-value-pair med gitt key
            raise KeyError(f'Settings har ikke key-value-pair med key "{key}"')

        try:
            if type(self.__settings[key]["options"][index]) != dict: #  type: ignore Så lenge at typen av option ikke er dict, returner option da option ikke har en annen returnvalue
                return self.__settings[key]["options"][index] # type: ignore
            else:
                return list(self.__settings[key]["options"][index].items())[0][0 if literalValue else 1] # type: ignore Returnerer option key hvis literalValue er true, ellers returnvalue for option

        except IndexError:
            raise IndexError(f'Settings objektet med attribute {key} har ingen option med index {index}. Max index er {len(self.__settings[key]["options"])}') # type: ignore

   
    def set(self, key: str, value: object) -> None:
        """
        Metode for å sette verdi for key-value-pair
           
        Parameters
        ----------
        key : str
            key til key-value-pair
        
        value : object
            verdien som skal bli satt til key-value-pair

        Raises
        ------
        NotInitializedError
            Hvis objektet ikke har blit initialiser med .init metoden

        KeyError
            hvis objektet ikke har en key-value-pair med gitt key

        ValueError
            hvis value param ikke er presentert i options list og dermed ikke er gyldig
        """

        if not self.__initialized: # hvis ikke objektet er initialisert
            raise NotInitializedError(f"Settings objektet {self} må være initialisert med .init methode før .set methode kan kalles")

        if key not in self.__settings.keys(): # sjekker om objektet har key-value-pair med gitt key
            raise KeyError(f'Settings har ikke key-value-pair med key "{key}"')

        validValue = False # om ny verdi er gyldig
        for option in self.__settings[key]["options"]: # type: ignore Looper gjennom hver option i options list
            if type(option) == dict: # hvis option er dict
                if list(option)[0] == value: # sjekker om verdi er lik key til key-value-pair i option
                    validValue = True
                    break

            elif option == value: # sjekker om den nye verdien er lik option
                validValue = True
                break

        if validValue: # hvis den nye verdien er gyldig
            self.__settings[key]["value"] = value # sett ny verdi til verdi
            if self.__initializedJSONFile:
                self.__updateStoredSettings() # oppdater json fil

        else: # ikke gyldig verdi
            raise ValueError(f'Ugyldig verdi for value med key "{key}". Verdi må være {[list(option)[0] for option in self.__settings[key]["options"]] if type(self.__settings[key]["options"][0]) == dict else self.__settings[key]["options"]}') # type: ignore
    

    def resetStoredSettings(self) -> None:
        """
        Metode for å nullstille json fil med instillingene

        Raises
        ------
        NotInitializedJSONFileError
            Hvis objektet ikke har blit initialiser med .initJSONFile metoden
        """
        
        if not self.__initializedJSONFile: # sjekker om initaliser opp mot json file
            raise NotInitializedJSONFileError(f"Settings objektet {self} må være initialisert med .initJSONFile metode før .resetStoredSettings metode kan kalles")

        open(self.__json_path, "w").close() # sletter alt innhold i filen


    def __updateStoredSettings(self) -> None:
        """
        Metode for å oppdatere json fil med data fra objektet

        Raises
        ------
        NotInitializedJSONFileError
            Hvis objektet ikke har blit initialiser med .initJSONFile metoden
        """

        if not self.__initializedJSONFile: # sjekker om initaliser opp mot json file
            raise NotInitializedJSONFileError(f"Settings objektet {self} må være initialisert med .initJSONFile metode før .__updateStoredSettings metode kan kalles")

        try:
            with open(self.__json_path, "w") as f: # åpner fil i write modus
                newDict = dict()  # new dict
                for key, value in self.__settings.items(): # looper gjennom key-value-pais i settings
                    newDict[key] = value["value"] # legger til key-value-pair med gitt key og value for gitt value for instillingen
                
                json.dump(newDict, f) # konverter dict til json string og legger til i fil

        except:
            print(f"Klarte ikke å oppdatere settings til Settings objektet {self} til json fil med path {self.__json_path}")
            raise 
        
    
    def __getStoredSettings(self) -> None:
        """
        Metode for å hente settings fra json fil og synce objektet til det

        Raises
        ------
        NotInitializedJSONFileError
            Hvis objektet ikke har blit initialiser med .initJSONFile metoden
        """

        if not self.__initializedJSONFile: # sjekker om initaliser opp mot json file
            raise NotInitializedJSONFileError(f"Settings objektet {self} må være initialisert med .initJSONFile metode før .__getStoredSettings metode kan kalles")

        try:
            with open(self.__json_path, "r") as f: # åpner fil
                json_str  = f.read() # reads content
                if json_str != "": # så lenge fil ikke er tom
                    settings: dict[str, str] = json.loads(json_str) # parser json string til dict
                    for key, value in settings.items(): # looper gjennom hver key-value-pair
                        try:
                            if value != None: # så lenge value ikke er None
                                self.set(key, value) # sett verdi

                        except (KeyError, ValueError) as e: # handle errors
                            if type(e) == KeyError:
                                print(f'Ugyldig key ("{key}") for key-value-pair data fra json fil {self.__json_path}')

                            else:
                                print(f'Ugyldig verdi {value} med key ("{key}") for key-value-pair data fra json fil {self.__json_path}')

                            if Input(f"Ønsker du å nullstille filen {self.__json_path} slik at nye settings kan bli lagret på riktig måte (y/n)? ").case({1: ["y"], 2: ["n"]}) == 1:
                                self.resetStoredSettings()

        except:
            print(f"Klarte ikke å synce settings til Settings objektet {self} med json fil med path {self.__json_path}")
            raise
