import asyncio
import asyncpg
import json

from app.socketio import SocketManager
from app.mqtt import MQTTManager

listener_ch = ["update", "update_table"]


class TestListen:
    sio_ = None

    def __init__(self, sio: SocketManager, mqtt: MQTTManager):
        self._sio = sio
        self._mqtt = mqtt
        self.q = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.db_events(), loop=self.loop)

    # @asyncio.coroutine
    async def listen(self, conn, channel):
        async def listener1(conn, pid, channel, payload):
            print(channel, payload)
            await self.q.put(conn)

        await conn.add_listener("test", listener1)
        for ch in listener_ch:
            await conn.add_listener(ch, self.listen_handler)
        # await conn.add_listener("update", self.listen_handler)
        # await conn.add_listener("update_table", self.listen_handler)
        await conn.execute("NOTIFY test,'open notify test'")

    async def db_events(self):
        conn = await asyncpg.connect(
            dsn="postgresql://postgres:postgres@localhost:5432/postgres"
        )
        print("connected", conn)
        await self.listen(conn, "test")

    async def listen_handler(self, conn, pid, channel, payload):
        print(channel, payload)
        data = json.loads(payload)
        ns = "/" + "/".join(list(data.values())[:4])
        print("namespace:", ns)
        print(
            "data:",
        )
        await self.q.put(conn)
        await self._sio.emit(channel + "-ws", payload)
        self._mqtt.pub(channel + "-mqtt", payload)
