"""Recolecta comentarios desde un CSV sintético o desde una página autorizada.
No evita autenticación, CAPTCHA ni restricciones de acceso de ningún sitio.
"""
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "datos"
DEFAULT_INPUT = DATA_DIR / "comentarios_sinteticos.csv"
DEFAULT_OUTPUT = DATA_DIR / "comentarios.csv"


def copiar_csv(origen: Path, destino: Path) -> int:
    if not origen.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {origen}")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with origen.open("r", encoding="utf-8-sig", newline="") as src:
        reader = csv.DictReader(src)
        if not reader.fieldnames or "comentario" not in reader.fieldnames:
            raise ValueError("El CSV debe contener una columna llamada 'comentario'.")
        rows = list(reader)
    with destino.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["id", "fecha_recoleccion_utc", "fuente", "comentario"])
        writer.writeheader()
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for i, row in enumerate(rows, 1):
            writer.writerow({"id": row.get("id") or i, "fecha_recoleccion_utc": now,
                             "fuente": row.get("fuente") or "conjunto_sintetico", "comentario": row.get("comentario", "").strip()})
    return len(rows)


def recolectar_web(url: str, selector: str, destino: Path) -> int:
    """Usa Selenium solo en páginas cuyo acceso automatizado esté permitido."""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
    except ImportError as exc:
        raise RuntimeError("Selenium no está instalado. Instale dependencias con: pip install -r requirements.txt") from exc
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        texts = [el.text.strip() for el in driver.find_elements(By.CSS_SELECTOR, selector) if el.text.strip()]
    finally:
        driver.quit()
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["id", "fecha_recoleccion_utc", "fuente", "comentario"])
        writer.writeheader()
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for i, text in enumerate(texts, 1):
            writer.writerow({"id": i, "fecha_recoleccion_utc": now, "fuente": url, "comentario": text})
    return len(texts)


def main():
    parser = argparse.ArgumentParser(description="Recolección ética de comentarios sobre transporte público.")
    parser.add_argument("--url", help="URL de una página que permita explícitamente la recolección automatizada")
    parser.add_argument("--selector", default="article, .post, .comment", help="Selector CSS de los comentarios")
    parser.add_argument("--entrada", type=Path, default=DEFAULT_INPUT, help="CSV de comentarios (modo local)")
    parser.add_argument("--salida", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    count = recolectar_web(args.url, args.selector, args.salida) if args.url else copiar_csv(args.entrada, args.salida)
    print(f"[OK] Comentarios procesados: {count}")
    print(f"[OK] Archivo generado: {args.salida}")
    print("[INFO] Modo: web autorizado" if args.url else "[INFO] Modo: conjunto sintético; no son publicaciones reales")

if __name__ == "__main__":
    main()
