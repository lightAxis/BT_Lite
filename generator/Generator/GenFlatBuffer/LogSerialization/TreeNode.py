# automatically generated by the FlatBuffers compiler, do not modify

# namespace: LogSerialization

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class TreeNode(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = TreeNode()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsTreeNode(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # TreeNode
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # TreeNode
    def Uid(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint16Flags, o + self._tab.Pos)
        return 0

    # TreeNode
    def ChildrenUid(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint16Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 2))
        return 0

    # TreeNode
    def ChildrenUidAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint16Flags, o)
        return 0

    # TreeNode
    def ChildrenUidLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # TreeNode
    def ChildrenUidIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

    # TreeNode
    def Status(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # TreeNode
    def InstanceName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # TreeNode
    def RegistrationName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # TreeNode
    def PortRemaps(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from LogSerialization.PortConfig import PortConfig
            obj = PortConfig()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # TreeNode
    def PortRemapsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # TreeNode
    def PortRemapsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        return o == 0

def Start(builder): builder.StartObject(6)
def TreeNodeStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddUid(builder, uid): builder.PrependUint16Slot(0, uid, 0)
def TreeNodeAddUid(builder, uid):
    """This method is deprecated. Please switch to AddUid."""
    return AddUid(builder, uid)
def AddChildrenUid(builder, childrenUid): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(childrenUid), 0)
def TreeNodeAddChildrenUid(builder, childrenUid):
    """This method is deprecated. Please switch to AddChildrenUid."""
    return AddChildrenUid(builder, childrenUid)
def StartChildrenUidVector(builder, numElems): return builder.StartVector(2, numElems, 2)
def TreeNodeStartChildrenUidVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartChildrenUidVector(builder, numElems)
def AddStatus(builder, status): builder.PrependInt8Slot(2, status, 0)
def TreeNodeAddStatus(builder, status):
    """This method is deprecated. Please switch to AddStatus."""
    return AddStatus(builder, status)
def AddInstanceName(builder, instanceName): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(instanceName), 0)
def TreeNodeAddInstanceName(builder, instanceName):
    """This method is deprecated. Please switch to AddInstanceName."""
    return AddInstanceName(builder, instanceName)
def AddRegistrationName(builder, registrationName): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(registrationName), 0)
def TreeNodeAddRegistrationName(builder, registrationName):
    """This method is deprecated. Please switch to AddRegistrationName."""
    return AddRegistrationName(builder, registrationName)
def AddPortRemaps(builder, portRemaps): builder.PrependUOffsetTRelativeSlot(5, flatbuffers.number_types.UOffsetTFlags.py_type(portRemaps), 0)
def TreeNodeAddPortRemaps(builder, portRemaps):
    """This method is deprecated. Please switch to AddPortRemaps."""
    return AddPortRemaps(builder, portRemaps)
def StartPortRemapsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def TreeNodeStartPortRemapsVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartPortRemapsVector(builder, numElems)
def End(builder): return builder.EndObject()
def TreeNodeEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)