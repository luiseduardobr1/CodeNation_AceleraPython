import jwt


def create_token(data, secret):
    return jwt.encode(data, secret, 'HS256')


def verify_signature(token):
    try:
        return jwt.decode(token, "acelera")
    except:
        return {"error": 2}
