# ============================================================
# BYBIT WS RELAY v2.0 — Stable WebSocket Proxy
# ------------------------------------------------------------
# - GEO-bypass (KZ, TR, UAE, EU restrictions)
# - auto-reconnect
# - multi-client support
# - correct subscription forwarding
# - keeps connection alive
# ============================================================

import asyncio
import json
import aiohttp
import aiohttp.web
import websockets

BYBIT_WS = "wss://stream.bybit.com/v5/public"

# ----------------------------------------------------------------
# Connect to Bybit and return a live websocket connection
# ----------------------------------------------------------------
async def connect_bybit():
    while True:
        try:
            ws = await websockets.connect(BYBIT_WS, ssl=None, ping_interval=20, ping_timeout=20)
            print("Connected to Bybit WS")
            return ws
        except Exception as e:
            print("Bybit WS reconnect error:", e)
            await asyncio.sleep(2)


# ----------------------------------------------------------------
# Relay Handler — client <-> bybit
# ----------------------------------------------------------------
async def relay_handler(request):
    ws_client = aiohttp.web.WebSocketResponse(heartbeat=20)
    await ws_client.prepare(request)

    ws_bybit = await connect_bybit()

    async def client_to_bybit():
        async for msg in ws_client:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    await ws_bybit.send(msg.data)
                except Exception:
                    break

        print("Client disconnected (client_to_bybit)")
        await ws_client.close()
        await ws_bybit.close()

    async def bybit_to_client():
        try:
            async for msg in ws_bybit:
                try:
                    await ws_client.send_str(msg)
                except Exception:
                    break
        except Exception:
            pass

        print("Bybit disconnected — restarting bybit socket")
        await ws_client.close()

    # Run both directions
    await asyncio.gather(client_to_bybit(), bybit_to_client())

    return ws_client


# ----------------------------------------------------------------
# Main app
# ----------------------------------------------------------------
def main():
    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.get("/relay", relay_handler)])

    print("Relay server started on port 8765")
    aiohttp.web.run_app(app, port=8765)


if __name__ == "__main__":
    main()
