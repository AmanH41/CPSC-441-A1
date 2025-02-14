import socket

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

def start_client():
    """ Start the client and connect to the server. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        

        #test
        # Client interaction loop
        while True:
            # Display the menu and get user input
            print("\nMenu:")
            print("1. Simple Palindrome Check")
            print("1. Complex Palindrome Check")
            print("2. Exit")
            choice = input("Enter choice (1/2/3): ").strip()

            if choice == '1':
                input_string = input("Enter the string to check: ")
                message = f"simple|{input_string}"
                client_socket.send(message.encode())
                # Wait for and display the server response
                response = client_socket.recv(1024).decode()
                print(f"Server response: {response}")
            elif choice == '2':
                input_string = input("Enter the string to check: ")
                message = f"complex|{input_string}"
                client_socket.send(message.encode())
                # Wait for and display the server response
                response = client_socket.recv(1024).decode()
                print(f"Server response: {response}")                
            elif choice == '3':
                print("Exiting the client...")
                message = f"exit"
                client_socket.send(message.encode())
                break

if __name__ == "__main__":
    start_client()
