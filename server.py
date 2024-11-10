import socket
import threading

#här skapas en tcp server som tar info/lyssnar på en specifik port som i detta fall är 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345)) #local host och port
server_socket.listen(1)
print('serverstatus:igång\nväntar på anslutning\n') #detta är första servermeddelande när allting gått igenom




#detta är en lista som lagrar klienter som är anslutna till servern
clients = []


#med denna funktion så kan man skicka meddelande till alla klienter som är anslutna till servern
def broadcast(message, sender_socket):
        for client in clients:
            if client != sender_socket:
                client.sendall(message.encode())


#här är en funktion som då hanterar varje klient
def handle_client(client_socket, client_address):
    print(f'ny anslutning: {client_address}, glöm inte att chatta')
    welcome_message = f'välkommen till servern: {client_address}. glöm ej att chatta!'
    client_socket.sendall(welcome_message.encode())
    broadcast(f'ny anslutning {client_address}', client_socket)
    clients.append(client_socket)



    try:
        while True:
            message = client_socket.recv(1024).decode() #här tas meddelanden emot från klienten
            if not message:
                break
            print(f'meddelande från {client_address}: {message}')
            broadcast(message, client_socket)
    except ConnectionResetError:
        print(f'Användare {client_address} har lämnat')



    finally: #skulle det vara så att klientens anslutning avbryts så kopplar den ifrån den
        clients.remove(client_socket)
        client_socket.close()
        print(f'avslutad anslutning: {client_address}')


#här startas det en ny tråd för varje klient som är ansluiten
try:
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,client_address))
        client_thread.start()
finally:
    server_socket.close()