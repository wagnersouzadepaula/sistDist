# Miguel Braz
# Wagner Souza de Paula

import socket
import select
import errno
import sys


cabecalho_maximo = 40

IP = "127.0.0.1"
PORT = 1234
nomeUsuarioCliente = input("Nome do usuário: ")
socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketCliente.connect((IP, PORT))

socketCliente.setblocking(False)

nomeClienteCodificado = nomeUsuarioCliente.encode('utf-8')
username_header = f"{len(nomeClienteCodificado):<{cabecalho_maximo}}".encode('utf-8')
socketCliente.send(username_header + nomeClienteCodificado)

while True:

    message = input(f'{nomeUsuarioCliente} diz: ')

    if message:

        message = message.encode('utf-8')
        message_header = f"{len(message): {cabecalho_maximo}}".encode('utf-8')
        socketCliente.send(message_header + message)
        if message.decode().upper() == 'SAIR':
            exit()

    try:

        while True:

            username_header = socketCliente.recv(cabecalho_maximo)

            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())

            nomeClienteCodificado = socketCliente.recv(username_length).decode('utf-8')

            message_header = socketCliente.recv(cabecalho_maximo)
            message_length = int(message_header.decode('utf-8').strip())
            message = socketCliente.recv(message_length).decode('utf-8')


            print(f'{nomeClienteCodificado} > {message}')

    except IOError as e:

        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        continue

    except Exception as e:

        print('Reading error: '.format(str(e)))
        sys.exit()
