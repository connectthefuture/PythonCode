import asyncio

@asyncio.coroutine
def simple_echo_server():
    # Start a socket server, call back for each client connected.
    # The client_connected_handler coroutine will be automatically converted to a Task
    yield from asyncio.start_server(client_connected_handler, 'localhost', 2222)

@asyncio.coroutine
def client_connected_handler(client_reader, client_writer):
    # Runs for each client connected
    # client_reader is a StreamReader object
    # client_writer is a StreamWriter object
    print("Connection received!")
    while True:
        data = yield from client_reader.read(8192)
        if not data:
            break
        print(data)
        client_writer.write(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(simple_echo_server())
try:
    loop.run_forever()
finally:
    loop.close()
