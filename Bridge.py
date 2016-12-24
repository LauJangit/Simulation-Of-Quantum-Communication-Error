import socket
import sys
import threading
from time import ctime, sleep
import random


def connSocket(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen(1)
    return sock;


def transferMsg(conn1, conn2, ErrRate):
    try:
        while True:
            recv = conn1.recv(1024).decode().encode();
            if recv.decode() == "":
                continue;
            else:
                rate = int(float(ErrRate) / 100.0 * float(len(recv)));
                data = bytearray(recv)
                while rate > 0:
                    randNum = random.randint(0, len(recv) - 1)
                    data[randNum] = randomChar();
                    rate = rate - 1;
                print(str(data));
                conn2.send(str(data));
    except:
        print("CATCH EXCEPTION");
        conn1.close();
        conn2.close();


def randomChar():
    randNum = random.randint(0, 127)
    return chr(randNum);


def action(alicePort, bobPort, bitErrorRate):
    try:
        aliceConn = connSocket(alicePort);
        bobConn = connSocket(bobPort);
    except:
        print("Bind Failed!");
        aliceConn.close()
        bobConn.close()
        sys.exit(0)

    print("Bind Succeed!\nWaiting For Connection...\n");
    aliceConnection, aliceAddress = aliceConn.accept()
    print("Alice Bilded");
    bobConnection, bobAddress = bobConn.accept()
    print("Bob Bilded");

    threads = []
    t1 = threading.Thread(target=transferMsg, args=(aliceConnection, bobConnection, bitErrorRate))
    threads.append(t1)
    t2 = threading.Thread(target=transferMsg, args=(bobConnection, aliceConnection, bitErrorRate))
    threads.append(t2)
    if __name__ == '__main__':
        for t in threads:
            t.setDaemon(True)
            t.start()
    action(alicePort, bobPort, bitErrorRate);


# start
alicePort = 0;
bobPort = 0;
bitErrorRate = 0;
try:
    alicePort = int(sys.argv[1]);
    bobPort = int(sys.argv[2]);
    bitErrorRate = int(sys.argv[3]);
except:
    print("Using Default Setting...");
    alicePort = 10000;
    bobPort = 10001;
    bitErrorRate = 30;

print("The Alice Port is " + str(alicePort));
print("The Bob Port is " + str(bobPort));
print("Bit Error Rate is " + str(bitErrorRate));
print("Binding.....\n");
while True:
    try:
        action(alicePort, bobPort, bitErrorRate)
    except:
        print("GET EXCEPTION!!!!!!");
        continue;

connection.close()
