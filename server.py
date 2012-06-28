from gevent.server import StreamServer
import os
import threading


def mangodb(socket, address):
    socket.sendall('HELLO\r\n')
    client = socket.makefile()
    output = open('/dev/null', 'w')
    lock = threading.Lock()
    while 1:
        line = client.readline()
        if not line:
            break
        cmd_bits = line.split(' ', 1)
        cmd = cmd_bits[0]
        if cmd == 'BYE':
            break
        if len(cmd_bits) > 1:
            lock.acquire(True)
            output.write(cmd_bits[1])
            if os.environ.get('MANGODB_DURABLE', False):
                output.flush()
                os.fsync(output.fileno())
            lock.release()
            client.write('OK' + os.urandom(1024).encode('string-escape') + '\r\n')
        client.flush()


if __name__ == '__main__':
    server = StreamServer(('0.0.0.0', 27017), mangodb)
    print ('Starting MangoDB on port 27017')
    server.serve_forever()
