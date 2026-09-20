"""
generar_reto.py — Genera el reto/frase del dia para la clase y lo guarda
en reto.json, que index.html lee para mostrarlo.

No hay datos personales de nadie: solo un texto corto pensado para
ninos de unos 10 anos, pensado para que la profesora lo lea o proyecte
en clase.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

DIR = Path(__file__).parent
SALIDA = DIR / "reto.json"

PROMPT = """Genera UN solo reto o frase para reflexionar, pensado para ninos
y ninas de unos 10 anos en una clase de primaria en Espana. Alterna cada dia
entre dos tipos, elige uno:

- Un reto de comportamiento concreto y realizable en un dia (ej: "hoy
  ayuda a alguien sin que te lo pida", "hoy intenta aprender el nombre de
  alguien que no conoces bien").
- Una frase corta para reflexionar en grupo, simple y positiva, sin
  sonar a sermon de adulto.

Reglas:
- Maximo 2 frases cortas, lenguaje sencillo y calido, nada infantil de mas
  ni cursi.
- Nunca repitas el mismo tema dos dias seguidos si puedes evitarlo.
- No menciones religion, politica, ni nada que necesite contexto de un
  dia en concreto.
- Responde SOLO con el texto final, sin comillas, sin explicaciones, sin
  markdown.
"""


def generar_texto() -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Aviso: no hay ANTHROPIC_API_KEY, uso un texto de respaldo.", file=sys.stderr)
        return "Hoy: sé amable con alguien sin que te lo pidan."

    client = Anthropic(api_key=api_key)
    resp = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=200,
        messages=[{"role": "user", "content": PROMPT}],
    )
    for bloque in resp.content:
        if bloque.type == "text":
            return bloque.text.strip()
    return "Hoy: sé amable con alguien sin que te lo pidan."


def main() -> None:
    texto = generar_texto()
    fecha = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    SALIDA.write_text(
        json.dumps({"fecha": fecha, "texto": texto}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[{fecha}] {texto}")


if __name__ == "__main__":
    main()
