from flask import Flask, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from apps.config import Config

auth = HTTPTokenAuth(scheme='JWT')


@auth.verify_token
def verify_token(token):
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(token)
        print(data)
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    #g.user = User.query.get(data.get('id'))
    return True

def generate_token(user_id):
    s = Serializer(Config.SECRET_KEY)
    token = s.dumps({"user_id":user_id}).decode()
    return token

def decode_token(inside_token):
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(inside_token)
        print(data)
    except SignatureExpired:
        return False,'内部token过期', None
    except BadSignature:
        return False,'token错误',None
    return True,'内部token校验成功',data

if __name__ == '__main__':
    # t = generate_token(1)
    # print(t)
    # print(verify_token(t))
    print(decode_token('eyJhbGciOiJIUzUxMiIsImlhdCI6MTYyMjEwMTI1NCwiZXhwIjoxNjIyMTA0ODU0fQ.eyJ1c2VyX2lkIjoyNn0.X7-RGfM_mdhqZ3nsl1KulpRqmCKtAvke0NrFCLXZ_iQONmA_n6pui6Uo5cN8_7AAme9Yx5i_VonedPEqirnmYA'))
