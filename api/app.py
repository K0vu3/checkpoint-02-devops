from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
api = Api(app)

CORS(app)

db = psycopg2.connect(
    host="db",
    database="api_db",
    user="api_user",
    password="example"
)

cursor = db.cursor()
#removendo a tabela caso ja exista
query_0 = """
    DROP TABLE IF EXISTS users
"""
cursor.execute(query_0)
db.commit()

#criando a tabela e as colunas
cursor = db.cursor()
query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        age INTEGER,
        email TEXT,
        city TEXT,
        ip TEXT
    )
"""
cursor.execute(query)
db.commit()

#carga na tabela
query_01 = """
    INSERT INTO users (id, name, age, email, city, ip) VALUES
    (1, 'Demetris', 44, 'dgaitskill0@biglobe.ne.jp', 'Talzemt', '223.71.111.130'),
    (2, 'Estele', 35, 'eswigg1@wikipedia.org', 'Valence', '225.167.42.247'),
    (3, 'Britteny', 20, 'bgolson2@psu.edu', 'Bantiran', '236.53.245.251'),
    (4, 'Dniren', 24, 'dsnar3@vkontakte.ru', 'Nesterovskaya', '245.165.207.76'),
    (5, 'Aurelia', 22, 'ayaldren4@wix.com', 'Sehwān', '30.37.114.248'),
    (6, 'Vernon', 20, 'veburne5@fotki.com', 'Thayetmyo', '151.190.53.98'),
    (7, 'Lesley', 23, 'lmoatt6@mozilla.com', 'El Jícaro', '179.251.239.173'),
    (8, 'Giana', 18, 'galexis7@google.ca', 'Rokoy', '4.231.142.219'),
    (9, 'Rosemaria', 34, 'rwaddie8@cbsnews.com', 'Ratenggoji', '76.154.4.118'),
    (10, 'Ernaline', 56, 'eantoniutti9@msn.com', 'Luhačovice', '32.20.171.149'),
    (11, 'Bertram', 58, 'bbattera@canalblog.com', 'Nazran', '59.228.14.95'),
    (12, 'Gene', 46, 'genriquesb@plala.or.jp', 'Jardinópolis', '23.129.238.41'),
    (13, 'Keely', 42, 'kferrync@cornell.edu', 'Inazawa', '94.131.246.152'),
    (14, 'Danit', 26, 'dedmottd@salon.com', 'Hollywood', '122.156.62.10'),
    (15, 'Jase', 19, 'jstuddearde@fastcompany.com', 'Xingang', '195.200.153.182'),
    (16, 'Lorrin', 39, 'lparfettf@latimes.com', 'Boston', '235.218.74.2'),
    (17, 'Hakeem', 51, 'hpolycoteg@independent.co.uk', 'Luftinjë', '36.239.160.243'),
    (18, 'Graehme', 35, 'gmabenh@jugem.jp', 'Verkhniye Kigi', '107.213.112.161'),
    (19, 'Wendeline', 32, 'wpollyi@g.co', 'Cruzeiro do Sul', '135.88.128.167'),
    (20, 'Neal', 56, 'nallchinj@yahoo.co.jp', 'Calingcuan', '91.2.92.224'),
    (21, 'Brynn', 59, 'bdecreuzek@amazon.com', 'Wetzlar', '242.126.28.40'),
    (22, 'Wilma', 22, 'wcoalbranl@nba.com', 'Chegutu', '223.192.174.166'),
    (23, 'Glen', 19, 'ggarthlandm@de.vu', 'Tantu', '233.211.207.27'),
    (24, 'Stacia', 59, 'sspeightn@boston.com', 'Leonárisso', '116.168.176.164'),
    (25, 'Minette', 22, 'mwinearo@sphinn.com', 'Guangning', '43.16.144.179')
"""
cursor.execute(query_01)
db.commit()


class Users(Resource):
    def get(self):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users ORDER BY id")
        result = cursor.fetchall()
        # Criar um dicionário para cada linha do resultado
        users = []
        for row in result:
            user = {
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'email': row[3],
                'city': row[4],
                'ip': row[5]
            }
            users.append(user)

        # Retornar os usuários em formato JSON
        return jsonify(users)
        # return jsonify(result)

    def post(self):
        cursor = db.cursor()
        data = request.get_json()
        query_find_last_id = "SELECT MAX(id) FROM users;"
        cursor.execute(query_find_last_id)
        last_id = cursor.fetchone()[0]
        new_id = last_id + 1
        query = "INSERT INTO users (id, name, age, email, city, ip) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (new_id, data['name'], data['age'], data['email'], data['city'], data['ip'])
        try:
            cursor.execute("BEGIN")
            cursor.execute(query, values)
            cursor.execute("COMMIT")
            return {'status': 'success', 'message': 'User added successfully'}
        except Exception as e:
            cursor.execute("ROLLBACK")
            return {'status': 'error', 'message': str(e)}
    
    def put(self, user_id):
        cursor = db.cursor()
        data = request.get_json()
        query = "UPDATE users SET name = %s, age = %s, email = %s, city = %s,ip = %s WHERE id = %s"
        values = (data['name'], data['age'],data['email'], data['city'],data['ip'], user_id)
        try:
            cursor.execute("BEGIN")
            cursor.execute(query, values)
            cursor.execute("COMMIT")
            return {'status': 'success', 'message': 'User updated successfully'}
        except Exception as e:
            cursor.execute("ROLLBACK")
            return {'status': 'error', 'message': str(e)}

    def delete(self, user_id):
        cursor = db.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        db.commit()
        return {'status': 'success', 'message': 'User deleted successfully'}

api.add_resource(Users, '/users', '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
