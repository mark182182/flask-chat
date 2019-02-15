from flask import Flask, render_template, jsonify, request
import MySqldb as MySQL

app = Flask(__name__)


@app.route('/')
def get_index():
  return render_template('index.html')


@app.route('/chat', methods=['GET'])
def get_chat_messages():
  db = MySQL.connect('localhost', 'root', '12345', "chat")
  cur = db.cursor()
  cur = cur.execute('SELECT * FROM messages')
  messages = jsonify(cur.fetchall())
  return messages


@app.route('/chat', methods=['POST'])
def post_chat_messages():
  message = get_current_message()
  db = MySQL.connect('localhost', 'root', '12345', "chat")
  cur = db.cursor()
  cur = cur.execute('INSERT INTO messages (username, message) VALUES($s, $s)',
                    [message['username'], message['message']])


@app.route('/message', methods=['GET'])
def get_current_message():
  content = request.json
  print content['username']
  print content['message']
  return jsonify({"username": content['username'], "message": content['message']})


app.run(debug=true)
