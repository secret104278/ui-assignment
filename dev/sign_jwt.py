#!/usr/bin/env python3

"""
the dev key pair can be generate by following cmd

openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
"""

import jwt
from pathlib import Path

token = {
    "acct": "admindev",
}

private_key = Path("private.pem").read_text()
encoded = jwt.encode(token, private_key, algorithm="RS256")
Path("adminjwt").write_text(encoded)
