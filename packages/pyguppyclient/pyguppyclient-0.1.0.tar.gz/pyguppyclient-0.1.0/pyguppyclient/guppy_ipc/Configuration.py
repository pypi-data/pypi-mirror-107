# automatically generated by the FlatBuffers compiler, do not modify

# namespace: guppy_ipc

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Configuration(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsConfiguration(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Configuration()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def ConfigurationBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x30\x30\x30\x32", size_prefixed=size_prefixed)

    # Configuration
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Configuration
    def QscoreOffset(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # Configuration
    def QscoreScale(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # Configuration
    def TempWeight(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # Configuration
    def TempBias(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # Configuration
    def ModelStride(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

    # Configuration
    def LabelLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint32Flags, o + self._tab.Pos)
        return 0

    # Configuration
    def ConfigName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(16))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Configuration
    def ModelType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

def ConfigurationStart(builder): builder.StartObject(8)
def ConfigurationAddQscoreOffset(builder, qscoreOffset): builder.PrependFloat32Slot(0, qscoreOffset, 0.0)
def ConfigurationAddQscoreScale(builder, qscoreScale): builder.PrependFloat32Slot(1, qscoreScale, 0.0)
def ConfigurationAddTempWeight(builder, tempWeight): builder.PrependFloat32Slot(2, tempWeight, 0.0)
def ConfigurationAddTempBias(builder, tempBias): builder.PrependFloat32Slot(3, tempBias, 0.0)
def ConfigurationAddModelStride(builder, modelStride): builder.PrependUint32Slot(4, modelStride, 0)
def ConfigurationAddLabelLength(builder, labelLength): builder.PrependUint32Slot(5, labelLength, 0)
def ConfigurationAddConfigName(builder, configName): builder.PrependUOffsetTRelativeSlot(6, flatbuffers.number_types.UOffsetTFlags.py_type(configName), 0)
def ConfigurationAddModelType(builder, modelType): builder.PrependUOffsetTRelativeSlot(7, flatbuffers.number_types.UOffsetTFlags.py_type(modelType), 0)
def ConfigurationEnd(builder): return builder.EndObject()
