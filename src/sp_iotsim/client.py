import websockets
import zlib

from pathlib import Path


async def main(port: int, addr: str, max_packets: int, log_file: Path = None):
    """
    Parameters
    ----------
    port: int
        the network port to use (arbitrary, must match server)
    addr: str
        the address of the server (localhost if on same computer)
    max_packets: int
        to avoid using all the hard drive if the client is left running,
        we set a maximum number of packets before shutting the client down
    log_file: pathlib.Path
        where to store the data received (student must add code for this)
    """
    if log_file:
        log_file = Path(log_file).expanduser()
    uri = f"ws://{addr}:{port}"
    async with websockets.connect(uri) as websocket:
        qb = await websocket.recv()
        if isinstance(qb, bytes):
            print(zlib.decompress(qb).decode("utf8"))
        else:
            print(qb)

        f = open('data.txt','w')
        for i in range(max_packets):
            data = await websocket.recv()
            if i % 5 == 0:
                pass
                # print(f"{i} total messages received")
            f.write(data + "\n")
            print(data)
            f.flush()
        f.close()


def cli():
    p = argparse.ArgumentParser(description="WebSocket client")
    p.add_argument("-l", "--log", help="file to log JSON data")
    p.add_argument("-host", help="Host address", default="localhost")
    p.add_argument("-port", help="network port", type=int, default=8765)
    p.add_argument(
        "-max_packets",
        help="shut down program after total packages received",
        type=int,
        default=100000,
    )
    P = p.parse_args()
    try:
        asyncio.run(main(P.port, P.host, P.max_packets, P.log))
    except KeyboardInterrupt:
        print(P.log)
if __name__ == "__main__":
    cli()
