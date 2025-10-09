import re
import bisect
from pathlib import Path

RUTA = Path("texto.txt")
texto = RUTA.read_text(encoding="utf-8")

# Tokens con nombre
TOKENS = [
    ("COM", r'#.*'),

    #("CADENA", r'"[^"]*"'),
    #("CADENA",   r'"(?P<contenido>[^"]*"'),    
    #("CADENA",   r'"(?P<contenido>[^"\\]*(?:\\.[^"\\]*)*)"'),

    ("KWORD", r'\b(int|for|if|string)\b'),
    #("LIST", r'c'),
    ("NUM", r'-?\d+'),
    ("ID", r'[a-zA-Z_][a-zA-Z0-9_]*'),


    ("ABRE_COM", r'"'),
    ("CIERRA_COM", r'"'),

    ("ABRE_P", r'\('),
    ("CIERRA_P", r'\)'),
    ("SIM_EQ", r'=|<-'),
    ("SIM", r'\+|\-|\*|\/|=|==|!=|<=|>=|<|>|\{|\}|:|;|,|#'),

    ("WS", r'[ \t\n]+'), # Ignorar espacios en blanco
    ("ERR", r'.'),

]

patron = re.compile("|".join(f"(?P<{nombre}>{regex})" for nombre, regex in TOKENS))

line_starts = [0]
for i, ch in enumerate(texto):
    if ch == "\n":
        line_starts.append(i + 1)

def offset_to_line_col(offset: int):
    idx = bisect.bisect_right(line_starts, offset) - 1
    line = idx + 1
    col = offset - line_starts[idx] + 1
    return line, col

errores_encontrados = []


for m in patron.finditer(texto):
    token_type = m.lastgroup
    lexema = m.group()

    if token_type == "WS":
        continue

    # if token_type == "CADENA":
    #     # m.group(0) = "contenido", m.group(1) = contenido sin comillas
    #     contenido = m.group('contenido')

    #     # Posición de la comilla de apertura
    #     open_off = m.start()               # offset de la comilla de apertura
    #     open_line, open_col = offset_to_line_col(open_off)
    #     print(f"Linea {open_line}, Columna {open_col} -> ' \" ' ABRE_COM")

    #     # Posición del contenido: justo después de la comilla de apertura
    #     content_off = open_off + 1
    #     c_line, c_col = offset_to_line_col(content_off)
    #     print(f"Linea {c_line}, Columna {c_col} -> ' {contenido} ' CADENA")

    #     # Posición de la comilla de cierre: último caracter de la coincidencia
    #     close_off = m.end() - 1
    #     close_line, close_col = offset_to_line_col(close_off)
    #     print(f"Linea {close_line}, Columna {close_col} -> ' \" ' CIERRA_COM")

    # else:
    #     # Tokens normales (KWORD, NUM, ID, COM, ABRE_P, CIERRA_P, SIM)
    #     line, col = offset_to_line_col(m.start())
    #     print(f"Linea {line}, Columna {col} -> ' {lexema} ' {token_type}")

    line, col = offset_to_line_col(m.start())

    if token_type == "ERR":
        # Acumula el error en la lista
        errores_encontrados.append((line, col, lexema))
    else:
        # Imprime tokens normales
        print(f"Linea {line}, Columna {col} -> '{lexema}' {token_type}")
    
if errores_encontrados:
    print("\n--- ERRORES DETECTADOS ---")
    for err_line, err_col, err_lexema in errores_encontrados:
        print(f"Linea {err_line}, Columna {err_col} -> '{err_lexema}' ERR")