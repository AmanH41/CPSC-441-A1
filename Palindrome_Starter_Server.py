import socket
import threading
import logging
import re 
from collections import Counter


# Set up basic logging configuration
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Constants for the server configuration
HOST = 'localhost'
PORT = 12345

def handle_client(client_socket, client_address):
    """ Handle incoming client requests. """
    logging.info(f"Connection from {client_address}")
    
    try:
        while True:
            # Receive data from the client
            request_data = client_socket.recv(1024).decode()
            if not request_data:  # Client has closed the connection
                break

            logging.info(f"Received request: {request_data}")
            
            # Here, the request is processed to determine the response
            response = process_request(request_data)
            client_socket.send(response.encode())
            logging.info(f"Sent response: {response}")
    finally:
        # Close the client connection
        client_socket.close()
        logging.info(f"Closed connection with {client_address}")
        exit()

def process_request(request_data):
    """ Process the client's request and generate a response. """
    # Students need to parse the request and call the appropriate palindrome function
    check_type, input_string = request_data.split('|')
    input_string = ''.join(e for e in input_string if e.isalnum()).lower()
    
    if check_type == 'simple':
        result = is_palindrome(input_string)
        return f"Is palindrome: {result}"
    elif check_type == "complex":
        can_form, swaps,result = is_complexPalindrome(input_string)
        #return f"Can form palindrome: {can_from}"
        return f"\nCan form palindrom: {can_form}\nNumber of swaps: \nPalindrome: {result}"



def is_palindrome(input_string):
    ##python module to remove white space and special char 
    input_string = re.sub(r'[^a-zA-Z0-9]', '', input_string).lower()
    """ Check if the given string is a palindrome. """
    return input_string == input_string[::-1]  ## return true or false if string is palindrome 

def can_form_palindrome(input_string):
    #Check if the string can be rearranged into a palindrome.
    # Count the frequency of each character
    char_counts = Counter(input_string)
    # Count how many characters have an odd frequency
    odd_counts = sum(1 for count in char_counts.values() if count % 2 != 0)
    # A string can form a palindrome if at most one character has an odd count
    return odd_counts <= 1 


def is_complexPalindrome(input_string):
    """Calculate the minimum number of swaps to convert the string into a palindrome."""
    if not can_form_palindrome(input_string):
        return False, 0  # Cannot form a palindrome

    # Convert the string to a list for easier manipulation
    s = list(input_string)
    n = len(s)
    swaps = 0

    # Two-pointer approach
    left, right = 0, n - 1  #left pointer at the beginning and right pointer at the end of string  
    while left < right:
        # If characters match, move both pointers
        if s[left] == s[right]:
            left += 1
            right -= 1
        else:
            # Find the matching character from the right
            mid = right
            while mid > left and s[mid] != s[left]:
                mid -= 1
            # If no matching character found, it's already a palindrome
            if mid == left:
                s[left], s[left + 1] = s[left + 1], s[left]
                swaps += 1
            else:
                # Swap characters to make s[left] == s[right]
                for i in range(mid, right):
                    s[i], s[i + 1] = s[i + 1], s[i]
                    swaps += 1
                left += 1
                right -= 1
    
    palindrome =''.join(map(str,s))

    return True, swaps, palindrome

def start_server():
    """ Start the server and listen for incoming connections. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        logging.info(f"Server started and listening on {HOST}:{PORT}")
        
        while True:
            # Accept new client connections and start a thread for each client
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == '__main__':
    start_server()
