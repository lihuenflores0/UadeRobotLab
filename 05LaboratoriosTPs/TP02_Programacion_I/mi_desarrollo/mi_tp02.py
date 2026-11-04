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

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO, MISION_CIRCULO


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
    es_valido = False

    if isinstance(comando, tuple) and len(comando) > 0 and isinstance(comando[0], str):
        if comando[0] == "avanzar" or comando[0] == "girar":
            if len(comando) == 3:
                velocidad_ok = (isinstance(comando[1], (int, float))
                                and not isinstance(comando[1], bool))
                tiempo_ok = (isinstance(comando[2], (int, float))
                             and not isinstance(comando[2], bool))
                if velocidad_ok and tiempo_ok and comando[2] >= 0:
                    es_valido = True
        elif comando[0] == "detenerse" or comando[0] == "saludar":
            if len(comando) == 1:
                es_valido = True

    return es_valido


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

    if nombre == "avanzar":
        robot.avanzar(velocidad=comando[1], tiempo=comando[2])
        texto = "avanzo a " + str(comando[1]) + " m/s durante " + str(comando[2]) + " s"
    elif nombre == "girar":
        robot.girar(velocidad=comando[1], tiempo=comando[2])
        texto = "giro a " + str(comando[1]) + " rad/s durante " + str(comando[2]) + " s"
    elif nombre == "detenerse":
        robot.detenerse()
        texto = "se detuvo"
    elif nombre == "saludar":
        robot.saludar()
        texto = "saludo"
    else:
        texto = "comando desconocido: " + nombre

    return texto

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

    for i in range(len(mision)):
        numero = i + 1
        comando = mision[i]

        if comando_es_valido(comando):
            try:
                detalle = ejecutar_comando(robot, comando)
                historial.append([numero, comando, "ejecutado", detalle])
                print("[OK] #" + str(numero), comando, "->", detalle)
            except ErrorDeSeguridad as error:
                motivo = "rechazado por el robot (seguridad): " + str(error)
                historial.append([numero, comando, "rechazado", motivo])
                print("[RECHAZADO] #" + str(numero), comando, "->", motivo)
        else:
            # Averiguar por que no es valido
            if not isinstance(comando, tuple):
                motivo = "el comando no es una tupla"
            elif len(comando) == 0:
                motivo = "el comando esta vacio"
            elif not isinstance(comando[0], str):
                motivo = "el nombre del comando no es un texto"
            elif comando[0] == "avanzar" or comando[0] == "girar":
                if len(comando) != 3:
                    motivo = comando[0] + " lleva 2 datos (velocidad y tiempo)"
                elif (not isinstance(comando[1], (int, float))
                      or isinstance(comando[1], bool)):
                    motivo = "la velocidad no es un numero"
                elif (not isinstance(comando[2], (int, float))
                      or isinstance(comando[2], bool)):
                    motivo = "el tiempo no es un numero"
                elif comando[2] < 0:
                    motivo = "el tiempo es negativo"
                else:
                    motivo = "no cumple el formato"
            elif comando[0] == "detenerse" or comando[0] == "saludar":
                motivo = comando[0] + " no lleva datos"
            else:
                motivo = "comando desconocido: " + comando[0]

            historial.append([numero, comando, "rechazado", motivo])
            print("[RECHAZADO] #" + str(numero), comando, "->", motivo)


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
    ejecutados = 0
    rechazados = 0

    for registro in historial:
        if registro[2] == "ejecutado":
            ejecutados = ejecutados + 1
        else:
            rechazados = rechazados + 1

    print("=" * 50)
    print("REPORTE FINAL DE LA MISION")
    print("=" * 50)
    print("Comandos recibidos: ", len(historial))
    print("Ejecutados bien:    ", ejecutados)
    print("Rechazados:         ", rechazados)

    if rechazados > 0:
        print("\nMotivos de rechazo:")
        for registro in historial:
            if registro[2] == "rechazado":
                print("  #" + str(registro[0]), registro[1], "->", registro[3])
    print("=" * 50)


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = [] 

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_CIRCULO, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
