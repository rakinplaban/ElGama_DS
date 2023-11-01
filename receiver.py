# Acknowledgment: This code is based on an example from OpenAI's GPT-3 model (https://github.com/OpenAI/gpt-3.5-turbo/blob/main/examples/elgamal_digital_signature.py).
# The code has been modified to suit the project's requirements.


import sender
# Read signatures from a text file and verify them

def verify_signatures_from_file(file_path, public_key):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        S1, S2 = map(int, line.strip().split())
        message = f"Message{i + 1}"  # You should replace this with your actual messages
        is_valid = sender.verify_signature(message, (S1, S2), public_key)

        if is_valid:
            print(f"Signature for Message{i + 1} is valid.")
        else:
            print(f"Signature for Message{i + 1} is invalid.")

if __name__ == '__main__':
    q = 101  # Replace with your desired prime number
    public_key = sender.generate_public_keys(q)
    private_key = sender.generate_private_key(q)

    verify_signatures_from_file('signatures.txt', public_key)
