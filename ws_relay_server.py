import asyncio
import json
import aiohttp
import aiohttp.web
import websockets

import asyncio
import json
import aiohttp
import aiohttp.web
import websockets

BYBIT_WS = "wss://stream.bybit.com/v3/public/spot"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

async def connect_bybit():
    while True:
        try:
            ws = await websockets.connect(
                BYBIT_WS,
                extra_headers=HEADERS,
                ssl=None,
                ping_interval=20,
                ping_timeout=20
            )
            print("Connected to Bybit WS")
            return ws
        except Exception as e:
            print("Reconnect to Bybit failed:", e)
            await asyncio.sleep(2)

async def relay_handler(request):
    ws_client = aiohttp.web.WebSocketResponse(heartbeat=20)
    await ws_client.prepare(request)

    ws_bybit = await connect_bybit()

    async def client_to_bybit():
        async for msg in ws_client:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    await ws_bybit.send(msg.data)
                except:
                    break

        await ws_bybit.close()
        await ws_client.close()

    async def bybit_to_client():
        try:
            async for msg in ws_bybit:
                await ws_client.send_str(msg)
        except:
            pass

        await ws_client.close()

    await asyncio.gather(client_to_bybit(), bybit_to_client())
    return ws_client

def main():
    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.get("/relay", relay_handler)])
    aiohttp.web.run_app(app, port=8765)

if __name__ == "__main__":
    main()
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

async def connect_bybit():
    while True:
        try:
            ws = await websockets.connect(
                BYBIT_WS,
                extra_headers=HEADERS,
                ssl=None,
                ping_interval=20,
                ping_timeout=20
            )
            print("Connected to Bybit WS")
            return ws
        except Exception as e:
            print("Reconnect to Bybit failed:", e)
            await asyncio.sleep(2)

async def relay_handler(request):
    ws_client = aiohttp.web.WebSocketResponse(heartbeat=20)
    await ws_client.prepare(request)

    ws_bybit = await connect_bybit()

    async def client_to_bybit():
        async for msg in ws_client:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    await ws_bybit.send(msg.data)
                except:
                    break

        await ws_bybit.close()
        await ws_client.close()

    async def bybit_to_client():
        try:
            async for msg in ws_bybit:
                await ws_client.send_str(msg)
        except:
            pass

        await ws_client.close()

    await asyncio.gather(client_to_bybit(), bybit_to_client())
    return ws_client

def main():
    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.get("/relay", relay_handler)])
    aiohttp.web.run_app(app, port=8765)

if __name__ == "__main__":
    main()
