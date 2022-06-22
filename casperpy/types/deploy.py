import dataclasses
import enum
import typing
import abc

import casperpy.types.cl_types as cl_types
import casperpy.types.cl_values as cl_values
import casperpy.types.crypto as crypto_types

@dataclasses.dataclass
class DeployArgument:
    """
    An argument to be passed to vm for execution.
    """
    name: str
    """Argument name mapped to an entry point parameter."""
    value: cl_values.CL_Value

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.value == other.value

    def encode_value(self) -> bytes:
        """
        Encode the argument to a byte array.
        """
        print(f"Encoding argument {self.name}")
        return cl_values.CL_String(self.name).encode_value() + \
        cl_values.encode_u8_array(self.value.encode_value()) + \
        self.value.encode_type()
    
@dataclasses.dataclass
class DeployExecutableItem:
    """
    Encapsulates VM execution information.
    """
    
    args: typing.Union[typing.List[DeployArgument], typing.Dict[str, cl_values.CL_Value]]

    def __eq__(self, other: object) -> bool:
        return self.args == other.args

    @property
    def args_list(self) -> typing.List[DeployArgument]:
        """
        Returns a list of arguments.
        """
        if isinstance(self.args, dict):
            return [DeployArgument(name=key, value=value) for key, value in self.args.items()]
        elif isinstance(self.args, list):
            return self.args
        else:
            raise ValueError("Invalid type for args: {}".format(type(self.args)))

@dataclasses.dataclass
class ModuleBytes(DeployExecutableItem):
    """
    Module bytes.
    """
    raw_wasm_payload: bytes = dataclasses.field(default_factory=bytes)

    def __eq__(self, other: object) -> bool:
        return self.raw_wasm_payload == other.raw_wasm_payload

    def encode_value(self) -> bytes:
        leading_byte = bytes([0])
        length_byte = cl_values.CL_U32(len(self.raw_wasm_payload)).encode_value()
        return bytes([0]) \
            + cl_values.encode_u8_array(self.raw_wasm_payload)\
            + cl_values.encode_vector([arg.encode_value() for arg in self.args_list])

@dataclasses.dataclass
class DeployApproval:
    """
    Digital signature for a deploy.
    """
    signer: str
    """Account that signed the deploy."""
    signature: bytes
    signature_type = crypto_types.KeyAlgorithm

    def __eq__(self, other: object) -> bool:
        return self.signer == other.signer and self.signature == other.signature and self.signature_type == other.signature_type

    @property
    def signature_with_type(self) -> bytes:
        return self.signature_type.value + self.signature


@dataclasses.dataclass
class Deploy:
    """
    Information required to interact with chain.
    """

    approvals: typing.List[DeployApproval]
    hash: bytes
    payment: DeployExecutableItem
    session: DeployExecutableItem

    def __eq__(self, other: object) -> bool:
        return self.approvals == other.approvals and self.hash == other.hash and self.payment == other.payment and self.session == other.session