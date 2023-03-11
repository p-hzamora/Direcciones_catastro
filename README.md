# Direcciones_catastro
Modifica el formato cotidiano con el que se asignan las direcciones de las calles, para ajustarlo al formato de la pagina del catastro.
En otras palabras, analiza la direccion que se pase por parametro y la separa en sus correspodientes partes.

Para el correcto funcionamiento de esta clase, la dirección debe cumplir con:
        (OPCIONAL)      tipo de via
        (OBLIGATORIO)   nombre de la via
        (OBLIGATORIO)   número del edificio
        (OPCIONAL)      Numero o letra de bloque

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
