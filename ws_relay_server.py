# ============================================================
# BYBIT WS RELAY v1.0
# ------------------------------------------------------------
# Принимает WebSocket от клиента
# Открывает WebSocket к Bybit
# Пересылает клиенту реальные тикеры
# Полный GEO-bypass (KZ, TR, UAE, EU restrictions)
# ============================================================

import asyncio
import json
import websockets
import aiohttp
import aiohttp.web

BYBIT_WS = "wss://stream.bybit.com/v5/public/spot"


async def relay_handler(request):
    ws_client = aiohttp.web.WebSocketResponse()
    await ws_client.prepare(request)

    async with websockets.connect(BYBIT_WS, ssl=None) as ws_bybit:

        async def client_to_bybit():
            async for msg in ws_client:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    await ws_bybit.send(msg.data)

        async def bybit_to_client():
            async for msg in ws_bybit:
                await ws_client.send_str(msg)

        await asyncio.gather(client_to_bybit(), bybit_to_client())

    return ws_client


def main():
    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.get("/relay", relay_handler)])
    aiohttp.web.run_app(app, port=8765)


if __name__ == "__main__":
    main()
