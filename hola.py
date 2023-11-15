def contiene_todas_las_vocales(palabra):
    vocales = set("aeiou")
    return vocales.issubset(set(palabra.lower()))

# Ejemplo de uso
palabra = "murcielago"
if contiene_todas_las_vocales(palabra):
    print(f"La palabra '{palabra}' contiene todas las vocales.")
else:
    print(f"La palabra '{palabra}' no contiene todas las vocales.")