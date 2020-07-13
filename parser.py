#!/usr/bin/python
from Crypto.PublicKey import RSA

import re
import base64
import sys
import subprocess
from rsa_reconstruction.factor_db  import n_to_primes, get_prime
from rsa_reconstruction.rebuild_key import  recover_key

def parse_public_key(pubkey):
    element = pubkey
    if not pubkey.isdigit() and ("BEGIN PUBLIC" not in pubkey or "END PUBLIC" not in pubkey):
        element = ("-----BEGIN PUBLIC KEY-----\n" 
                + element 
                + "\n-----END PUBLIC KEY-----")

    return element

def to_rsa_key(key_encoded):
    # lets check if we're given an integer. If so, reconstruct the key
    if key_encoded.isdigit():
        pubkey = RSA.construct((int(key_encoded), 65537L))
    # key looks to be in PEM format so lets just import it
    else:
        pubkey = RSA.importKey(key_encoded)

    # pubkey.n is our base10'ified version of our base16 modulus
    # pubkey.e is our exponent (usually 65537) (2^16)+1
    print("[*] pubkey.e: {}".format(pubkey.e))
    print("[*] pubkey.n: {}".format(pubkey.n))
    return pubkey


def perform_algorithm(pubkey_string):
    # Select the appropriate algorithm based on key size
    pubkey_string = parse_public_key(pubkey_string)
    pubkey = to_rsa_key(pubkey_string)
    if pubkey.n.bit_length() < 256:
        print("[*] key length is too small for nfs algorithm (try a key >=256). Trying \"factordb\" prime lookups instead")
        s,p_page,q_page = n_to_primes(str(pubkey.n))[0]
        p = get_prime(p_page)
        q = get_prime(q_page) 
        if p!=q:
            return [p,q, pubkey.e]
        else: return None

    print("[*] Key looks like {} bits".format(pubkey.n.bit_length()))
    result_set = perform_nfs(pubkey)
    result_set.append(pubkey.e)
    return result_set

def read_subprocess(pubkey):
    proc = subprocess.Popen(["/app/cado-nfs-2.3.0/cado-nfs.py", str(pubkey.n)], shell=False, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = None
    while (True):
        line = proc.stdout.readline()
        line = line.decode()
        if (line == ""): break
        matched = re.search(":([^:]+):.*(\d+\.?\d+\%)", line)
        if matched:
            sys.stdout.write('[*] %s %s\r' % (matched.group(1), matched.group(2)))
            sys.stdout.flush()
        result = line
    return result

def perform_nfs(pubkey):
    print("[*] Using cadonfs to compute primes")
    result = read_subprocess(pubkey)
    return result.split()

if __name__ == "__main__":
    if len(sys.argv) <= 1: 
        print("[*] Please provide a public key or modulus as first argument.")
        sys.exit(1)

    pubkey_string = sys.argv[1]

    primes_and_exponent = perform_algorithm(pubkey_string)
    print("[*] results are: {}".format(primes_and_exponent))
    if primes_and_exponent and len(primes_and_exponent) == 3:
        print("[*] Key extraction done.")
        p,q,e = primes_and_exponent
        recover_key(int(p),int(q),int(e), None)

