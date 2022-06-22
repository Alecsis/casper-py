import dataclasses
import enum
import typing
import abc

import casperpy.types.cl_types as cl_types
import casperpy.types.crypto as crypto_types

KEY_ACCOUNT_PREFIX = "account-hash"
KEY_HASH_PREFIX = "hash"
KEY_UREF_PREFIX = "uref"

class CL_TypeKey(enum.Enum):
    """
    Enumeration over set of CL type keys.
    """
    ANY = 21
    BOOL = 0
    BYTE_ARRAY = 15
    I32 = 1
    I64 = 2
    KEY = 11
    LIST = 14
    MAP = 17
    OPTION = 13
    PUBLIC_KEY = 22
    RESULT = 16
    STRING = 10
    TUPLE_1 = 18
    TUPLE_2 = 19
    TUPLE_3 = 20
    U8 = 3
    U32 = 4
    U64 = 5
    U128 = 6
    U256 = 7
    U512 = 8
    UNIT = 9
    UREF = 12

@dataclasses.dataclass
class CL_Value(abc.ABC):
    """
    CL value.
    """
    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    def encode_value(self) -> bytes:
        """
        Encode the value to a byte array.
        """
        raise NotImplementedError()

    @staticmethod
    def encode_type() -> bytes:
        """
        Encode the type of the value to a byte array.
        """
        raise NotImplementedError()


@dataclasses.dataclass
class CL_Any(CL_Value):
    """
    CL type for any value.
    """
    value: object

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

@dataclasses.dataclass
class CL_Bool(CL_Value):
    """
    CL type for boolean value.
    """
    value: bool

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

@dataclasses.dataclass
class CL_ByteArray(CL_Value):
    """
    CL type for byte array value.
    """
    value: bytes

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

@dataclasses.dataclass
class CL_Int(CL_Value):
    """
    CL type for integer value.
    """
    value: int

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

@dataclasses.dataclass
class CL_I32(CL_Int):
    """
    CL type for 32-bit integer value.
    """
    pass


@dataclasses.dataclass
class CL_I64(CL_Int):
    """
    CL type for 32-bit integer value.
    """
    pass

@dataclasses.dataclass
class CL_KeyType(enum.Enum):
    """
    CL type for key type.
    """
    ACCOUNT = 0
    HASH = 1
    UREF = 2

    @staticmethod
    def from_key(key: str) -> 'CL_KeyType':
        if key.startswith(KEY_ACCOUNT_PREFIX):
            return CL_KeyType.ACCOUNT
        elif key.startswith(KEY_HASH_PREFIX):
            return CL_KeyType.HASH
        elif key.startswith(KEY_UREF_PREFIX):
            return CL_KeyType.UREF
        else:
            raise ValueError(f"Invalid key: {key}")
    
    def __str__(self) -> str:
        if self == CL_KeyType.ACCOUNT:
            return KEY_ACCOUNT_PREFIX
        elif self == CL_KeyType.HASH:
            return KEY_HASH_PREFIX
        elif self == CL_KeyType.UREF:
            return KEY_UREF_PREFIX
        else:
            raise ValueError(f"Invalid key type: {self}")
        

@dataclasses.dataclass
class CL_Key(CL_Value):
    """
    CL type for key value.
    """
    key_type: CL_KeyType
    value: bytes
    """ 32 bytes key """

    def __eq__(self, other: object) -> bool:
        return self.value == other.value and self.key_type == other.key_type

    @staticmethod
    def from_string(key: str) -> 'CL_Key':
        """
        Create CL_Key from string. Key could be in format:
        - account-hash-0c92e754d41013212318d26be504e0f491199b92bdf4ca375b92f8986d1cfd3c
        - hash-0c92e754d41013212318d26be504e0f491199b92bdf4ca375b92f8986d1cfd3c
        - uref-0c92e754d41013212318d26be504e0f491199b92bdf4ca375b92f8986d1cfd3c
        """
        hex = key.split('-')[-1]
        value = bytes.fromhex(hex)
        key_type = CL_KeyType.from_key(key)
        return CL_Key(key_type, value)
    

@dataclasses.dataclass
class CL_List(CL_Value):
    """
    CL type for list value.
    """
    value: typing.List[CL_Value]

    def __eq__(self, other: object) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CL_Map(CL_Value):
    """
    CL type for map value. Key and value are CL_Value.
    """
    value: typing.List[typing.Tuple[CL_Value, CL_Value]]

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

@dataclasses.dataclass
class CL_Union(CL_Value):
    """
    CL type for union value.
    """
    value: typing.Optional[CL_Value]
    option_type: cl_types.CL_Type

    def __eq__(self, other: object) -> bool:
        return self.value == other.value and self.option_type == other.option_type

@dataclasses.dataclass
class CL_PublicKey(CL_Value):
    """
    CL type for public key value.
    """
    value: bytes
    algo: crypto_types.KeyAlgorithm

    def __eq__(self, other: object) -> bool:
        return self.value == other.value and self.algo == other.algo

@dataclasses.dataclass
class CL_Result(CL_Value):
    """
    CL type for result value coming from a function call.
    """
    value: object

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

@dataclasses.dataclass
class CL_String(CL_Value):
    """
    CL type for string value.
    """
    value: str

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

    def encode_value(self) -> bytes:
        """
        Encode the value to a byte array.
        """
        encoded: bytes = (self.value or "").encode("utf-8")
        return CL_U32(len(encoded)).encode_value() + encoded

@dataclasses.dataclass
class CL_U8(CL_Int):
    """
    CL type for 8-bit integer value.
    """
    pass

@dataclasses.dataclass
class CL_U16(CL_Int):
    """
    CL type for 16-bit integer value.
    """
    pass

@dataclasses.dataclass
class CL_U32(CL_Int):
    """
    CL type for 32-bit integer value.
    """
    
    def encode_value(self) -> bytes:
        return encode_int(self.value, (4, ), signed=False, trim=False)

@dataclasses.dataclass
class CL_U64(CL_Int):
    """
    CL type for 64-bit integer value.
    """
    pass

@dataclasses.dataclass
class CL_U128(CL_Int):
    """
    CL type for 128-bit integer value.
    """
    pass

@dataclasses.dataclass
class CL_U256(CL_Int):
    """
    CL type for 256-bit integer value.
    """
    pass

@dataclasses.dataclass
class CL_U512(CL_Int):
    """
    CL type for 512-bit integer value.
    """

    def encode_value(self) -> bytes:
        return encode_int(self.value, (1, 4, 8, 16, 32, 64), signed=False, trim=True)
    
    @staticmethod
    def encode_type() -> bytes:
        return bytes([CL_TypeKey.U512.value])

@dataclasses.dataclass
class CL_Unit(CL_Value):
    """
    CL type for unit value (none value).
    """
    pass

@dataclasses.dataclass
class CL_UrefAccessRights(enum.Enum):
    """
    CL type for uref access rights value.
    """

    NONE = 0
    READ = 1
    WRITE = 2
    ADD = 4
    READ_WRITE = 3
    READ_ADD = 5
    ADD_WRITE = 6
    READ_ADD_WRITE = 7

@dataclasses.dataclass
class CL_Uref(CL_Value):
    """
    CL type for uref value.
    """
    value: str
    access_rights: CL_UrefAccessRights

    def __eq__(self, other: object) -> bool:
        return self.value == other.value and self.access_rights == other.access_rights
    
    @staticmethod
    def from_string(uref: str) -> 'CL_Uref':
        """
        Create CL_Uref from string. Uref could be in format:
        - uref-0c92e754d41013212318d26be504e0f491199b92bdf4ca375b92f8986d1cfd3c-0
        """
        parts = uref.split('-')
        access_rights = CL_UrefAccessRights(int(parts[-1]))
        value = bytes.fromhex(parts[-2])
        return CL_Uref(value, access_rights)

def encode_u8_array(values: typing.List[int]) -> bytes:
    """
    Encode list of 8-bit integers into bytes.
    """
    return CL_U32(len(values)).encode_value() + bytes(values)

def encode_vector(values: typing.List) -> bytes:
    """
    Encode list of CL_Value into bytes.
    """
    return CL_U32(len(values)).encode_value() + bytes([i for j in values for i in j])

def encode_int(
    value: int,
    byte_lengths: typing.List[int],
    signed: bool,
    trim: bool
) -> bytes:
    """
    Encode integer value into bytes.
    """
    encoded = None
    for length in byte_lengths:
        try:
            value = int(value)
            encoded = value.to_bytes(length, "little", signed=signed)
        except OverflowError:
            continue

    if encoded is None:
        raise ValueError("Invalid integer: max size exceeded")

    if trim:
        while encoded and encoded[-1] == 0:
            encoded = encoded[0:-1]

    if len(byte_lengths) == 1:
        return encoded
    else:
        return bytes([len(encoded)]) + encoded