# Análisis y diseño del proyecto

**Nombre:** Fortnite Tracker.

**Problema:** Cuando varias personas quieren llevar un registro de sus partidas de Fortnite, puede ser incómodo organizar sus estadísticas en notas separadas. Se necesita un lugar donde registrar y actualizar los datos de cada jugador.

**Objetivo general:** Desarrollar una página web sencilla que permita gestionar jugadores y sus estadísticas de Fortnite mediante Python, FastAPI y SQLite.

**Usuarios:** Estudiantes y personas que juegan Fortnite y desean organizar manualmente los resultados de sus partidas.

**Funcionalidades:** Ver jugadores; buscar por nombre; crear, editar y eliminar jugadores; registrar plataforma, temporada, partidas, victorias y eliminaciones; agregar y eliminar temporadas; ver totales generales. Los datos se consultan desde SQLite por medio de una API.

**Alcance:** Es una aplicación de registro manual, no consulta la API oficial de Fortnite. Los datos iniciales son ejemplos ficticios.

**Arquitectura:** navegador (HTML, CSS, JS) → API REST en FastAPI (Python) → SQLite (tablas temporadas y jugadores).
