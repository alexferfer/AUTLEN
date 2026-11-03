"""AUTLEN 2026/27 - Práctica 1.

Integrantes: COMPLETAR
Completa los patrones y las sustituciones. Añade una explicación breve de cada uno.
Pruebas: python3 -m unittest -v test_p1
"""

# Ejemplo: cadenas no vacías sobre {a,b} que empiezan por a.
RE0 = r"a[ab]*"

# 1. Número impar de ceros.
RE1 = r"1*01*(01*01*)*"
# 2. Sin dos unos consecutivos; se admite la cadena vacía.
RE2 = r"(0|10)*1?"

# 3. Importes con signo opcional y parte decimal opcional de dos cifras.
RE3 = r"[+-]?(0|[1-9][0-9]*)(,[0-9]{2})?"

# 4. Archivos nombre_apellido.txt o .csv, con datos/ opcional.
RE4 = r""

# 5. hh:mm:ss; grupos: hora, minutos, segundos.
RE5 = r""

# 6. rgb(r,g,b); grupos: rojo, verde, azul.
RE6 = r""

# 7. Cada secuencia de espacios/tabuladores se sustituye por un espacio.
RE7 = r""
SUB7 = r""

# 8. Cadena completa apellido, nombre -> nombre apellido.
RE8 = r""
SUB8 = r""
