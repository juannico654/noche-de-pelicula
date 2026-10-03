# 🎬 Noche de Película

App Android hecha en Python + Kivy para elegir películas en pareja.

## Funciones
- Sorteo aleatorio entre películas no vistas.
- Filtro por productora.
- Biblioteca completa en modal.
- Marcar películas como vistas/pendientes.
- Agregar películas propias.
- Puntuación independiente de Nicolás y Jaeline (1–5 estrellas).
- Persistencia local en Android mediante JSON.
- Código separado por modelos, datos, servicios y UI.

## Ejecutar en PC
```bash
python -m pip install kivy==2.3.1
python main.py
```

## Generar APK
En Linux:
```bash
python -m pip install buildozer
buildozer -v android debug
```
El APK queda en `bin/`.
