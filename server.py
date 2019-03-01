from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import MySQLdb as MySQL

app = Flask(__name__, static_folder='templates')
app.config['SECRET_KEY'] = 'karton'
socketio = SocketIO(app)
CORS(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
  if path != "" and os.path.exists("react_app/build/" + path):
    return send_from_directory('react_app/build', path)
  else:
    return send_from_directory('react_app/build', 'index.html')


@app.route('/chat', methods=['GET'])
def get_chat_messages():
  db = MySQL.connect('localhost', 'root', '12345', 'chat', charset='utf8')
  cur = db.cursor()
  cur.execute('SELECT * FROM messages')
  messages = jsonify(cur.fetchall())
  cur.close()
  db.close()
  return messages


@app.route('/message', methods=['POST'])
def get_current_message_and_save_to_database():
  content = request.json
  db = MySQL.connect('localhost', 'root', '12345', 'chat', charset='utf8')
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
  print "%s connected" % (request.sid)


socketio.run(app, use_reloader=True, host='192.168.111.234')
