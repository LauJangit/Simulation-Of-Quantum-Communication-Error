# coding=utf-8
import socket;
import time;


def encode(str):
    return ''.join([bin(ord(char)).replace('0b', '0') for char in str])


def checkSum(data):
    sum = 0;
    byteData = bytearray(data)
    for i in range(0, len(byteData)):
        if (byteData[i] == 48):
            sum = sum + 0;
        if (byteData[i] == 49):
            sum = sum + 1;
    if sum % 2 == 0:
        return 0;
    else:
        return 1;


def compare(string):
    global conn
    global key
    conn.send(str(checkSum(string)).encode());
    data = conn.recv(1024).decode();
    if data == str(0):
        key = key + string
        print(streamtobyte(key) + "\n" + str(qw(key)))
        return 1;
    else:
        return 0;
        # return 0;#不同
        # return 1;#相同


def frontHalfLength(string):
    if len(string) % 2 == 0:
        return len(string) / 2;
    if len(string) % 2 == 1:
        return len(string) / 2 + 1;


def behindHalfLength(string):
    if len(string) % 2 == 0:
        return len(string) / 2;
    if len(string) % 2 == 1:
        return len(string) / 2;


def check(linkList, data):
    begin = linkList[0][0];
    end = linkList[0][1];
    data = data[begin:end];
    del linkList[0];
    if len(data) <= 2:
        return linkList;
    if not compare(data[0:frontHalfLength(data)]):
        linkList.insert(0, (begin, begin + frontHalfLength(data)));
    if not compare(data[behindHalfLength(data):]):
        linkList.insert(0, (begin + behindHalfLength(data), begin + len(data)));
    # print(str(frontHalfLength(data))+","+str(behindHalfLength(data))+","+str(len(data)))
    return linkList;


def process(data):
    # print(data);
    linkList = [(0, len(data))];
    while not len(linkList) == 0:
        print(linkList)
        check(linkList, data);


def getKey(Port):
    address = ('127.0.0.1', Port);
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.connect(address);
    data = s.recv(1024).decode();
    s.close();
    # print(data)
    return data;


def linkSocket(Port):
    address = ('127.0.0.1', Port);
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.connect(address);
    return s;


def streamtobyte(stream):
    string = "";
    byteNum = len(stream) / 8;
    List = [];
    for i in range(0, byteNum):
        List.append(stream[i * 8:i * 8 + 8])
    for i in List:
        string = string + decode("0b" + i);
    return string;


def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])


def qw(stream):
    string = "";
    byteNum = len(stream) / 8;
    List = [];
    for i in range(0, byteNum):
        List.append(stream[i * 8:i * 8 + 8])
    return List;


# start
global conn
conn = linkSocket(20000);
global key
key = ""
process(encode(getKey(10001)));

print(streamtobyte(key));
