"""Genera gráfico de frecuencias usando resultados/analisis.json."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
entrada = BASE_DIR / "resultados" / "analisis.json"
salida = BASE_DIR / "resultados" / "frecuencias.png"
if not entrada.exists():
    raise FileNotFoundError("Ejecute primero python analisis.py")
data = json.loads(entrada.read_text(encoding="utf-8"))
frecuencias = data.get("frecuencias", {})
items = sorted(frecuencias.items(), key=lambda x: x[1])
fig, ax = plt.subplots(figsize=(9, 5.2))
if items:
    ax.barh([x[0].capitalize() for x in items], [x[1] for x in items])
    for i, (_, value) in enumerate(items):
        ax.text(value + 0.05, i, str(value), va="center")
ax.set_title("Frecuencia de categorías en comentarios sintéticos")
ax.set_xlabel("Menciones (un comentario puede aportar más de una)")
ax.set_ylabel("Categoría")
ax.grid(axis="x", alpha=0.25)
fig.tight_layout()
salida.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(salida, dpi=160, bbox_inches="tight")
print(f"[OK] Gráfico guardado: {salida}")
