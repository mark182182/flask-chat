from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
import MySQLdb as MySQL

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'karton'
socketio = SocketIO(app)
CORS(app)

db = MySQL.connect(os.getenv('HOST_ADDRESS'), os.getenv('DB_NAME'), os.getenv('DB_PASS'), os.getenv('DB_DATABASE'), charset='utf8')
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS `messages` ("
            "  `id` int(11) NOT NULL AUTO_INCREMENT,"
            "  `username` varchar(100) COLLATE utf8_hungarian_ci NOT NULL,"
            "  `message` varchar(100) COLLATE utf8_hungarian_ci NOT NULL,"
            "  `createdAt` timestamp NOT NULL DEFAULT current_timestamp(),"
            "  PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_hungarian_ci")

@app.route('/chat', methods=['GET'])
def get_chat_messages():
  db = MySQL.connect(os.getenv('HOST_ADDRESS'), os.getenv('DB_NAME'), os.getenv('DB_PASS'), os.getenv('DB_DATABASE'),
                     charset='utf8')
  cur = db.cursor()
  cur.execute('SELECT * FROM messages')
  messages = jsonify(cur.fetchall())
  cur.close()
  db.close()
  return messages


@app.route('/message', methods=['POST'])
def get_current_message_and_save_to_database():
  content = request.json
  db = MySQL.connect(os.getenv('HOST_ADDRESS'), os.getenv('DB_NAME'), os.getenv('DB_PASS'), os.getenv('DB_DATABASE'),
                     charset='utf8')
  cur = db.cursor()
  cur.execute('INSERT INTO messages (username, message) VALUES(%s, %s)',
              (content['username'], content['message']))
  count_messages = cur.execute('SELECT * FROM messages')
  if (count_messages == 21):
    cur.execute('DELETE FROM messages ORDER BY id LIMIT 1')
  db.commit()
  cur.close()
  db.close()
  socketio.emit('message', content)
  return jsonify(content)


@socketio.on('connect')
def connected():
  print("%s connected" % request.sid)


socketio.run(app, use_reloader=True, host=os.getenv('HOST_ADDRESS'))
