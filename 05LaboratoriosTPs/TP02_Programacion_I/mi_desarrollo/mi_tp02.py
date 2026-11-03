# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  Lihuen Flores
#  Comision:           .....................................
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    # TU CODIGO ACA
    if not isinstance(comando, (tuple, list)) or len(comando) == 0:
        return False, "no es una tupla o esta vacia"

    nombre = comando[0]

    if nombre in ("detenerse", "saludar"):
        if len(comando) != 1:
            return False, f"'{nombre}' no lleva datos"
        return True, ""

    if nombre in ("avanzar", "girar"):
        if len(comando) != 3:
            return False, f"'{nombre}' necesita velocidad y tiempo"

        velocidad, tiempo = comando[1], comando[2]
        for valor in (velocidad, tiempo):
            # bool es subclase de int, por eso se excluye aparte
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                return False, f"{valor!r} no es un numero"

        if tiempo < 0:
            return False, "el tiempo es negativo"
        if tiempo > 10:
            return False, f"el tiempo ({tiempo} s) supera el maximo de 10 s"

        limite = 0.20 if nombre == "avanzar" else 0.50
        if abs(velocidad) > limite:
            return False, f"la velocidad ({velocidad}) supera el maximo de {limite}"
        return True, ""

    return False, f"el comando '{nombre}' no existe"


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    # TU CODIGO ACA
    nombre = comando[0]

    try:
        if nombre == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "detenerse":
            robot.detenerse()
        elif nombre == "saludar":
            robot.saludar()
    except ErrorDeSeguridad as error:
        return f"RECHAZADO POR EL ROBOT: {error}"

    return "OK"


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    # TU CODIGO ACA
    for comando in mision:
        valido, motivo = comando_es_valido(comando)

        if not valido:
            historial.append({
                "comando": comando,
                "ejecutado": False,
                "detalle": motivo,
            })
            continue  # sigue con el siguiente, no corta la mision

        resultado = ejecutar_comando(robot, comando)
        historial.append({
            "comando": comando,
            "ejecutado": resultado == "OK",
            "detalle": resultado,
        })


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    # TU CODIGO ACA
    ok = [h for h in historial if h["ejecutado"]]
    fallidos = [h for h in historial if not h["ejecutado"]]

    print("=" * 50)
    print("REPORTE DE LA MISION")
    print("=" * 50)
    print(f"Comandos totales:    {len(historial)}")
    print(f"Ejecutados bien:     {len(ok)}")
    print(f"Rechazados:          {len(fallidos)}")

    if fallidos:
        print("\nMotivos de rechazo:")
        for h in fallidos:
            print(f"  - {h['comando']}: {h['detalle']}")
    print("=" * 50)


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    mision_saludo = [
        ("saludar",),
        ("avanzar", 0.2, 2.0),
        ("saludar",),
    ]   

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_BASICA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
