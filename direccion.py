import re
from difflib import SequenceMatcher

class StringModification():
    
    @staticmethod
    def similar(a, b)-> float:
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def del_acentos(name)->str:
        if not re.search(r"á|à|ä|â|é|è|ë|ê|í|ì|ï|î|ó|ò|ö|ô|ú|ù|ü|û]",name, flags=re.IGNORECASE):
            return name
        
        name= re.sub(r"[á|à|ä|â]", "a", name)
        name= re.sub(r"[é|è|ë|ê]", "e", name)
        name= re.sub(r"[í|ì|ï|î]", "i", name)
        name= re.sub(r"[ó|ò|ö|ô]", "o", name)
        name= re.sub(r"[ú|ù|ü|û]", "u", name)

        # CAPITALIZE
        name= re.sub(r"[Á|À|Ä|Â]", "A", name)
        name= re.sub(r"[É|È|Ë|Ê]", "E", name)
        name= re.sub(r"[Í|Ì|Ï|Î]", "I", name)
        name= re.sub(r"[Ó|Ò|Ö|Ô]", "O", name)
        name= re.sub(r"[Ú|Ù|Ü|Û]", "U", name)
        return name
    
    @staticmethod
    def del_nexos(name):
        '''
        >>> del nexos("Calle Rodriguez de la Fuente")
        >>> "RodriguezFuente"
        '''
        return re.sub(r"^(del?|l[a|o]s?)\b", " ", name, flags=re.IGNORECASE).strip()
    
    @staticmethod
    def del_comas(name):
        '''
        >>> del comas("Calle Rodriguez de la Fuente, 50")
        >>> "Calle Rodriguez de la Fuente 50"
        '''
        return re.sub(r",", "", name, flags=re.IGNORECASE).strip()
    
    @staticmethod
    def del_avenue(direc:str)->tuple:
        '''
        Si existe el nombre de una via, esta se separa del nombre
        
        param. direc-> direccion en formato str que se desea separar la via

        >>> del_avenue('pradera del Panizo 59')
        >>> ('AVENIDA', 'pradera del Panizo 59')
        
        >>> del_avenue('Panizo 59')
        >>> (None, 'Panizo 59')
        '''
        vias= (
        ('ARROYO', 'ARR'),
        "ALAMEDA",
        "AUTOVIA",
        ('AVENIDA', 'AV', 'AVD'),
        "BARRANCO",
        ('BARRIO', 'BO', 'B'),
        ('CAMPILLO', 'CAMP'),
        ('CALLE', 'C', 'C/', 'CL'),
        "CALLEJA",
        ('CERRILLO', 'CERR'),
        "CAMINO",
        "CAMPAMENTO",
        ('ENSANCHE', 'ENS'),
        ('CARRERA', 'CARR'),
        ('CARRETERA', 'CTRA', 'CARRET'),
        ('INTERIOR', 'INT'),
        "CASERIO",
        "COLONIA",
        "CONJUNTO",
        ('COSTANILLA', 'COST'),
        ('PRADERA', 'PRAD'),
        ('PRETIL', 'PRET'),
        "ESCALINATA",
        ('RAMBLA', 'RBLA'),
        ('RIBERA', 'RIB'),
        "FINCA",
        "GALERIA",
        ('GLORIETA', 'GTA'),
        "GRUPO",
        "JARDIN",
        "LUGAR",
        "PARAJE",
        "PARQUE",
        "PARTICULAR",
        ('PASADIZO', 'PZO'),
        ('PASAJE', 'PJE', 'PJ'),
        ('PASEO', 'PS'),
        "PISTA",
        ('PLAZA', 'PZA', 'PL', 'PLZA','PZ'),
        "PLAZUELA",
        "POBLADO",
        "POLIGONO",
        "PROLONGACION",
        ('PUENTE', 'PTE'),
        "PUERTA",
        "RINCON",
        "RINCONADA",
        ('RONDA', 'RDA'),
        "ROTONDA",
        "SECTOR",
        "SENDA",
        "SITIO",
        "SUBIDA",
        ('TRAVESIA', 'TR'),
        "URBANIZACION",
        ('VEREDA', 'VER', 'VDA'),
        "ZONA",
        )
        
        AZ= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        via_letter= direc[0]
        via= direc.split(' ')[0]
        az_pos= AZ.index(via_letter)
        
        # Ordenar la lista de palabras que comience buscando una coincidencia en aquellas sitios que tenga la misma letra
        AZ= AZ[az_pos:] + AZ[:az_pos]
        vias= sorted(vias,key= lambda x: AZ.index(x[0][0]))

        for names in vias:
            if via in names:
                # uso del $ para conocer la ultima posicion y separar la via del tipo de via
                type_via = names[0]
                via = direc.removeprefix(via).lstrip()+ Direccion.LAST_CHR
                via = re.sub(r"^(de l[a|o]s?|del?)\b\s",'', via, flags=re.IGNORECASE)
                return type_via, via 
        return None,direc.lstrip()+ Direccion.LAST_CHR
                 



class Direccion(object):
    '''
    Analiza la direccion que se pase por parametro y la separa en sus correspodientes partes.
    Para el correcto funcionamiento de esta clase, la dirección debe cumplir con:
            (OPCIONAL)      tipo de via
            (OBLIGATORIO)   nombre de la via
            (OBLIGATORIO)   número del edificio
            (OPCIONAL)      Numero o letra de bloque


    Ej.
        >>> dir= 'Calle Marqués de Viana 59 2ºC'
        >>> calle= Direcciones(dir)

        >>> calle           # MARQUES DE VIANA 59
        >>> calle.streets   # ['MARQUES DE VIANA 59]
        >>> calle.type_via  # CALLE
        >>> calle.via       # MARQUES DE VIANA
        >>> calle.num       # 59
        >>> calle.es        # None
        >>> calle.pl        # 2
        >>> calle.pt        # C



    '''
    street_sep="-"
    num_sep=","
    comu_sep="_"   
    ORDER= ('_type_via',"_via","_num","_es","_pl","_pt") 
    LAST_CHR= '$'
    string= StringModification()

    def __init__(self, direccion:string, warning= True)-> None:
        direccion = direccion.strip()
        self._magic= []
        self._warning= warning
        self._original= direccion
        self._type_via= None
        self._via= None
        self._num= []
        self._es= None
        self._pl= None
        self._pt= None

        self._parts= {}
        self._streets= []
        self._all_direc= []
        self._children= []
        
        
        if Direccion.street_sep in direccion: # En caso de que en una direccion aparezcan varios nombre de vias separados con "-" se procede a separar
            self._separate_dir()
            # VER QUE DEBEMOS METER AQUI

        else: #Solo cuando se trate de una unica via
            self._direccion= direccion
            self._del_comu()        # Eliminar nombre del edificio "{EDIFICIO NAME}_{VIA NAME}"
            self._del_acentos() 
            self._upper_dir()       

            self._parser_address() #Most important
            
            if isinstance(self._num,list):
                value= ",".join(self._num)
                self._parts['_num']=value
            if len(self._num)==1:
                self._num= self._num[0]
            elif len(self._num)==0:
                self._num= None
        
        #si _streets esta vacio quiere decir que en la direccion solo se esta pasando una unica direccion (no hay '-') por tanto ._streets estara siempre vacia
        if self._streets:
            self._all_direc= [calle for dir in self._streets for calle in dir._children]
        else:
            
            self._all_direc= self._children            
    
    def __str__(self) -> string:
        return self.strformat


    @property
    def strformat(self):
        if self._magic:
            return self.pretiffy_dir()
        else:
            return self.street

    @property
    def streets(self):
        return self._all_direc
    
    @property
    def street(self):
        if (num:=len(self._all_direc))>1 and self._warning:
            print(f'\nWarning: No solo existe una calle, se está devolviendo únicamente la priemra calle de una lista con {num} calles\n\t Utiliza mejor el controlador de acceso .streets\n\n')
        return self._all_direc[0]

    @property
    def parts(self):
        return {x[1:]:y for x,y in self._parts.items()}

    @property
    def type_via(self):
        self._magic.append('_type_via')
        return self

    @property
    def via(self):
        self._magic.append('_via')
        return self

    @property
    def num(self):
        self._magic.append("_num")
        return self

    @property
    def es(self):
        self._magic.append("_es")
        return self

    @property
    def pl(self):
        self._magic.append("_pl")
        return self

    @property
    def pt(self):
        self._magic.append("_pt")
        return self

    #GETTERS
    def get_type_via(self): return self._type_via
    def get_via(self): return self._via
    def get_num(self): return self._num
    def get_es(self): return self._es
    def get_pl(self): return self._pl
    def get_pt(self): return self._pt

    def _del_acentos(self):
        self._direccion = self.string.del_acentos(self._direccion)
        return self

    def _del_comu(self):     
        if Direccion.comu_sep in self._direccion:
            self._direccion= self._direccion.split(Direccion.comu_sep)[-1]
            return self
    
    def _upper_dir(self)->object:
        self._direccion= self._direccion.upper()
        return self

    def _separate_dir(self) -> object:
        split_dir= self._original.split(self.street_sep)
        for x in split_dir:
            calles= Direccion(x.strip())
            self._streets.append(calles)
            
        return self
    
    def _parser_address(self) -> None:
        '''
        Utilizando la direccion original, la separa en diferentes partes

            -self._type_via -> str
            -self._via -> str
            -self._num -> str
            -self._es -> str
            -self._pl -> str
            -self._pt -> str

        Agrega a self._children aquellas direcciones en caso de que existan
        Las direcciones que se agregan a self._children son unicas, solo tiene un numero, una escalera, una puerta...
        '''
       
        def search_items(x, text) ->re:
            '''
            Busca un patron en funcion de la palabra que se pase
            Ej.
            >>> search_items('ES','MARIA BLAZQUEZ 44 ES:2')
            >>> "2"
            '''
            pattern= rf"(?<=\s{x}[\W?])(\d+|\w+)"
            return re.compile(pattern).search(text)

        #separar de la direccion original, el tipo de via del resto de la direccion
        self._type_via, address= Direccion.string.del_avenue(self._direccion)

        # ENCONTRAR EL TIPO DE VIA Y SEPARARLA
        if self._type_via:
            self._parts['_type_via']= self._type_via

        # ENCONTRAR VIA Y SEPARARLA
        #seek_via= re.search(rf'^([\w\s?]+)(?=\W?\s?(\{Direccion.LAST_CHR}|\d|ES|PL|PT))', address)
        seek_via= re.search(rf'^([A-Z\'\,?\s?]+)(?=\W?\s?(\{Direccion.LAST_CHR}|(N[ºª])?\s?\d|PL|ES|PT))', address)
        if seek_via:
            self._via= self.string.del_comas(seek_via.group(1).strip())
        else: 
            self._via= self.string.del_comas(address.strip(Direccion.LAST_CHR))
        self._parts['_via']= self._via

        #Encontrar el o los numeros de la via
        #Search devuelve la primera coincidencia por eso no ponemos mas restricciones
        num_address= address[len(self._via):]
        first_num= re.search(r"(\d+)", num_address)
        # Si lo encuentra quiere decir que la direccion tiene un numero de calle
        if first_num:
            num_ini= first_num.start()
            #num_fin encuentra solo numeros que les anteceda una ',' si no lo encuentra, quiere decir que solo hay un numero
            num_fin= re.search(rf"(?<={Direccion.num_sep})(\d+)(?=\W?[\s{Direccion.LAST_CHR}])",num_address)
            #num_fin= [x for x in re.finditer(rf"(?<={Direccion.num_sep})(\d+)",new_address)][-1]
            if num_fin:
                num_fin= num_fin.end()
            else:
                num_fin= first_num.end()
            self._num= num_address[num_ini:num_fin].split(Direccion.num_sep)
        else:
            self._num= []

        
        # ENCONTRAR ESCALERA Y SEPARARLA
        seek_es= search_items('ES', address)
        if seek_es:
            self._es= self.parser_char(seek_es.group(1))
            self._parts['_es']= f"ES:{self._es}"
        
        
        FOUND_SECOND= lambda: re.search(r"(\d+)[ºª]\s?([A-Z]+|\d+)", address)

        # ENCONTRAR PLANTA Y SEPARARLA
        seek_pl= search_items('PL', address) 
        seek_pl_2= FOUND_SECOND()
        if seek_pl:
            self._pl= self.parser_char(seek_pl.group(1))
            self._parts['_pl']= f"PL:{self._pl}"
        elif seek_pl_2:
            self._pl= self.parser_char(seek_pl_2.group(1))
            self._parts['_pl']= f"PL:{self._pl}"
         

        
        # ENCONTRAR PUERTA Y SEPARARLA
        seek_pt= search_items('PT', address)
        seek_pt_2= FOUND_SECOND()
        if seek_pt:
            self._pt= self.parser_char(seek_pt.group(1))
            self._parts['_pt']= f"PT:{self._pt}"
        elif seek_pt_2:
            self._pt= self.parser_char(seek_pt_2.group(2))
            self._parts['_pt']= f"PT:{self._pt}"
        

        # Si tiene algun numero la calle, se procede a separar cada numero en diferentes direcciones
        # SE HACE AL FINAL PORQUE ES NECESARIO RECORRER EL RESTO DE PARTES DE LA DIRECCION PARA ESTRUCTURARLO BIEN  
        # NECESITAMOS CONOCER SI TIENE O NO BLOQUE, PLANTA O PUERTA
        if self._num:
            for x in self._num:
                temp:dict= self._parts
                temp['_num']= x
                new_dir= " ".join([temp[x] for x in Direccion.ORDER if x in temp])
                self._children.append(new_dir)
        else:
            new_dir= " ".join([self._parts[x] for x in Direccion.ORDER if x in self._parts])
            self._children.append(new_dir)
        return None

    def pretiffy_dir(self):

        new= []
        #creamos variable temporal ya que vamos a eliminar valores de la lista
        temp= self._magic[::]
        for name_attr in temp:
            if hasattr(self,name_attr):
                value= getattr(self,name_attr)
                if value != None:
                    #si nos encontramos mas de un numero en la direccion
                    new.append(self._parts[name_attr])
            self._magic.remove(name_attr)
        if new:
            return " ".join(new)
        else:
            return 

    @staticmethod
    def parser_char(obj:str) ->str:
        pattern = re.compile(r"\d+")
        if len(obj) > 1 or not pattern.match(obj):
            return obj
        
        return str(f"{int(obj):02d}")
        





if __name__== "__main__":
    dir= 'CL ALCALA GALIANO 3 Pl:03 Pt:A'
    dir2= '    C/ ALCALÁ GALIANO, Nº 3, 3º,'
    calle= Direccion(dir)
    calle2= Direccion(dir2)
    print(calle.via.num.strformat)
    print(calle2.via.num.strformat)