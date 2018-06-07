#will contain an in memory table of all registered users
from werkzeug.security import safe_str_cmp
from user import User


users = [
    User(1,'bob', 'asdf') 
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):  #this is equivalent of user.password == password, it just works on all python versions and different systems
        return user
        
def identity(payload):  #identity function is unique to FlaskJWT (which we installed). payload is the contents of the JWT token.
    user_id = payload['identity'] 
    return userid_mapping.get(user_id, None)
        