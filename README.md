# Plataforma exploratoria de comentarios sobre transporte público

## Requisitos e instalación

Python 3.10 o superior recomendado. En una terminal, desde esta carpeta:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

Si el entorno no tiene conexión, la instalación de paquetes/modelo puede fallar. `analisis.py` usa un respaldo `spacy.blank('es')` para que el flujo local funcione, pero este respaldo no equivale al modelo entrenado `es_core_news_sm`.

## Ejecución completa

```bash
python recoleccion.py
python analisis.py
python optimizacion.py
python graficar.py
pytest -v
```

El archivo de entrada incluido es sintético y no representa publicaciones reales. Para Selenium, solo use páginas que permitan la automatización y revise sus términos y avisos de privacidad:

```bash
python recoleccion.py --url "https://sitio-autorizado.example/pagina" --selector ".comentario"
```

El selector es un ejemplo y debe ajustarse a la estructura de la página autorizada. Se requiere un controlador de navegador compatible (Selenium Manager puede resolverlo si el entorno permite descargas).

## Salidas

- `datos/comentarios.csv`: comentarios normalizados.
- `resultados/analisis.json`: categorías y frecuencias.
- `resultados/propuestas.json`: recomendaciones preliminares.
- `resultados/frecuencias.png`: gráfico generado desde el análisis.
- `evidencias/`: registros de terminal y capturas PNG creadas a partir de la salida real de ejecución.

## Limitaciones

La clasificación se basa en palabras clave y no comprende bien ironía, contexto, negaciones ni variantes regionales. Un comentario puede pertenecer a varias categorías. Los datos sintéticos sirven para comprobar el flujo técnico, no para concluir cuáles son los problemas reales de Bogotá. Las propuestas requieren validación con datos operativos oficiales, participación ciudadana y evaluación de impacto.
