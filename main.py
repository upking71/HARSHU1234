from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import requests
import json

# Encryption function
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

# Decryption function
def decrypt_message(encrypted_message, key):
    encrypted_message = base64.b64decode(encrypted_message)
    nonce = encrypted_message[:16]
    tag = encrypted_message[16:32]
    ciphertext = encrypted_message[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_message.decode('utf-8')

# Function to send an encrypted message
def send_encrypted_message(message, key):
    encrypted_message = encrypt_message(message, key)
    payload = {
        'message': encrypted_message
    }
    response = requests.post('https://your-api-endpoint', json=payload)
    if response.status_code == 200:
        print("Encrypted message sent successfully.")
    else:
        print("Failed to send encrypted message.")

# Function to receive and decrypt a message
def receive_encrypted_message(key):
    response = requests.get('https://your-api-endpoint')
    if response.status_code == 200:
        encrypted_message = response.json()['message']
        decrypted_message = decrypt_message(encrypted_message, key)
        print("Decrypted message received:", decrypted_message)
    else:
        print("Failed to fetch encrypted message.")

# Example usage
def main():
    # Generate a random key (should be securely shared with the recipient)
    key = get_random_bytes(16)  # AES-128 key (16 bytes)

    # Example message
    message_to_send = "Hello, this is a test message!"

    # Send encrypted message
    send_encrypted_message(message_to_send, key)

    # Simulate receiving encrypted message (replace with actual implementation)
    receive_encrypted_message(key)

if __name__ == "__main__":
    main()
  
