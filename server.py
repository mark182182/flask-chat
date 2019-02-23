from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import MySQLdb as MySQL

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_index():
  return render_template('index.html')


@app.route('/chat', methods=['GET'])
def get_chat_messages():
  db = MySQL.connect('172.17.0.2', 'root', '12345', "chat")
  cur = db.cursor()
  cur.execute('SELECT * FROM messages')
  messages = jsonify(cur.fetchall())
  cur.close()
  db.close()
  return messages


@app.route('/message', methods=['POST'])
def get_current_message_and_save_to_database():
  content = request.json
  db = MySQL.connect('172.17.0.2', 'root', '12345', "chat")
  cur = db.cursor()
  cur.execute('INSERT INTO messages (username, message) VALUES(%s, %s)',
              (content['username'], content['message']))
  db.commit()
  cur.close()
  db.close()
  return jsonify(content)


app.run(debug=True)
