# automatically generated by the FlatBuffers compiler, do not modify

# namespace: LogSerialization

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class StatusChange(object):
    __slots__ = ['_tab']

    @classmethod
    def SizeOf(cls):
        return 16

    # StatusChange
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # StatusChange
    def Uid(self): return self._tab.Get(flatbuffers.number_types.Uint16Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # StatusChange
    def PrevStatus(self): return self._tab.Get(flatbuffers.number_types.Int8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(2))
    # StatusChange
    def Status(self): return self._tab.Get(flatbuffers.number_types.Int8Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(3))
    # StatusChange
    def Timestamp(self, obj):
        obj.Init(self._tab.Bytes, self._tab.Pos + 8)
        return obj


def CreateStatusChange(builder, uid, prevStatus, status, timestamp_usecSinceEpoch):
    builder.Prep(8, 16)
    builder.Prep(8, 8)
    builder.PrependUint64(timestamp_usecSinceEpoch)
    builder.Pad(4)
    builder.PrependInt8(status)
    builder.PrependInt8(prevStatus)
    builder.PrependUint16(uid)
    return builder.Offset()