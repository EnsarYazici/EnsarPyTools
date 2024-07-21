from flask import Flask, request, jsonify
import json
import bcrypt

app = Flask(__name__)

# JSON dosyasını yükle
def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)

# JSON dosyasına veri yaz
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Kullanıcı doğrulama
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    users_data = load_data()
    for user in users_data['users']:
        if user['username'] == username and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({"success": True, "usage_count": user['usage_count']})
    
    return jsonify({"success": False}), 401

# Kullanım hakkını güncelle
@app.route('/use', methods=['POST'])
def use():
    data = request.json
    username = data['username']
    
    users_data = load_data()
    for user in users_data['users']:
        if user['username'] == username:
            if user['usage_count'] > 0:
                user['usage_count'] -= 1
                save_data(users_data)
                return jsonify({"success": True})
    
    return jsonify({"success": False}), 403

if __name__ == '__main__':
    app.run(debug=True)
