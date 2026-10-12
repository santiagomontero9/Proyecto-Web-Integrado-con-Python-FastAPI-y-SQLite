# Fortnite Tracker

Proyecto web escolar para registrar jugadores y estadísticas de Fortnite, sin conexión con las cuentas reales ni con Epic Games.

## Problema y objetivo

Se necesita un lugar sencillo para organizar estadísticas de partidas sin usar notas separadas. La aplicación permite guardar, consultar, editar y borrar registros de jugadores y asignarlos a temporadas.

## Tecnologías

- Python + FastAPI: lógica y API REST.
- SQLite: base de datos relacional.
- HTML, CSS y JavaScript: interfaz.
- GitHub: repositorio.
- Vercel: publicación de demostración.

## Ejecutar en Windows desde VS Code

1. Instalá Python 3.12 o superior y abrí la carpeta del proyecto en VS Code.
2. Abrí una terminal en esa carpeta y ejecutá:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Si PowerShell no te deja activar el entorno virtual, podés usar directamente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app:app --reload
```

3. Abrí http://127.0.0.1:8000/ en el navegador. Documentación automática de API: http://127.0.0.1:8000/docs.
4. Para detener la aplicación usá Ctrl+C. Los cambios locales se guardan en `fortnite.db`.

## Estructura

```text
Fortnite_Tracker/
  app.py                  FastAPI y endpoints
  backend/database.py     SQLite y creación de tablas
  fortnite.db             Base de datos de ejemplo
  public/index.html       Interfaz
  public/static/          JavaScript y CSS
  docs/ANALISIS.md        Problema, objetivo y funcionalidades
  docs/modelo_ER.md       Diagrama entidad-relación, PK, FK y relaciones
  docs/modelo_ER.svg      Diagrama gráfico
  requirements.txt        Dependencias Python
  vercel.json             Configuración de Vercel
  .gitignore              Archivos excluidos de Git
  GUIA_ENTREGA.md         Publicación y entrega
```

## API

| Método | Ruta | Función |
|---|---|---|
| GET | `/api/jugadores` | Consultar jugadores |
| GET | `/api/jugadores/{id}` | Consultar uno |
| POST | `/api/jugadores` | Crear |
| PUT | `/api/jugadores/{id}` | Actualizar |
| DELETE | `/api/jugadores/{id}` | Eliminar |
| GET | `/api/temporadas` | Consultar temporadas |
| POST | `/api/temporadas` | Agregar temporada |
| DELETE | `/api/temporadas/{id}` | Eliminar temporada sin jugadores |

## Nota importante sobre Vercel y SQLite

Vercel permite ejecutar la aplicación FastAPI, pero sus funciones no proporcionan un disco SQLite permanente. En Vercel se usa una copia temporal de `fortnite.db` en `/tmp`; se pueden probar acciones CRUD, **pero los cambios pueden desaparecer** cuando se reinicia la instancia o se ejecuta en otra instancia. La versión local sí conserva cambios en `fortnite.db`. Si el docente exige persistencia real en Vercel, es necesario autorizar una base de datos persistente externa u otro hosting con almacenamiento persistente (lo cual modifica el requisito de SQLite). No se debe presentar el almacenamiento temporal de Vercel como permanente.

## Créditos

Trabajo educativo inspirado en Fortnite. Proyecto no oficial, sin afiliación a Epic Games. Estadísticas iniciales ficticias.
