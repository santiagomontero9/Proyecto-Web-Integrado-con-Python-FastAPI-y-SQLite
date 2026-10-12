# Guía rápida para entregar

## Paso 1: probar en tu PC

Abrí `Fortnite_Tracker` en VS Code. Desde la terminal, ejecutá:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Abrí http://127.0.0.1:8000. Creá un jugador, editá las estadísticas y eliminá el jugador. Después comprobá que las temporadas se vean. Para detener el servidor usá `Ctrl+C`.

## Paso 2: subir el proyecto a GitHub

Creá un repositorio público **Fortnite-Tracker** en https://github.com/new. En la terminal dentro de la carpeta del proyecto:

```powershell
git init
git add .
git commit -m "Proyecto Fortnite Tracker con FastAPI y SQLite"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/Fortnite-Tracker.git
git push -u origin main
```

Reemplazá `TU_USUARIO` por tu usuario real de GitHub. Si Git pide iniciar sesión, completá el proceso. Si Git no está instalado, instalá Git para Windows o subí los archivos desde la web de GitHub.

## Paso 3: publicar con Vercel

Método más sencillo, **sin iniciar el proyecto en una terminal**:

1. Entrá a https://vercel.com y creá/iniciá sesión.
2. Elegí **Add New > Project**.
3. Conectá GitHub e importá el repositorio `Fortnite-Tracker`.
4. Dejá **Root Directory** en la raíz del repositorio y framework en **Other** / detección automática. No agregués Build Command.
5. Hacé clic en **Deploy**.
6. Abrí el enlace `.vercel.app`, revisá la página, agregá y modificá un jugador, y probá las funciones.

Si el enlace no funciona, mirá **Deployments > Function Logs** y verificá que Vercel reconozca `app.py` y haya instalado `requirements.txt`.

**Opción alternativa por terminal (no obligatoria):** `npm install -g vercel` y, dentro de la carpeta, `vercel login` seguido de `vercel --prod`.

**Limitación importante:** Vercel permite crear/editar/eliminar registros temporalmente, pero su sistema de archivos no conserva de forma garantizada los cambios de SQLite. Los datos pueden reiniciarse. Para cumplir estrictamente persistencia en producción, consultá al profesor si acepta otro hosting persistente o un cambio de base de datos. Localmente sí persiste.

## Paso 4: entregar

- El archivo `Fortnite_Tracker.zip`.
- URL de GitHub: `https://github.com/TU_USUARIO/Fortnite-Tracker`.
- URL de Vercel: `https://NOMBRE-DEL-PROYECTO.vercel.app` (copiá la URL **real**, no este ejemplo).
- Si la plataforma de clase solicita anexos individuales, `docs/modelo_ER.svg`, `docs/modelo_ER.md` y `docs/ANALISIS.md` ya vienen en el ZIP.

**Importante:** los enlaces reales los obtenés únicamente después de subir y publicar desde tus cuentas. No están creados de antemano.
