import asyncio

LASTLINE = b'Last line.\n'


@asyncio.coroutine
def simple_echo_client():
    # Open a connection and write a few lines by using the StreamWriter object
    reader, writer = yield from asyncio.open_connection('localhost', 2222)
    # reader is a StreamReader object
    # writer is a StreamWriter object
    writer.write(b'First line.\n')
    writer.write(b'Second line.\n')
    writer.write(b'Third line.\n')
    writer.write(LASTLINE)

    # Now, read a few lines by using the StreamReader object
    print("Lines received")
    while True:
        line = yield from reader.readline()
        print(line)
        if line == LASTLINE or not line:
            break
    writer.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(simple_echo_client())
