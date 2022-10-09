#!usr/bin/env python3

from dataclasses import dataclass
from typing import List, Dict, Tuple

import struct
import ctypes


import os

from flatbuffer_python import flatbuffers
from LogSerialization import BehaviorTree
from LogSerialization import NodeModel
from LogSerialization import NodeStatus
from LogSerialization import NodeType
from LogSerialization import PortConfig
from LogSerialization import PortDirection
from LogSerialization import PortModel
from LogSerialization import StatusChange
from LogSerialization import StatusChangeLog
from LogSerialization import Timestamp
from LogSerialization import TreeNode


@dataclass
class log_t:
    time: int
    uid: int
    prevState: int
    nowState: int


def Merge():
    pass


def ParseLogs(fileContent: bytes) -> List[log_t]:

    pass


def ParseLog(fileContent: bytes, offset: int) -> Tuple[List[log_t], int]:

    index = 0
    len = 2
    index = offset

    len = 2
    logLenByte = fileContent[index:index+len]
    index = index + len

    len = 8
    nowByte = fileContent[index:index+len]
    index = index + len

    logLen = int.from_bytes(logLenByte, byteorder='little', signed=False)
    now = int.from_bytes(nowByte, byteorder='little', signed=False)
    logCount = int(logLen / 2)
    Logs: List[log_t] = []
    for i in range(0, logCount):
        len = 2
        logSegcon = fileContent[index:index+len]
        index = index + len
        logSeg = int.from_bytes(logSegcon, byteorder='little', signed=False)
        # print(hex(logSeg))

        uid = logSeg & 0x0FFF
        uid = ctypes.c_uint16(uid).value
        prevState = (logSeg & 0x3000) >> 12
        prevState = ctypes.c_uint8(prevState).value
        nowState = (logSeg & 0xC000) >> 14
        nowState = ctypes.c_uint8(nowState).value

        tempLog: log_t = log_t(
            time=now, uid=uid, prevState=prevState, nowState=nowState)
        Logs.append(tempLog)

    return Logs, index
    pass


def GenerateLogByteArray(logs: List[log_t]) -> bytearray:
    result: bytearray = bytearray()
    for log in logs:
        result.extend(ConvertToFlatBufferLogByte(log))
    return result
    pass


def ConvertToFlatBufferLogByte(log: log_t) -> int:
    t_sec = int(log.time / 1000000)
    t_sec = struct.pack("I", t_sec)

    t_usec = int(log.time % 1000000)
    t_usec = struct.pack("I", t_usec)

    UID = struct.pack("H", log.uid)
    prev_status = struct.pack("B", log.prevState)
    now_status = struct.pack("B", log.nowState)

    result = bytearray(t_sec)
    result.extend(bytearray(t_usec))
    result.extend(bytearray(UID))
    result.extend(bytearray(prev_status))
    result.extend(bytearray(now_status))

    return result
    pass


if __name__ == "__main__":

    BTBuffer = open(os.path.dirname(os.path.dirname(
        os.path.dirname(__file__)))+"/Tree.fbl", "rb")
    BTContent = BTBuffer.read()
    BTBytes = bytearray(BTContent)
    BTBuffer.close()

    logBuffer = open("/home/jiseok/gitlab/BT_Lite/build/test.bin", 'rb')
    fileContent = logBuffer.read()
    fileContentLen = fileContent.__len__()

    totalLogs: List[log_t] = []
    offset = 0
    while True:
        if fileContentLen <= offset:
            break
        else:
            newLogs, offset = ParseLog(fileContent=fileContent, offset=offset)
            totalLogs.extend(newLogs)

    LogBytes: bytearray = GenerateLogByteArray(totalLogs)
    logBuffer.close()

    resultBuffer = open("mergedLog.fbl", 'wb')
    resultBuffer.write(BTBytes)
    resultBuffer.write(LogBytes)
    resultBuffer.close()
    pass
