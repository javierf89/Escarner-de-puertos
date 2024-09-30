import socket 
from termcolor import colored
import sys
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

cont  = 0
def iniciar_socket():

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.1)
    return s


def escarner(ip,port):
    global cont
    s = iniciar_socket()
    try:
        s.connect((ip,port))
        cont = cont+1
        print(colored(f"Este puerto esta abierto: {port}" , 'green'))
        s.sendall(b"HEAD / HTTP/ 1.0\r\n\r\n")
        respuesta = s.recv(1024)
        respuesta =  respuesta.decode(errors='ignore').split('\n')
        if respuesta:
           print(colored(f"Descripcion del puerto:\n " , 'yellow'))
           for line in respuesta:
               print(colored(f"{line}" , 'grey'))
       

    except(socket.timeout,ConnectionRefusedError):
        pass
    finally:
        s.close()

def inicializador(ip,port):

    for i in port:
        escarner(ip,int(i))

def menu():


    print(colored(f"----- Bienvenido al menu: ----- \n" , 'yellow'))


    print(colored("1. Un puerto" ,'blue'))
    print(colored("2. Muchos puertos",'blue'))
    print(colored("3. Un rango de puertos" ,'blue'))

    opcion = int(input(colored("Ingrese la opcion: " , 'green')))

    if opcion==1:
        port= input(colored(f"Ingrese el  puerto:\n " , 'light_magenta'))
        ip = input(colored("Ingrese la ip: \n " ,'light_magenta'))
        inicializador(ip,(port,))
    elif opcion==2:
        port = input(colored("Ingrese varios puertos en este estilo (example: 1,2,3):  " , 'light_magenta'))
        port =port.split(',')
   
        ip = input(colored("Ingrese la ip: " ,'light_magenta'))
        inicializador(ip,(port))
    elif opcion==3:
        port = input(colored("Ingrese un rango de puerto example(1-65535): ", 'light_magenta'))
        ip = input(colored("Ingrese la ip: " ,'light_magenta'))
        port = port.split('-')
        for i in  range(int(port[0]),int(port[1])):
            port.append(int(i))
        with ThreadPoolExecutor(max_workers=100) as tareas:
            tareas.map(lambda puertos : inicializador(ip,(puertos,)),port)
    else:
        print(colored("Error: valor incorrecto", 'red'))
        sys.exit(1)
    

def main():
    menu()
    print(colored(f"El programa termino con esta cantidad de puertos abiertos {cont}" , 'red'))


if __name__ == '__main__':
   main()