# generated from rosidl_generator_py/resource/_idl.py.em
# with input from drone_slam:msg/ElevationGrid.idl
# generated code does not contain a copyright notice

from __future__ import annotations

import collections.abc
import os
import typing

import rosidl_pycommon.interface_base_classes

if typing.TYPE_CHECKING:
    from ctypes import Structure

    class PyCapsule(Structure):
        pass  # don't need to define the full structure


# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
ros_python_check_fields = os.getenv('ROS_PYTHON_CHECK_FIELDS', default='')


if typing.TYPE_CHECKING:
    import geometry_msgs.msg  # noqa: E402, I100, I201, I300
    import std_msgs.msg  # noqa: E402, I100, I201, I300


# Import statements for member types

# Member 'state'
# Member 'z_min'
# Member 'z_max'
# Member 'hits'
import array  # noqa: E402, I100

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ElevationGrid(rosidl_pycommon.interface_base_classes.MessageTypeSupportMeta):
    """Metaclass of message 'ElevationGrid'."""

    _CREATE_ROS_MESSAGE: typing.ClassVar[typing.Optional[PyCapsule]] = None
    _CONVERT_FROM_PY: typing.ClassVar[typing.Optional[PyCapsule]] = None
    _CONVERT_TO_PY: typing.ClassVar[typing.Optional[PyCapsule]] = None
    _DESTROY_ROS_MESSAGE: typing.ClassVar[typing.Optional[PyCapsule]] = None
    _TYPE_SUPPORT: typing.ClassVar[typing.Optional[PyCapsule]] = None

    class ElevationGridConstants(typing.TypedDict):
        pass

    __constants: ElevationGridConstants = {
    }

    @classmethod
    def __import_type_support__(cls) -> None:
        try:
            from rosidl_generator_py import import_type_support  # type: ignore[attr-defined]
            module = import_type_support('drone_slam')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'drone_slam.msg.ElevationGrid')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__elevation_grid
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__elevation_grid
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__elevation_grid
            cls._TYPE_SUPPORT = module.type_support_msg__msg__elevation_grid
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__elevation_grid

            from geometry_msgs.msg import Pose
            if Pose._TYPE_SUPPORT is None:
                Pose.__import_type_support__()

            from std_msgs.msg import Header
            if Header._TYPE_SUPPORT is None:
                Header.__import_type_support__()

    @classmethod
    def __prepare__(metacls, name: str, bases: tuple[type[typing.Any], ...], /, **kwds: typing.Any) -> collections.abc.MutableMapping[str, object]:
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ElevationGrid(rosidl_pycommon.interface_base_classes.BaseMessage, metaclass=Metaclass_ElevationGrid):
    """Message class 'ElevationGrid'."""

    __slots__ = [
        '_header',
        '_resolution',
        '_width',
        '_height',
        '_origin',
        '_state',
        '_z_min',
        '_z_max',
        '_hits',
        '_check_fields',
    ]

    _fields_and_field_types: dict[str, str] = {
        'header': 'std_msgs/Header',
        'resolution': 'float',
        'width': 'uint32',
        'height': 'uint32',
        'origin': 'geometry_msgs/Pose',
        'state': 'sequence<uint8>',
        'z_min': 'sequence<float>',
        'z_max': 'sequence<float>',
        'hits': 'sequence<uint32>',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES: tuple[rosidl_parser.definition.AbstractType, ...] = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint8')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('float')),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint32')),  # noqa: E501
    )

    def __init__(self, *,
                 header: typing.Optional[std_msgs.msg.Header] = None,  # noqa: E501
                 resolution: typing.Optional[float] = None,  # noqa: E501
                 width: typing.Optional[int] = None,  # noqa: E501
                 height: typing.Optional[int] = None,  # noqa: E501
                 origin: typing.Optional[geometry_msgs.msg.Pose] = None,  # noqa: E501
                 state: typing.Optional[collections.abc.Sequence[int]] = None,  # noqa: E501
                 z_min: typing.Optional[collections.abc.Sequence[float]] = None,  # noqa: E501
                 z_max: typing.Optional[collections.abc.Sequence[float]] = None,  # noqa: E501
                 hits: typing.Optional[collections.abc.Sequence[int]] = None,  # noqa: E501
                 check_fields: typing.Optional[bool] = None) -> None:
        if check_fields is not None:
            self._check_fields = check_fields
        else:
            self._check_fields = ros_python_check_fields == '1'
        from std_msgs.msg import Header
        self.header = header if header is not None else Header()
        self.resolution = resolution if resolution is not None else float()
        self.width = width if width is not None else int()
        self.height = height if height is not None else int()
        from geometry_msgs.msg import Pose
        self.origin = origin if origin is not None else Pose()
        self.state = state if state is not None else array.array('B', [])
        self.z_min = z_min if z_min is not None else array.array('f', [])
        self.z_max = z_max if z_max is not None else array.array('f', [])
        self.hits = hits if hits is not None else array.array('I', [])

    def __repr__(self) -> str:
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args: list[str] = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    from rosidl_buffer import Buffer as _RosidlBuffer
                    if not isinstance(field, _RosidlBuffer):
                        if self._check_fields:
                            assert fieldstr.startswith('array(')
                        prefix = "array('X', "
                        suffix = ')'
                        fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ElevationGrid):
            return False
        if self.header != other.header:
            return False
        if self.resolution != other.resolution:
            return False
        if self.width != other.width:
            return False
        if self.height != other.height:
            return False
        if self.origin != other.origin:
            return False
        if self.state != other.state:
            return False
        if self.z_min != other.z_min:
            return False
        if self.z_max != other.z_max:
            return False
        if self.hits != other.hits:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls) -> dict[str, str]:
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self) -> std_msgs.msg.Header:
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value: std_msgs.msg.Header) -> None:
        from std_msgs.msg import Header

        if self._check_fields:
            if False:  # Done for templating alignment
                pass
            else:
                assert \
                    isinstance(value, Header), \
                    "The 'header' field must be a sub message of type 'Header'"

        self._header = value

    @builtins.property
    def resolution(self) -> float:
        """Message field 'resolution'."""
        return self._resolution

    @resolution.setter
    def resolution(self, value: float) -> None:

        if self._check_fields:
            if False:  # Done for templating alignment
                pass
            else:
                assert \
                    isinstance(value, float), \
                    "The 'resolution' field must be of type 'float'"
                assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                    "The 'resolution' field must be a float in [-3.402823466e+38, 3.402823466e+38]"

        self._resolution = value

    @builtins.property
    def width(self) -> int:
        """Message field 'width'."""
        return self._width

    @width.setter
    def width(self, value: int) -> None:

        if self._check_fields:
            if False:  # Done for templating alignment
                pass
            else:
                assert \
                    isinstance(value, int), \
                    "The 'width' field must be of type 'int'"
                assert value >= 0 and value < 4294967296, \
                    "The 'width' field must be an unsigned integer in [0, 4294967295]"

        self._width = value

    @builtins.property
    def height(self) -> int:
        """Message field 'height'."""
        return self._height

    @height.setter
    def height(self, value: int) -> None:

        if self._check_fields:
            if False:  # Done for templating alignment
                pass
            else:
                assert \
                    isinstance(value, int), \
                    "The 'height' field must be of type 'int'"
                assert value >= 0 and value < 4294967296, \
                    "The 'height' field must be an unsigned integer in [0, 4294967295]"

        self._height = value

    @builtins.property
    def origin(self) -> geometry_msgs.msg.Pose:
        """Message field 'origin'."""
        return self._origin

    @origin.setter
    def origin(self, value: geometry_msgs.msg.Pose) -> None:
        from geometry_msgs.msg import Pose

        if self._check_fields:
            if False:  # Done for templating alignment
                pass
            else:
                assert \
                    isinstance(value, Pose), \
                    "The 'origin' field must be a sub message of type 'Pose'"

        self._origin = value

    @builtins.property
    def state(self) -> typing.Annotated[typing.Any, array.array[int]]:   # typing.Annotated can be remove after mypy 1.16+ see mypy#3004
        """Message field 'state'."""
        return self._state

    @state.setter
    def state(self, value: collections.abc.Sequence[int]) -> None:
        if isinstance(value, collections.abc.Set):
            import warnings
            warnings.warn(
                'Using set or subclass of set is deprecated,'
                ' please use a subclass of collections.abc.Sequence like list',
                DeprecationWarning)
        from rosidl_buffer import Buffer as _RosidlBuffer
        if isinstance(value, _RosidlBuffer):
            self._state = value  # type: ignore[assignment]
            return

        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'B', \
                    "The 'state' array.array() must have the type code of 'B'"
            else:
                assert \
                    ((isinstance(value, collections.abc.Sequence) or
                     isinstance(value, collections.abc.Set)) and
                     not isinstance(value, str) and
                     not isinstance(value, collections.UserString) and
                     all(isinstance(v, int) for v in value) and
                     all(val >= 0 and val < 256 for val in value)), \
                    "The 'state' field must be sequence and each value of type 'int' and each unsigned integer in [0, 255]"

        if isinstance(value, array.array):
            self._state = value  # type: ignore[assignment]
            return
        # type ignore below fixed in mypy 1.17+ see mypy#19421
        self._state = array.array('B', value)  # type: ignore[assignment]

    @builtins.property
    def z_min(self) -> typing.Annotated[typing.Any, array.array[float]]:   # typing.Annotated can be remove after mypy 1.16+ see mypy#3004
        """Message field 'z_min'."""
        return self._z_min

    @z_min.setter
    def z_min(self, value: collections.abc.Sequence[float]) -> None:
        if isinstance(value, collections.abc.Set):
            import warnings
            warnings.warn(
                'Using set or subclass of set is deprecated,'
                ' please use a subclass of collections.abc.Sequence like list',
                DeprecationWarning)

        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'f', \
                    "The 'z_min' array.array() must have the type code of 'f'"
            else:
                assert \
                    ((isinstance(value, collections.abc.Sequence) or
                     isinstance(value, collections.abc.Set)) and
                     not isinstance(value, str) and
                     not isinstance(value, collections.UserString) and
                     all(isinstance(v, float) for v in value) and
                     all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                    "The 'z_min' field must be sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"

        if isinstance(value, array.array):
            self._z_min = value
            return
        # type ignore below fixed in mypy 1.17+ see mypy#19421
        self._z_min = array.array('f', value)  # type: ignore[assignment]

    @builtins.property
    def z_max(self) -> typing.Annotated[typing.Any, array.array[float]]:   # typing.Annotated can be remove after mypy 1.16+ see mypy#3004
        """Message field 'z_max'."""
        return self._z_max

    @z_max.setter
    def z_max(self, value: collections.abc.Sequence[float]) -> None:
        if isinstance(value, collections.abc.Set):
            import warnings
            warnings.warn(
                'Using set or subclass of set is deprecated,'
                ' please use a subclass of collections.abc.Sequence like list',
                DeprecationWarning)

        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'f', \
                    "The 'z_max' array.array() must have the type code of 'f'"
            else:
                assert \
                    ((isinstance(value, collections.abc.Sequence) or
                     isinstance(value, collections.abc.Set)) and
                     not isinstance(value, str) and
                     not isinstance(value, collections.UserString) and
                     all(isinstance(v, float) for v in value) and
                     all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                    "The 'z_max' field must be sequence and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"

        if isinstance(value, array.array):
            self._z_max = value
            return
        # type ignore below fixed in mypy 1.17+ see mypy#19421
        self._z_max = array.array('f', value)  # type: ignore[assignment]

    @builtins.property
    def hits(self) -> typing.Annotated[typing.Any, array.array[int]]:   # typing.Annotated can be remove after mypy 1.16+ see mypy#3004
        """Message field 'hits'."""
        return self._hits

    @hits.setter
    def hits(self, value: collections.abc.Sequence[int]) -> None:
        if isinstance(value, collections.abc.Set):
            import warnings
            warnings.warn(
                'Using set or subclass of set is deprecated,'
                ' please use a subclass of collections.abc.Sequence like list',
                DeprecationWarning)

        if self._check_fields:
            if isinstance(value, array.array):
                assert value.typecode == 'I', \
                    "The 'hits' array.array() must have the type code of 'I'"
            else:
                assert \
                    ((isinstance(value, collections.abc.Sequence) or
                     isinstance(value, collections.abc.Set)) and
                     not isinstance(value, str) and
                     not isinstance(value, collections.UserString) and
                     all(isinstance(v, int) for v in value) and
                     all(val >= 0 and val < 4294967296 for val in value)), \
                    "The 'hits' field must be sequence and each value of type 'int' and each unsigned integer in [0, 4294967295]"

        if isinstance(value, array.array):
            self._hits = value
            return
        # type ignore below fixed in mypy 1.17+ see mypy#19421
        self._hits = array.array('I', value)  # type: ignore[assignment]
