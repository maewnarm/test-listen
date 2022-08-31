import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dblistener import TestListen
from app.socketio import SocketManager,createSocket
from app.mqtt import MQTTManager

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = SocketManager(app=app)
createSocket(sio=sio)

mqtt = MQTTManager()
mqtt.sub("update")

listener = TestListen(sio,mqtt)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
