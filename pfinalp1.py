#!/usr/bin/python
# -*- coding: latin-1 -*-
 
#################################### PRACTICA 3 ######################################
######################### Autores: Raquel Noblejas Sampedro  #########################
#########################          Daniel Revilla Twose      #########################
######################################################################################

# Importamos las bibliotecas que vamos a usar.
from subprocess import call
from lxml import etree
import shutil
import sys
import os

if (len(sys.argv) == 2):
    orden = sys.argv[1]
    print "La orden dada ha sido: " + orden

elif (len(sys.argv) == 4):
    orden = sys.argv[1]
    orden1 = sys.argv[2]
    orden2 = sys.argv[3]
    print "La orden dada ha sido: " + orden
    print "La orden dada ha sido: " + orden1
    print "La orden dada ha sido: " + orden2

else:
    orden = "error"

longitudOrdenEntera = len(sys.argv)

# Parametro global que contiene la lista de las MVs creadas e iremos añadiendo según los requisitos del usuario.
# Añadimos los equipos c1 y lb al array de maquinas que usaremos.
maquinas = []

# Variable donde se encuentra el directorio donde crearemos el directorio de trabajo.
path = "/mnt/tmp"
fullPath = "/mnt/tmp/p3"

# Constante para que se ponga un numero minimo y maximo de servidores.
numeroMinimoServidores = 1
numeroMaximoServidores = 5

# Variable para poner las direcciones IP de los servidores.
contador = 11

# Si la orden es create: crear los ficheros .qcow2 de diferencias y de especificacion
# XML de cada MV, asi como los bridges que soportan las LAN del escenario.
if(orden == "create"):

    # Mensaje explicativo de lo que realizara la orden dada.
    print "Al finalizar se crearan los ficheros qcow2 de diferencias y de especificacion XML de cada MV asi como la configuracion de la red."

    # Variable de control del bucle hasta que se introduce un numero dentro del rango.
    isNoEnteroAdecuado = True

    if (longitudOrdenEntera == 4):

        # Comprobamos si se ha introducido en el comando la opcion -n para determinar desde el inicio el numero de servidores.
        if(orden1 == "-n"):
            try:
                numeroServidores = int(orden2)
            except:
                print "Por favor introduce un numero entre [" + str(numeroMinimoServidores) + " - " + str(numeroMaximoServidores) + "]"
                sys.exit("Saliendo del script por favor introduzca un comando de los siguientes: create, create -n X, start, stop o destroy.")
            
            # Comprobamos que el numero de servidores pasado como argumento este entre los valores adecuados.
            if ((numeroServidores >= numeroMinimoServidores) and (numeroServidores <= numeroMaximoServidores)):

                print "Se configuraran " + str(numeroServidores) + " servidores."

                # Añadimos en el array de las maquinas los servidores.
                for n in range(1, numeroServidores+1):
                    maquinas.append("s"+str(n))

                # Añadimos en el array las maquinas del balanceador y del equipo c1.
                maquinas.append("lb")
                maquinas.append("c1")

                # Este metodo elimina replicados en la lista.
                set(maquinas)

                # Y las ordenamos alfabeticamente.
                sorted(maquinas)

                # Detenemos el bucle cambiando el estado de la variable noNumeroEntero.
                isNoEnteroAdecuado = False
    else:
        print "Para emplear el script de forma automatica especifique despues del comando -n segudo del numero de servidores (ej: -n 3)"

    print "Al no introducir correctamente o no introducir los parametros ej(-n 3) se pedira que introduzca manualmente el numero de servidores a crear."

    # Si no introducimos el numero de servidores en el comando se pedira al usuario que introduzca un numero de servidores entre el rango.
    while isNoEnteroAdecuado:

        # Preguntamos al usuario cuantos servidores quiere crear dentro del rango establecido.
        numeroServidores = raw_input("Cuantos servidores desea tener? [" + str(numeroMinimoServidores) + " - " + str(numeroMaximoServidores) + "]")
        try:
    	   numeroServidores = int(numeroServidores)
        except:
           print "Por favor introduce un numero entre [" + str(numeroMinimoServidores) + " - " + str(numeroMaximoServidores) + "]"

        # Comprobamos que lo introducido es un entero y que es positivo.
        if ((numeroServidores >= numeroMinimoServidores) and (numeroServidores <= numeroMaximoServidores)):
            
            print "Se configuraran " + str(numeroServidores) + " servidores."

            # Añadimos en el array de las maquinas los servidores.
            for n in range(1, numeroServidores+1):
                maquinas.append("s"+str(n))

            # Añadimos en el array las maquinas del balanceador y del equipo c1.
            maquinas.append("lb")
            maquinas.append("c1")

            # Este metodo elimina replicados en la lista.
            set(maquinas)

            # Y las ordenamos alfabeticamente.
            sorted(maquinas)

            # Detenemos el bucle cambiando el estado de la variable noNumeroEntero.
            isNoEnteroAdecuado = False
        
        # En caso de contrario damos al usuario un mensaje para que introduzca un numero entero dentro del rango.
        else:
            print "Por favor introduce un numero entre [" + str(numeroMinimoServidores) + " - " + str(numeroMaximoServidores) + "]"

    # Accedemos al directorio correspondiente.
    os.chdir(path)

    # Comprobamos si esta creado el directorio de trabajo "p3" y sino lo creamos.
    if (not os.path.isdir("p3")):
    	call(["mkdir","p3"])

    # Nos metemos en el directorio de trabajo.
    os.chdir("p3")

    # Si no encontramos la imagen comprimida la copiamos al directorio de trabajo
    if (not os.path.isfile("cdps-vm-base-p3.qcow2")):

    	# Equivalente al comando "cp" en phyton "shutil.copy(source, destination)".
        print "Copiando imagen base para las maquinas virtuales al directorio de trabajo."
    	shutil.copy("/mnt/vnx/repo/cdps-vm-base-p3.qcow2.bz2", ".")

        # Mensaje para comprobar que va a descomprimir la imagen (que se encuentra comprimida).
    	print "Descomprimiendo imagen base para las maquinas virtuales."
    	call(["bunzip2", "cdps-vm-base-p3.qcow2.bz2"])

    # Copiamos la plantilla XML en nuestro directorio de trabajo.
    shutil.copy("/mnt/vnx/repo/plantilla-vm-p3.xml", ".")

    # Bucle para crear los ficheros de configuracion de las maquinas.
    for i in maquinas:

        # Si no esta el fichero de la maquina virtual entonces la crearemos.
        if not os.path.isfile(i+".qcow2"):

            # Creamos la maquina virtual e imprimos por pantalla el mensaje de que se estan creando los ficheros.
            call(["qemu-img", "create", "-f", "qcow2", "-b", "cdps-vm-base-p3.qcow2", i+".qcow2"])
            shutil.copy("plantilla-vm-p3.xml", i+".xml")
            print "Fichero creado: "+i+".xml"
        
        # Sino imprimimos un mensaje diciendo que dicha maquina virtual ya esta creada.
        else:
            print "Ya existen los ficheros de "+i+".qcow2 en el directorio."


    # Vamos a editar los ficheros XML con las configuraciones adecuadas, sustituyendo los valores XXXX por lo que se debe mostrar.
    # Antes de arrancar cada maquina virtual se monta su sistema de ficheros en un directorio del host.
    # Modificamos los ficheros necesarios de cada MV directamente desde el host para el correcto funcionamiento.
    for i in maquinas:

        # Cargamos el fichero XML.
        tree = etree.parse(i+".xml")

        # Obtenemos el nodo raiz.
        root = tree.getroot()

        # Cambiamos el nombre de la VM en el fichero XML.
        name = root.find("name")

        # Comprobamos que el fichero no ha sido editar previamente.
	if (name.text == "XXX"):
            name.text = i
            
            # Cambiamos la fuente del fichero de la imagen.
            source = root.find("./devices/disk/source")
            source.set("file", "/mnt/tmp/p3/"+i+".qcow2")

            # Si es c1 debemos de configurarle en la LAN1.
            if (i == "c1"): 

            	# Cambiamos el bridge dentro de la interface para c1.
            	bridge = root.find("./devices/interface/source")
            	bridge.set("bridge", "LAN1")

                # Imprimimos los cambios que vamos a escribir en los ficheros XML.
                # print etree.tostring(tree, pretty_print=True)

                # Escribimos los cambios en el fichero XML.
                tree.write(i+".xml", pretty_print=True)


            # Si es el balanceador de carga tenemos que añadir dos interfaces para ambas LANs
            elif (i == "lb"):

                # Cambiamos el bridge dentro de la interface para lb.
                bridge = root.find("./devices/interface/source")
                bridge.set("bridge", "LAN1")

                # Con estos comandos creamos el elemento interface que hay que duplicar (o añadir al nodo devices).
                interfaceNuevo = etree.Element("interface", type="bridge")
                sourceNuevo = etree.SubElement(interfaceNuevo, "source", bridge="LAN2")
                modelNuevo = etree.SubElement(interfaceNuevo, "model", type="virtio")

                # El elemento creado anteriormente lo añadimos (append) al nodo devices.
                devices = root.find("devices")
                devices.append(interfaceNuevo)

                # Imprimimos los cambios que vamos a escribir en los ficheros XML.
                # print etree.tostring(tree, pretty_print=True)

                # Escribimos los cambios en el fichero XML.
                tree.write(i+".xml", pretty_print=True)

            # Si son servidores debemos de configurarlos en la LAN2.
            else:

        	    # Cambiamos el bridge dentro de la interface para los servidores.
            	bridge = root.find("./devices/interface/source")
            	bridge.set("bridge", "LAN2")

                # Imprimimos los cambios que vamos a escribir en los ficheros XML.
                # print etree.tostring(tree, pretty_print=True)

                # Escribimos los cambios en el fichero XML.
                tree.write(i+".xml", pretty_print=True)
	else:
	    print "El fichero "+i+".xml ya ha sido editado y su imagen configurada asi como su configuracion de red."

        # Creamos un directorio donde montar la imagen en el host
        call(["mkdir","mnt_"+i])

        # Ahora los ficheros de la MV estaran accesibles en el directorio "mnt"+i.
        call(["sudo", "vnx_mount_rootfs", "-s", "-r", i+".qcow2", "mnt_"+i])
        
        # Entramos en el directorio etc para cambiar el fichero hostname.
        os.chdir(fullPath+"/mnt_"+i+"/etc/")

        # Con el comando open(fichero, modo) el modo elegimos "w" que permite unicamente la escritura.
        # Para mas informacion sobre los modos de apertura: http://www.tutorialspoint.com/python/python_files_io.htm
        localhost = open("hostname", "w")

        # Escribimos el nombre del localhost como el nombre de la MV.
        localhost.write(i)

        # Cerramos el fichero.
        localhost.close()

        # Entramos en el directorio de trabajo p3 para la siguiente imagen.
        os.chdir("../..")

        # Entramos en el directorio etc para cambiar el fichero hostname.
        os.chdir(fullPath+"/mnt_"+i+"/etc/")

        fichero = open("hosts", 'r')
        ficheroLeido = fichero.read()
        fichero.close()

        cambios = ficheroLeido.replace("cdps", i)

        fichero = open("hosts", 'w')
        fichero.write(cambios)
        fichero.close()

        # Entramos en el directorio de trabajo p3 para la siguiente imagen.
        os.chdir("../..")

        # Entramos en el directorio etc/network/ para cambiar el fichero interfaces.
        os.chdir(fullPath+"/mnt_"+i+"/etc/network/")

        # Configuracion del fichero /etc/network/interfaces
        # http://www.cyberciti.biz/tips/howto-ubuntu-linux-convert-dhcp-network-configuration-to-static-ip-configuration.html
        fichero = open("interfaces", "r")
        ficheroLeido = fichero.read()
        fichero.close()

        cambios = ficheroLeido.replace("dhcp", "static")

        fichero = open("interfaces", "w")
        fichero.write(cambios)
        fichero.close()


        # Configuramos el resto del fichero interfaces segun el tipo de MV.
        if(i == "c1"):
            fichero = open("interfaces", "a")

            # Escribimos las siguientes lineas que faltan para la configuracion de la red.
            lineas = ["address 10.0.1.2\n", "netmask 255.255.255.0\n", "gateway 10.0.1.1"]
            fichero.writelines(lineas)
            fichero.close()

            # Entramos en el directorio de trabajo p3 para la siguiente imagen.
            os.chdir("../../..")

        # Si es el balanceador de carga debemos de añadirle ambas interfaces LAN1 y LAN2 (eth0 y eth1)
        elif(i == "lb"):
            fichero = open("interfaces", "a")

            # Escribimos las siguientes lineas que faltan para la configuracion de la red.
            lineas = ["address 10.0.1.1\n", "netmask 255.255.255.0\n", "\n","auto eth1\n" "iface eth1 inet static\n", "address 10.0.2.1\n", "netmask 255.255.255.0"]
            fichero.writelines(lineas)
            fichero.close()

	    # Entramos en el directorio de trabajo p3 para la siguiente imagen.
            os.chdir("../../..")

	    # Entramos en el directorio etc para cambiar el fichero hostname.
            os.chdir(fullPath+"/mnt_"+i+"/etc/")

            fichero = open("sysctl.conf", "r")
            ficheroLeido = fichero.read()
   	    fichero.close()

            cambios = ficheroLeido.replace("#net.ipv4.ip_forward=1", "net.ipv4.ip_forward=1")

            fichero = open("sysctl.conf", "w")
            fichero.write(cambios)
            fichero.close()
                
            # Salimos al directorio de trabajo.
            os.chdir("../..")

        # Si no es ni el balanceador de carga ni el c1 entonces debera ser un servidor.
        else:
            fichero = open("interfaces", "a")

            # Escribimos las siguientes lineas que faltan para la configuracion de la red.
            lineas = ["address 10.0.2."+str(contador)+"\n", "netmask 255.255.255.0 \n", "gateway 10.0.2.1"]
            fichero.writelines(lineas)
            fichero.close()

            # Incrementamos el contador para la siguiente direccion IP sea distinta.
            contador = contador + 1

	    # Entramos en el directorio de trabajo p3 para la siguiente imagen.
            os.chdir("../../..")
        
        # Una vez terminado de modificar los ficheros necesarios para la configuracion de la MV la desmontamos.
        call(["sudo", "vnx_mount_rootfs", "-u", "mnt_"+i])

	# Destruimos el directorio donde se ha montado la imagen.
	os.system("rm -rf mnt_"+i)

    # Creacion de los bridges.
    call(["sudo", "brctl", "addbr", "LAN1"])
    call(["sudo", "brctl", "addbr", "LAN2"])
    call(["sudo", "ifconfig", "LAN1", "up"])
    call(["sudo", "ifconfig", "LAN2","up"])


    # Comandos de configuracion para el Host (nuestra terminal).
    os.system("sudo ifconfig LAN1 10.0.1.3/24")
    os.system("sudo ip route add 10.0.0.0/16 via 10.0.1.1")

    # Debemos crear dos veces las MVs porque si no da fallo.
    for i in range(1, 3):

        # Creación de las MVs.
        for i in maquinas:

           # Mensaje diciendo que se estan creando las MVs.
           print "Creando la MV: " + i
           call(["sudo", "virsh", "create", i+".xml"])

    # Indicamos que ha terminado el script con exito.
    print "La ejecuccion ha terminado sin problemas."


################################################################################################################
################################################################################################################


# Arrancar las maquinas virtuales y mostrar su consola
elif (orden == "start"):

    # Imprimimos mensaje informativo.
    print "Al finalizar se abriran las terminales de las MVs creadas."

    # Accedemos al directorio correspondiente.
    os.chdir("/mnt/tmp")

    # Comprobamos si existe el directorio de trabajo.
    if (os.path.isdir("p3")):

        # Entramos en el directorio de trabajo.
        os.chdir("p3")

        # Tenemos que saber cuantas MVs hay creadas.
        ficheros = os.listdir(fullPath)

        # Llenamos la lista de MVs creada.
        for i in ficheros:
            
            for j in range(1, numeroMaximoServidores+1):

                # Si el fichero corresponde al XML de un servidor lo añadimos a la lista de MVs.
                if(i == "s"+str(j)+".xml"):

                    maquinas.append("s"+str(j))

        # Añadimos las MVs correspondientes a c1 y a lb.
        maquinas.append("c1")
        maquinas.append("lb")

        # Este metodo elimina replicados en la lista.
        set(maquinas)

        # Y las ordenamos alfabeticamente.
        sorted(maquinas)

	# Debemos crear dos veces las MVs porque si no da fallo.
    	for i in range(1, 3):

            # Creación de las MVs.
            for i in maquinas:

                # Mensaje diciendo que se estan creando las MVs.
                print "Creando la MV: " + i
                call(["sudo", "virsh", "create", i+".xml"])

        # Vamos recorriendo las MVs creadas para arrancar (en background) sus respectivas terminales.
        for i in maquinas:
            print "Abriendo la consola de: " + i

            # Abrimos la consola textual de cada MVs con el siguiente comando.
            comando = 'xterm -e "sudo virsh console ' + i + '" &'
            os.system(comando)

        # Arrancar gestor de MV.
        os.system("HOME=/mnt/tmp sudo virt-manager")

    else:
        print "El directorio de trabajo p3 no esta creado, por favor para crearlo use el comando create."

    # Indicamos que ha terminado el script con exito.
    print "La ejecuccion ha terminado sin problemas."


################################################################################################################
################################################################################################################


# Para parar las maquinas virtuales.
elif (orden == "stop"):

    # Imprimimos mensaje informativo.
    print "Al finalizar se pararan las terminales de las MVs creadas."

    # Accedemos al directorio correspondiente.
    os.chdir("/mnt/tmp")

    # Comprobamos si existe el directorio de trabajo.
    if (os.path.isdir("p3")):

        # Entramos en el directorio de trabajo.
        os.chdir("p3")

        # Tenemos que saber cuantas MVs hay creadas.
        ficheros = os.listdir(fullPath)

        # Llenamos la lista de MVs creada.
        for i in ficheros:
            
            for j in range(1, numeroMaximoServidores+1):
                 # Si el fichero corresponde al XML de un servidor lo añadimos a la lista de MVs.
                 if(i == "s"+str(j)+".xml"):

                       maquinas.append("s"+str(j))

        # Añadimos las MVs correspondientes a c1 y a lb.
        maquinas.append("c1")
        maquinas.append("lb")

        # Este metodo elimina replicados en la lista.
        set(maquinas)

        # Y las ordenamos alfabeticamente.
        sorted(maquinas)

        # Recorremos las MVs creadas para apagarlas (stop).
        for i in maquinas:

            print "Deteniendo la MV de: " + i
            call(["sudo", "virsh", "shutdown", i])

    # Al no existir el directorio de trabajo no podemos destruir nada y damos un mensaje informativo.
    else:
        print "El directorio de trabajo p3 no esta creado, por favor para crearlo use el comando create."

    # Indicamos que ha terminado el script con exito.
    print "La ejecuccion ha terminado sin problemas."


################################################################################################################
################################################################################################################


# Para liberar el escenario, borrando todos los ficheros creados, es decir, el entorno de trabajo.
elif (orden == "destroy"):

    # Imprimimos mensaje informativo.
    print "Al finalizar se liberara el escenario borrando el entorno de trabajo creado."

    # Accedemos al directorio correspondiente.
    os.chdir("/mnt/tmp")

    # Comprobamos si existe el directorio de trabajo.
    if (os.path.isdir("p3")):

        # Entramos en el directorio de trabajo.
        os.chdir("p3")

        # Tenemos que saber cuantas MVs hay creadas.
        ficheros = os.listdir(fullPath)

        # Llenamos la lista de MVs creada.
        for i in ficheros:
            
            for j in range(1, numeroMaximoServidores+1):
                 # Si el fichero corresponde al XML de un servidor lo añadimos a la lista de MVs.
                 if(i == "s"+str(j)+".xml"):

                       maquinas.append("s"+str(j))

        # Añadimos las MVs correspondientes a c1 y a lb.
        maquinas.append("c1")
        maquinas.append("lb")

        # Este metodo elimina replicados en la lista.
        set(maquinas)

        # Y las ordenamos alfabeticamente.
        sorted(maquinas)

        # Destruimos todas las maquinas virtuales.
        for i in maquinas:

            # Dando la orden destroy.
            call(["sudo", "virsh", "destroy", i])

        # Una vez destruidas las MVs ahora eliminaremos el directorio de trabajo con todos los elementos dentro.
        os.chdir("/mnt/tmp")
        call(["rm", "-rf", "p3"])

    # Al no existir el directorio de trabajo no podemos destruir nada y damos un mensaje informativo.
    else:
        print "El directorio de trabajo p3 no esta creado, por favor para crearlo use el comando create."

    # Indicamos que ha terminado el script con exito.
    print "La ejecuccion ha terminado sin problemas."


################################################################################################################
################################################################################################################


# Para ver el estado de todas las maquinas virtuales.
elif (orden == "monitor"):

    print "Al finalizar se mostrara el estado de todas las MVs."

    os.system("sudo virsh list --all")

    # Indicamos que ha terminado el script con exito.
    print "La ejecuccion ha terminado sin problemas."


# Caso por defecto imprimimos un mensaje diciendo las ordendes disponibles.
else:

    # Imprimimos un mensaje por defecto en caso de que la orden dada no sea la adecuada, recordando las ordenes compatibles.
    print "Por favor ejecute el script seguido de una de las siguientes ordenes: create, start, stop o destroy."

