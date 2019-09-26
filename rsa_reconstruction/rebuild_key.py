#!/usr/bin/python

import pyasn1.codec.der.encoder  
import pyasn1.type.univ  
import base64

def recover_key(p, q, e, output_file):  
    def egcd(a, b):
        x,y, u,v = 0,1, 1,0
        while a != 0:
            q, r = b//a, b%a
            m, n = x-u*q, y-v*q
            b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
        return gcd, x, y

    def modinv(a, m):
        gcd, x, y = egcd(a, m)
        if gcd != 1:
            return None  # modular inverse does not exist
        else:
            return x % m

    def pempriv(n, e, d, p, q, dP, dQ, qInv):
        template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
        seq = pyasn1.type.univ.Sequence()
        for x in [0, n, e, d, p, q, dP, dQ, qInv]:
            seq.setComponentByPosition(len(seq), pyasn1.type.univ.Integer(x))
        der = pyasn1.codec.der.encoder.encode(seq)
        return template.format(base64.encodestring(der).decode('ascii'))

    # main logic starts here
    n = p * q
    phi = (p -1)*(q-1)
    d = modinv(e, phi)
    dp = d % p
    dq = d % q
    qi = pow(q, p - 2, p)

    key = pempriv(n, e, d, p, q, dp, dq, qi)
    print(key)

    if output_file:
        f = open(output_file,"w")
        f.write(key)
        f.close()
