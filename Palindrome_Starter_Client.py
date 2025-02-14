import socket
import time 

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
TIMEOUT = 5  # 5 second timeout
MAX_RETRIES = 3  # 3 Tries before time out 

def send_request(request_data):
    #Send a request to the server and handle timeout/retries
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Create a socket and set a timeout
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(TIMEOUT)
                print(f"Attempting to connect to server (Retry {retries + 1})...")
                
                # Connect to the server
                client_socket.connect((SERVER_HOST, SERVER_PORT))
                print("Connected to server.")
                
                # Send the request data
                client_socket.send(request_data.encode())
                print(f"Sent request: {request_data}")
                
                # Receive the response
                response = client_socket.recv(1024).decode()
                return response
        except socket.timeout:
            print("Error: Server did not respond within the timeout period.")
        except ConnectionRefusedError:
            print("Error: Server is not available.")
        except Exception as e:
            print(f"Error: {e}")
        
        # Increment retry count and wait before retrying
        retries += 1
        if retries < MAX_RETRIES:
            print(f"Retrying in {TIMEOUT} seconds...")
            time.sleep(TIMEOUT)
            if retries == MAX_RETRIES:
                print("Max retries reached. Exiting.")
                break    
    return None


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
                response = send_request(message)
                if response:
                    print(f"Server response: {response}")

            elif choice == '2':
                input_string = input("Enter the string to check: ")
                message = f"complex|{input_string}"
                response = send_request(message)
                if response:
                    print(f"Server response: {response}")    

            elif choice == '3':
                print("Exiting the client...")
                break

            else:
                print("Invalid choice. please try agian.")

if __name__ == "__main__":
    start_client()
