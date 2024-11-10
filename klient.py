import socket
import threading

### denna kod hittade jag för att snygga till det man fick upp i terminalen. Innan såg det ostrukturerat.
RESET = "\033[0m"  
CLEAR_LINE = "\033[K"    

def clear_line_and_print(message):    
    print(f"\r{CLEAR_LINE}{message}")   

def print_prompt():  
    print(f"\rSkriv ditt meddelande: {RESET}", end="", flush=True) 
### denna kod från RESET till def print_promt hittade jag som sagt

#denna funktion används för att ta emot meddelande från servern
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode() # denna servern kommer inte behöva ta emot meddelande som är större än 1024 därför är 1024 byte åt gången satt.
            if message: #felsökning, kollar om meddelandet är tomt
                clear_line_and_print(f'\nserver meddelande!!! {message}{RESET}')
                print_prompt() #detta kommer upp när och visar att det är från severn
            else:
                clear_line_and_print('förlorad anslutning till server')
                break
        except Exception as e:
            clear_line_and_print(f'ett fel uppstod, asnlutning avbruten')
            break


##denna skapar vi tcp klienten och även anslutning till servern
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
print('ansluten till servern')


#här bildas själva starten för att ta emot meddelanden
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()




#detta är en såkallad "huvudloop" och är till för att skicka olika meddelanden och 
#kan skicka en hel del bara genom att skriva och trycka enter
try:
    while True:
        print_prompt()
        message = input()
        if message.lower() == 'exit':
            break
        client_socket.sendall(message.encode())
finally:
    client_socket.close()