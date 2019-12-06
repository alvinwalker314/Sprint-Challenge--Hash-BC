import hashlib
import requests
import json
import sys
from uuid import uuid4
from timeit import default_timer as timer
import random


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """
    start = timer()
    print("Searching for next proof")
    # Random starting point
    proof = random.randint(1, 100)
    # Convert last proof into unicode
    last_hash_uni = str(last_proof).encode()
    # Hash the last proof
    last_hash = hashlib.sha256(last_hash_uni).hexdigest()
    # Attempt to validate it
    while valid_proof(last_hash, proof) is False:
        # increment proof by a random number
        proof += random.randint(1, 100)
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    # Encode guess
    guess = f'{proof}'.encode()
    # Hash it
    new_hash = hashlib.sha256(guess).hexdigest()
    print(f'Prev hash end: {last_hash[-1:-7:-1]}')
    print(f'New hash start: {new_hash[0:6]}')
    # Check whether or not the last 6 of the prev has is equal to first 6 of new hash
    return last_hash[-6::1] == new_hash[0:6]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
