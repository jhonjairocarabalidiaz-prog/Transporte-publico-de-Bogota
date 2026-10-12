"""Genera propuestas orientativas a partir de frecuencias clasificadas."""
import argparse
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT = BASE_DIR / "resultados" / "analisis.json"
OUTPUT = BASE_DIR / "resultados" / "propuestas.json"


def generar_propuestas(analisis: dict, umbral: int = 3) -> list[dict]:
    frecuencias = analisis.get("frecuencias", {})
    propuestas = []
    reglas = {
        "espera": ("Evaluar un ajuste de frecuencia en las franjas señaladas y contrastarlo con datos operativos.", "Alta"),
        "ocupacion": ("Revisar aforo y distribución de demanda; considerar refuerzos piloto en periodos pico.", "Alta"),
        "congestion": ("Analizar tiempos de recorrido y coordinación semafórica con la autoridad competente.", "Media"),
        "informacion": ("Mejorar la comunicación de horarios, cambios y tiempos estimados en canales oficiales.", "Media"),
        "seguridad": ("Remitir puntos reportados al equipo de seguridad para evaluación y seguimiento.", "Alta"),
    }
    for categoria, (accion, prioridad) in reglas.items():
        cantidad = int(frecuencias.get(categoria, 0))
        if cantidad >= umbral:
            propuestas.append({"categoria": categoria, "menciones": cantidad, "prioridad": prioridad, "propuesta": accion})
    if not propuestas:
        propuestas.append({"categoria": "general", "menciones": 0, "prioridad": "Exploratoria", "propuesta": "Ampliar la muestra antes de priorizar cambios operativos."})
    return propuestas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrada", type=Path, default=INPUT)
    parser.add_argument("--salida", type=Path, default=OUTPUT)
    parser.add_argument("--umbral", type=int, default=3)
    args = parser.parse_args()
    if not args.entrada.exists():
        raise FileNotFoundError(f"No existe {args.entrada}. Ejecute primero analisis.py")
    data = json.loads(args.entrada.read_text(encoding="utf-8"))
    propuestas = generar_propuestas(data, args.umbral)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps(propuestas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Propuestas generadas: {len(propuestas)} (umbral={args.umbral})")
    for p in propuestas:
        print(f"  - [{p['prioridad']}] {p['categoria']} ({p['menciones']} menciones): {p['propuesta']}")
    print(f"[OK] Resultado guardado: {args.salida}")

if __name__ == "__main__":
    main()
