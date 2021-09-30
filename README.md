# RSACrack
RSACrack is a toolbox for deriving private key files from a given public key file, modulus or base64 encoded key.

At the time of writing it supports cracking RSA keys of 128, 256 bits in minutes. If you need to perform factorization in less time, feel free to spin up an EC2 instance that is compute optimised. My tests so far have shown 256bits can be done in less than 50 seconds using this toolbox.

## Motivation
I developed this toolbox so I could better understand how RSA works and gain an understanding of the various factorization libraries. Putting this together makes it simple for non-cryptographers to develop proof of concept key reconstruction without having to worry about the details.

## Getting started (quick method)
The simplest way to get started is to:

####  pull the docker image directly from [dockerhub](https://hub.docker.com/r/b4den/rsacrack).
`docker pull b4den/rsacrack`

#### run the toolbox against your public key file
`docker run -it b4den/rsacrack "$(cat location_of_your_public_key_file.pub)"`

For key bit lengths of less than or equal to 256 bits, after a couple of minutes the output should look something like:
```
[*] results are: ['<snip>', '<snip>', <snip>]
[*] Key extraction done.
-----BEGIN RSA PRIVATE KEY-----
		<snip>
-----END RSA PRIVATE KEY-----
```

## Getting started (building from Dockerfile)
I'd strongly suggest using the _quick_ method above, but if you want to build the docker image locally, that's supported too.

> Please note this may take some time due to `cado-nfs` and `openssl` library compile times.

#### clone the repo
`git clone https://github.com/b4den/rsacrack.git`

### build the image
`docker build . -t rsacrack`

### run your experiments!
`docker run -it b4den/rsacrack:latest  "$(cat location_of_your_public_key_file.pub)"`

## Additional notes
The notes for generating RSA key pairs are given below. If you're on a macbook then you should be able to generate keypairs using small key lengths. Otherwise, an earlier version of `openssl` is provided in the toolbox for this purpose.

#### Generating RSA private key
`openssl genrsa -out private_key.pem 256`

#### Extract public key from private key
`openssl rsa -in private_key.pem -pubout > public_key.pub`

#### Input specification
The application takes one and only one argument. From there the `modulus`, `exponent` and eventually `primes` are deduced from that key.

*Valid inputs*
- public key strings `docker run -it b4den/rsacrack "$(cat public_key.pem)"`
- public key value `docker run -it b4den/rsacrack "base64encoded-pubkey"`
- public key modulus `docker run -it b4den/rsacrack modulusint`


#### Openssl version
Some newer versions of openssl won't let you generate rsa keys of 128/256 bit sizes. As a workaround the image comes pre-compiled with openssl 1.0.0: `docker run --entrypoint openssl -it b4den/rsacrack genrsa 256`

> For Macbook's they come with LibreSSL so you should be able to use your builtin openssl library for key generation using small key lengths.

## References
Do check out the other repositories that this code relies on. `factordb` is a lookup site where `n` is small (<=128 bits). For key lengths greater than 128, our toolbox relies on the `cado-nfs` library.
- [`cado-nfs`](https://github.com/kurhula/cado-nfs)
- [`factordb`](http://factordb.com/)
- [`0day.work`](https://0day.work/how-i-recovered-your-private-key-or-why-small-keys-are-bad/)
