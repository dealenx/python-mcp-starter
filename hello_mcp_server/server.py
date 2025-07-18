import os
import sys
import anyio
import click
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

APP_ID = "hello-mcp-server"
mcp = FastMCP(APP_ID)

# Minimal Starlette app for SSE
starlette_app = Starlette(routes=[Mount("/", app=mcp.sse_app())])

# Example tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Runners
async def run_stdio():
    print("🚀 Запуск MCP сервера в режиме STDIO")
    print(f"📋 ID приложения: {APP_ID}")
    print(f"🐍 Версия Python: {sys.version}")
    print(f"📁 Рабочая директория: {os.getcwd()}")
    print(f"🔧 Переменные окружения:")
    for key in ['HOST', 'PORT', 'DEBUG']:
        value = os.getenv(key, 'не установлено')
        print(f"   {key}: {value}")
    print("📡 Ожидание подключения через STDIO...")
    await mcp.run_stdio_async()

def run_sse(host: str, port: int):
    print("🚀 Запуск MCP сервера в режиме SSE")
    print(f"📋 ID приложения: {APP_ID}")
    print(f"🐍 Версия Python: {sys.version}")
    print(f"📁 Рабочая директория: {os.getcwd()}")
    print(f"🌐 Хост: {host}")
    print(f"🔌 Порт: {port}")
    print(f"📍 URL сервера: http://{host}:{port}")
    print(f"🔧 Переменные окружения:")
    for key in ['HOST', 'PORT', 'DEBUG']:
        value = os.getenv(key, 'не установлено')
        print(f"   {key}: {value}")
    print("🎯 Запуск Uvicorn сервера...")
    uvicorn.run(starlette_app, host=host, port=port)

# CLI
@click.command()
@click.option("--sse", is_flag=True, help="Start as SSE server (otherwise stdio).")
@click.option("--host", default=lambda: os.getenv("HOST", "0.0.0.0"),
              show_default=True, help="Host for SSE mode")
@click.option("--port", type=int, default=lambda: int(os.getenv("PORT", 8000)),
              show_default=True, help="Port for SSE mode")
def main(sse: bool, host: str, port: int):
    print("=" * 50)
    print("🎉 Начался запуск MCP сервера")
    print("=" * 50)
    print(f"⚙️  Режим запуска: {'SSE' if sse else 'STDIO'}")
    print(f"🕐 Время запуска: {os.getenv('TZ', 'системное время')}")
    print(f"💻 Платформа: {sys.platform}")
    print(f"🏠 Домашняя директория: {os.path.expanduser('~')}")
    print("=" * 50)
    
    if sse:
        run_sse(host, port)
    else:
        anyio.run(run_stdio)

if __name__ == "__main__":
    main()
