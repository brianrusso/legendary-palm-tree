from werkzeug.security import generate_password_hash, check_password_hash
from arango import Arango

a = Arango(host="localhost", port=8529, username='root', password='joker')
db = a.database("aminer")
