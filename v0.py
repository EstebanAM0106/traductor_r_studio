import re
from pathlib import Path

RUTA = Path("texto.txt")
texto = RUTA.read_text(encoding="utf-8")

# Tokens con nombre
TOKENS = [
    ("KWORD", r'\b(int |for |if |string )\b'),
    ("NUM", r'-?\d+'),
    ("ID", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("ABRE_COM", r'"'),
    ("CADENA", r'"[^"]*"'),
    ("CIERRA_COM", r'"'),
    ("SIM", r'\+|\-|\*|\/|=|==|!=|<=|>=|<|>|\(|\)|\{|\}|;|,'),
    ("WS", r'[ \t\n]+'), # Ignorar espacios en blanco
]

patron = re.compile("|".join(f"(?P<{nombre}>{regex})" for nombre, regex in TOKENS))

for m in patron.finditer(texto):
    token_type = m.lastgroup
    token_value = m.group()
    pos = m.start() + 1  # columna (1-indexed)
    if token_type != "WS":  # ignoramos espacios y saltos de línea
        print(f"Linea 1, Columna {pos} -> ' {token_value} ' {token_type}")

