from flask import Flask, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from apps.config import Config

#app = Flask(__name__)
#auth = HTTPTokenAuth(scheme='JWT',header="X-Token")
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

if __name__ == '__main__':
    t = generate_token(1)
    print(t)
    print(verify_token(t))