# Bitácora técnica - TP02 Robot Unitree Go2

**Alumnos:** Santiago Balsamo, Emanuel Brandt, Martin Salvagni, Lihuen Flores
**Materia:** Programación I
**Repositorio:** (https://github.com/lihuenflores0/UadeRobotLab)

## Registro de acciones

| Nº | Acción / comando | Resultado | Problema | Solución intentada | Estado |
|---|---|---|---|---|---|
| 1 | Clone del repositorio UadeRobotLab | Repo clonado | - | - | RESUELTO |
| 2 | Fork en GitHub | Fork creado | - | - | RESUELTO |
| 3 | Lectura de INSTALACION.md y LEEME_ESTUDIANTE.md | Respondidas preguntas a-e | - | - | RESUELTO |
| 4 | `systeminfo \| findstr /B /C:"OS Name" /C:"OS Version"` | Windows 11 Home, 10.0.26200 Build 26200 | - | - | RESUELTO |
| 5 | `echo %PROCESSOR_ARCHITECTURE%` | AMD64 | - | - | RESUELTO |
| 6 | `py -3 --version` / `python --version` | Python 3.14.8 | - | - | RESUELTO |
| 7 | `py -3 -m pip --version` | pip 26.3 | - | - | RESUELTO |
| 8 | `git --version` | git 2.53.0.windows.2 | - | - | RESUELTO |
| 9 | `python3 -c "import mujoco; print(mujoco.__version__)"` | 3.14.0 | - | MuJoCo ya estaba instalado, no hizo falta pip install | RESUELTO |
| 10 | `py -3 -m pip install mujoco` |	`Requirement already satisfied: mujoco 3.14.0 (y dependencias)` | - | Ya estaba instalado | RESUELTO |
| 11 | INICIAR_SIMULADOR.bat, opción 1 (G1) | Simulador iniciado: Robot: Unitree G1 | - | - | RESUELTO |


## Respuestas de la sección 3

### a) ¿Qué herramientas necesita el TP?

- **Python 3.10 o superior:** ejecuta todo, el simulador y mi programa.
- **MuJoCo** (`pip install mujoco`): es la ventana 3D donde se ve el robot.
- **Visual C++ Redistributable (x64):** solo en Windows; sin él, MuJoCo se instala pero no carga.
- **Modelos del G1 y del Go2:** el robot que se ve en pantalla. Ya vienen dentro del paquete (`entorno/sim/unitree_mujoco/`, unos 46 MB).
- **Carpeta del laboratorio:** el TP en sí (`05LaboratoriosTPs/TP02_Programacion_I/`).

### b) ¿Qué versión de Python se requiere?

Python 3.10 o superior. El ejemplo de verificación de la guía muestra Python 3.12.3, así que versiones más nuevas también funcionan.

### c) ¿Qué componentes ya están instalados en la computadora?

En la computadora ya estaba instalado Python 3.14, Git 2.53, Visual Studio Code y MuJoCo (el import devuelve la versión 3.14.0).

### d) ¿Qué componentes del repositorio oficial de Unitree no son necesarios?

Para este laboratorio no hacen falta:

- **CycloneDDS:** solo publica paquetes precompilados hasta Python 3.10, y con versiones más nuevas pip intenta compilarlo y falla con "Could not locate cyclonedds".
- **unitree_sdk2_python (el SDK oficial):** llama a `timerfd_create`, que existe solo en Linux, por lo que en macOS y Windows el import falla con "symbol not found".
- **Compilar nada ni clonar el repo completo de Unitree:** los modelos del G1 y del Go2 ya vienen recortados dentro del paquete (el repo completo pesa 299 MB; el paquete trae unos 46 MB).

### e) Diferencias entre el TP en PDF y el repositorio actual

El PDF usaba un simulador que solo imprimía logs y comandos expresados como objetivos (distancia y velocidad; ángulo en grados y sentido en texto). El repositorio actual usa un gemelo digital en MuJoCo y expresa todo en velocidad y tiempo, donde el signo de la velocidad angular indica el sentido. Los límites cambian a 0.20 m/s, 0.50 rad/s y 10 s, y ahora también se evalúa la instalación y la bitácora.

| Aspecto | TP en PDF | Repositorio actual |
|---|---|---|
| Simulador | `unitree_sdk_sim.py` (solo logs) | `robot.py` + MuJoCo por socket local |
| avanzar | `("avanzar", distancia, velocidad)` | `("avanzar", velocidad, tiempo)` |
| girar | `("girar", 90, "derecha")` (grados y texto) | `("girar", -0.5, 3.14)` (rad/s y segundos; el signo da el sentido) |
| Límites | 0.5 m/s, 5 m, 180° | 0.20 m/s, 0.50 rad/s, 10 s |
| Funciones | `inicializar_robot`, `procesar_comando` | `comando_es_valido`, `ejecutar_comando` |
| Control de seguridad | Solo la validación propia | Además, el robot lanza `ErrorDeSeguridad` |
| Instalación | Solo Python | Python + MuJoCo + Visual C++ en Windows |

## Etapa 1: caracterización del entorno

| Elemento | Información obtenida |
|---|---|
| Sistema operativo | Microsoft Windows 11 Home |
| Versión del sistema operativo | 10.0.26200 N/A Build 26200 |
| Arquitectura | AMD64 |
| Python instalado | Python 3.14.8 |
| Versión de Python | Python 3.14.8 |
| pip disponible | pip 26.3 |
| Git disponible | git version 2.53.0.windows.2 |
| MuJoCo previamente instalado | Sí (versión 3.14.0) |
| IDE utilizado | Visual Studio Code |
| Observaciones | El entorno ya estaba instalado previamente a documentar este punto |

![Comandos del entorno:](evidencias/01_entorno/01_comandos_entorno.png)

## Etapa 2: obtención del repositorio

**Método:** clonación con GitHub Desktop desde
https://github.com/tsamaan/UadeRobotLab.git.
**Ruta local:** C:\Users\lihue\OneDrive\Escritorio\GitHub\-Proyecto-Integrador--Etapa-1--Consejo-del-Mate\UadeRobotLab
**Fork:** https://github.com/lihuenflores0/UadeRobotLab

Los archivos `INSTALACION.md` y `LEEME_ESTUDIANTE.md` se encuentran
en `05LaboratoriosTPs/TP02_Programacion_I/`.

![Repo clonado](evidencias/02_instalacion/github_desktop_clone.png)

![Carpeta TP02](evidencias/02_instalacion/carpeta_tp02.png)

## Etapa 3: instalación de MuJoCo

**Comando:** `py -3 -m pip install mujoco`
**Salida:** Requirement already satisfied: mujoco in C:\Users\lihue\AppData\Roaming\Python\Python314\site-packages (3.14.0), junto con sus dependencias (numpy, glfw, pyopengl, etc.).
**Versión instalada:** 3.14.0 (confirmada con `import mujoco`).
**Advertencias / errores:** ninguno. No hubo errores de certificados.
**Solución aplicada:** ninguna, MuJoCo ya estaba instalado.

![pip install mujoco e import](evidencias/02_instalacion/pip_install_mujoco.png)

## Etapa 4: verificación del entorno

**Comando:** `py -3 -m sim --solo-revisar` (ejecutado desde `05LaboratoriosTPs/TP02_Programacion_I/entorno`)
**Resultado:** [OK] Python 3.14.8, [OK] MuJoCo v3.14.0, [OK] Modelos oficiales de Unitree. Mensaje final: "Todo listo."
**Problemas:** ninguno.

![Verificación del entorno](evidencias/02_instalacion/verificacion_entorno.png)

## Etapa 5: puesta en marcha del gemelo digital

**Comando:** `INICIAR_SIMULADOR.bat`, robot seleccionado: 1 (G1)
**Aclaración:** el orientador menciona el Go2, pero se trabaja con el G1
**Resultado:** el simulador inició correctamente (Python 3.14.8, MuJoCo v3.14.0, modelos oficiales). Se abrió la ventana de MuJoCo con el G1 visible.
**Problemas:** ninguno.

![Selección del robot](evidencias/05_gemelo_digital/seleccion_robot.png)

![Ventana MuJoCo](evidencias/05_gemelo_digital/ventana_mujoco.png)