"""Clasificación exploratoria de comentarios con spaCy y reglas transparentes."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
import spacy

BASE_DIR = Path(__file__).resolve().parent
INPUT = BASE_DIR / "datos" / "comentarios.csv"
OUTPUT = BASE_DIR / "resultados" / "analisis.json"
CATEGORIAS = {
    "espera": ["espera", "demora", "tarde", "frecuencia", "tiempo", "minutos", "fila"],
    "ocupacion": ["lleno", "llena", "ocupado", "ocupada", "congestionado", "aforo", "hacinamiento"],
    "congestion": ["tráfico", "trafico", "trancón", "trancon", "congestión", "congestion", "atasco", "demorado"],
    "informacion": ["información", "informacion", "aviso", "ruta", "horario", "aplicación", "aplicacion", "mapa"],
    "seguridad": ["seguridad", "robo", "inseguro", "inseguridad", "acoso", "iluminación", "iluminacion"],
}


def cargar_modelo():
    """Prioriza el modelo español completo; si no está disponible, usa el pipeline base español."""
    try:
        return spacy.load("es_core_news_sm"), "es_core_news_sm"
    except OSError:
        nlp = spacy.blank("es")
        return nlp, "spacy.blank('es') (respaldo; sin modelo entrenado ni NER)"


def clasificar(texto: str, nlp=None) -> list[str]:
    normalizado = texto.casefold()
    if nlp is not None:
        # Procesa el texto con spaCy; la clasificación por palabras clave facilita la reproducibilidad.
        nlp(texto)
    encontradas = [cat for cat, palabras in CATEGORIAS.items() if any(p in normalizado for p in palabras)]
    return encontradas or ["otros"]


def analizar(entrada: Path, salida: Path) -> dict:
    if not entrada.exists():
        raise FileNotFoundError(f"No existe {entrada}. Ejecute primero recoleccion.py")
    nlp, modelo = cargar_modelo()
    with entrada.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    detalles, frecuencias = [], Counter()
    for row in rows:
        texto = row.get("comentario", "").strip()
        categorias = clasificar(texto, nlp)
        frecuencias.update(categorias)
        detalles.append({"id": row.get("id", ""), "comentario": texto, "categorias": categorias})
    resultado = {"modelo_nlp": modelo, "total_comentarios": len(rows), "frecuencias": dict(frecuencias), "comentarios": detalles,
                 "nota": "Clasificación exploratoria por palabras clave; puede asignar varias categorías a un comentario."}
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    return resultado


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrada", type=Path, default=INPUT)
    parser.add_argument("--salida", type=Path, default=OUTPUT)
    args = parser.parse_args()
    r = analizar(args.entrada, args.salida)
    print(f"[OK] Comentarios analizados: {r['total_comentarios']}")
    print(f"[INFO] Pipeline spaCy: {r['modelo_nlp']}")
    print("[RESULTADOS] Frecuencias por categoría:")
    for categoria, cantidad in sorted(r["frecuencias"].items(), key=lambda x: (-x[1], x[0])):
        print(f"  - {categoria}: {cantidad}")
    print(f"[OK] Resultado guardado: {args.salida}")

if __name__ == "__main__":
    main()
