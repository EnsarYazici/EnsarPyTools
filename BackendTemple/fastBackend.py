from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import bcrypt

app = FastAPI()

# JSON dosyasını yükle
def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)

# JSON dosyasına veri yaz
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

class LoginRequest(BaseModel):
    username: str
    password: str

class UseRequest(BaseModel):
    username: str

@app.post("/login")
async def login(request: LoginRequest):
    data = load_data()
    for user in data['users']:
        if user['username'] == request.username and bcrypt.checkpw(request.password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return {"success": True, "usage_count": user['usage_count']}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/use")
async def use(request: UseRequest):
    data = load_data()
    for user in data['users']:
        if user['username'] == request.username:
            if user['usage_count'] > 0:
                user['usage_count'] -= 1
                save_data(data)
                return {"success": True}
            else:
                raise HTTPException(status_code=403, detail="No usage left")
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
