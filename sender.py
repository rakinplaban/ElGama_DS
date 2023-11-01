# Acknowledgment: This code is based on an example from OpenAI's GPT-3 model (https://github.com/OpenAI/gpt-3.5-turbo/blob/main/examples/elgamal_digital_signature.py).
# The code has been modified to suit the project's requirements.

import random
import math
# Extended Euclidean Algorithm to find modular multiplicative inverse
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

# Calculate modular multiplicative inverse
def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("The modular inverse does not exist")
    else:
        return x % m

# Generate a primitive root modulo q
def generate_primitive_root(q):
    for a in range(2, q):
        if all(pow(a, (q - 1) // i, q) != 1 for i in range(2, q)):
            return a

# Generate a random integer relatively prime to q - 1
def generate_random_relative_prime(q):
    while True:
        k = random.randint(2, q - 1)
        if math.gcd(k, q - 1) == 1:
            return k

# Key generation for user A
# Key generation for user A
def generate_public_keys(q):
    a = generate_primitive_root(q)
    XA = random.randint(1, q - 1)
    YA = pow(a, XA, q)
    return (q, a, YA)

def generate_private_key(q):
    a = generate_primitive_root(q)
    XA = random.randint(1, q - 1)
    return (q, a, XA)

# Sign a message M
def sign_message(message, private_key):
    q, a, XA = private_key  # Unpack the private key correctly
    m = hash(message.encode('utf-8')) % (q - 1)
    K = generate_random_relative_prime(q)
    S1 = pow(a, K, q)
    K_inv = mod_inverse(K, q - 1)
    S2 = (K_inv * (m - XA * S1)) % (q - 1)
    return (S1, S2)


def save_signatures_to_file(signatures, file_path):
    with open(file_path, 'w') as file:
        for signature in signatures:
            S1, S2 = signature
            file.write(f"{S1} {S2}\n")


def verify_signature(message, signature, public_key):
    q, a, YA = public_key
    S1, S2 = signature
    if not (1 <= S1 <= q - 1) or not (0 <= S2 <= q - 2):
        return False
    m = hash(message.encode('utf-8')) % (q - 1)
    left = (pow(YA, S1, q) * pow(S1, S2, q)) % q
    right = pow(a, m, q)
    return left == right



if __name__ == '__main__':
    q = 101  # Replace with your desired prime number
    public_key = generate_public_keys(q)
    private_key = generate_private_key(q)

    messages = ["Message1", "Message2", "Message3"]
    signatures = []

    for message in messages:
        signature = sign_message(message, private_key)
        signatures.append(signature)

    save_signatures_to_file(signatures, 'signatures.txt')
