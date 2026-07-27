# AGENTS.md

## Alcance

Estas reglas se aplican a cualquier agente de IA que analice o modifique este repositorio.

## Antes de editar

1. Lee la tarea completa y respeta su alcance.
2. Verifica:
   - `git branch --show-current`
   - `git status`
   - `git log --oneline --decorate -5`
3. Confirma que estás en la rama indicada y que el árbol de trabajo está limpio.
4. Explora únicamente los archivos relacionados con la tarea.
5. Antes de modificar, entrega un análisis breve con:
   - problema confirmado;
   - archivos que propones modificar;
   - solución propuesta;
   - pruebas que agregarás o actualizarás.
6. Espera aprobación antes de implementar, salvo que la tarea indique expresamente lo contrario.

## Reglas de trabajo

- No audites todo el repositorio.
- No amplíes el alcance sin autorización.
- No hagas refactorizaciones generales durante una corrección puntual.
- No cambies rutas, parámetros, nombres públicos o comportamiento existente sin una necesidad confirmada.
- No modifiques modelos ni crees migraciones salvo autorización explícita.
- No modifiques configuración, archivos `.env`, archivos SQL, dependencias, archivos generados ni stashes salvo autorización explícita.
- No ejecutes `migrate`.
- No cambies de rama.
- No descartes cambios existentes.

## Git

- No hagas commit.
- No hagas push.
- No crees Pull Requests.
- Deja los cambios sin commit para revisión manual.

## Calidad

- Mantén las pruebas existentes.
- Agrega o actualiza pruebas para cubrir el cambio solicitado.
- Usa los ajustes de prueba del proyecto cuando corresponda:
  `ProyectEspecial.test_settings`
- Ejecuta, según corresponda:

```powershell
git diff --check
.\venv\Scripts\python.exe -m compileall -q ProyectEspecial Reveloper
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py test Reveloper --settings=ProyectEspecial.test_settings
```

- Si una validación no puede ejecutarse, informa el motivo exacto.
- No ocultes pruebas fallidas, advertencias relevantes ni riesgos pendientes.

## Respuesta final

Entrega un resumen breve con:

1. problema corregido;
2. archivos modificados;
3. pruebas agregadas o actualizadas;
4. resultado de las validaciones;
5. riesgos pendientes;
6. `git status`;
7. mensaje de commit sugerido.

No repitas el prompt ni entregues un informe extenso salvo que se solicite expresamente.
