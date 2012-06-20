from gevent.server import StreamServer
import os


def mangodb(socket, address):
    socket.sendall('HELLO\r\n')
    client = socket.makefile()
    output = open('/dev/null', 'w')
    while True:
        line = client.readline()
        if not line:
            break
        cmd_bits = line.split(' ', 1)
        cmd = cmd_bits[0]
        if cmd == 'BYE':
            break
        if len(cmd_bits) > 1:
            output.write(cmd_bits[1])
            client.write('OK' + os.urandom(1024) + '\r\n')
        client.flush()


if __name__ == '__main__':
    server = StreamServer(('0.0.0.0', 6000), mangodb)
    print ('Starting MangoDB on port 6000')
    server.serve_forever()
