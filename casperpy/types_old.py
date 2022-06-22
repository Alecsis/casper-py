import dataclasses
from sys import api_version
from typing import List, Optional
import enum
from abc import ABC, abstractclassmethod

class CL_TypeKey(enum.Enum):
    """
    Enumeration over set of CL type keys.
    """
    BOOL = 0
    I32 = 1
    I64 = 2
    U8 = 3
    U32 = 4
    U64 = 5
    U128 = 6
    U256 = 7
    U512 = 8
    UNIT = 9
    STRING = 10
    KEY = 11
    UREF = 12
    OPTION = 13
    LIST = 14
    BYTE_ARRAY = 15
    RESULT = 16
    MAP = 17
    TUPLE_1 = 18
    TUPLE_2 = 19
    TUPLE_3 = 20
    ANY = 21
    PUBLIC_KEY = 22



@dataclasses.dataclass
class ChainGetStateRootHashResponse:
    """
    The state root hash of the chain.
    """
    api_version: str
    state_root_hash: str

    @classmethod
    def from_json(cls, d: dict) -> "ChainGetStateRootHashResponse":
        """
        Create a ChainGetStateRootHashResponse from the API response.
        """
        return ChainGetStateRootHashResponse(
            api_version=d["api_version"],
            state_root_hash=d["state_root_hash"]
        )
    
@dataclasses.dataclass
class NamedKey:
    """
    A named key.
    """
    name: str
    key: str

@dataclasses.dataclass
class AssociatedKey:
    """
    An associated key.
    """

    account_hash: str
    weight: int

@dataclasses.dataclass
class ActionThresholds:
    """
    The action thresholds.
    """
    deployment: int
    key_management: int

@dataclasses.dataclass
class Account:
    """
    The account info of the public key.
    """
    account_hash: str
    named_keys: List[NamedKey]
    main_purse: str
    associated_keys: List[AssociatedKey]
    action_thresholds: ActionThresholds

@dataclasses.dataclass
class StateGetAccountInfoResponse:
    """
    The account info of the public key.
    """
    api_version: str
    account: Account
    merkle_proof: str

    @classmethod
    def from_json(cls, d: dict) -> 'StateGetAccountInfoResponse':
        """
        Create a StateGetAccountInfoResponse from the API response.
        """
        api_version=d['api_version']
        account = Account(
            account_hash=d["account"]["account_hash"],
            named_keys=[NamedKey(**key) for key in d["account"]["named_keys"]],
            main_purse=d["account"]["main_purse"],
            associated_keys=[AssociatedKey(**key) for key in d["account"]["associated_keys"]],
            action_thresholds=ActionThresholds(**d["account"]["action_thresholds"])
        )
        merkle_proof=d['merkle_proof']
        return cls(
            api_version,
            account,
            merkle_proof,
        )

@dataclasses.dataclass
class Approval:
    """
    The approval info deploy.
    """
    signature: str
    signer: str

    @classmethod
    def from_json(cls, d: dict) -> 'Approval':
        """
        Create an Approval from the API response.
        """
        return Approval(
            signature=d["signature"],
            signer=d["signer"]
        )

@dataclasses.dataclass
class DeployHeader:
    """
    The deploy header.
    """
    account: str
    body_hash: str
    chain_name: str
    dependencies: List[str]
    gas_price: int
    timestamp: str
    ttl: str

    @classmethod
    def from_json(cls, d: dict) -> 'DeployHeader':
        """
        Create a DeployHeader from the API response.
        """
        return DeployHeader(
            account=d["account"],
            body_hash=d["body_hash"],
            chain_name=d["chain_name"],
            dependencies=d["dependencies"],
            gas_price=d["gas_price"],
            timestamp=d["timestamp"],
            ttl=d["ttl"]
        )

@dataclasses.dataclass
class Transfer:
    """Represents a transfer from one purse to another."""
    amount: int
    deploy_hash: str
    sender: str
    """Sender is named `from` in the docs, but that's a reserved keyword."""
    gas: int
    id: Optional[int]
    source: str
    to: Optional[str]

@dataclasses.dataclass
class CLType:
    """A Casper value, i.e. a value which can be stored and manipulated by smart contracts.\n\nIt holds the underlying data as a type-erased, serialized `Vec<u8>` and also holds the CLType of the underlying data as a separate member.\n\nThe `parsed` field, representing the original value, is a convenience only available when a CLValue is encoded to JSON, and can always be set to null if preferred."""
    bytes: str
    cl_type: str
    parsed: Optional[str]

    @classmethod
    def from_json(cls, d: dict) -> 'CLType':
        """
        Create a CLType from the API response.
        """
        return CLType(
            bytes=d["bytes"],
            cl_type=d["cl_type"],
            parsed=d["parsed"] if "parsed" in d else None
        )

@dataclasses.dataclass
class NamedArg:
    """Named arguments to a contract."""
    name: str
    value: CLType

    @classmethod
    def from_json(cls, d: dict) -> 'NamedArg':
        """
        Create a NamedArg from the API response.
        """
        return NamedArg(
            name=d[0],
            value=CLType.from_json(d[1])
        )


class ExecutableDeployItem(ABC):
    @abstractclassmethod
    def from_json(cls, d: dict) -> 'ExecutableDeployItem':
        """
        Create an ExecutableDeployItem from the API response.
        """
        pass

    @abstractclassmethod
    def get_type() -> str:
        """
        Get the type of the deploy item.
        """
        pass

    @abstractclassmethod
    def describe(self) -> str:
        """
        Get the description of the deploy item.
        """
        pass

@dataclasses.dataclass
class ModuleBytes(ExecutableDeployItem):
    """ specified as raw bytes that represent WASM code and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    module_bytes: str
    """Hex-encoded raw Wasm bytes."""

    def get_type(self) -> str:
        return "module_bytes"

    def describe(self) -> str:
        return f"ModuleBytes, args: {self.args}, module_bytes: {self.module_bytes[:20]}..."

    @classmethod
    def from_json(cls, d: dict) -> 'ModuleBytes':
        """
        Create an ModuleBytes from the API response.
        """
        return ModuleBytes(
            args=list(map(NamedArg.from_json, d["args"])),
            module_bytes=d["module_bytes"]
        )

@dataclasses.dataclass
class StoredContractByHash(ExecutableDeployItem):
    """Stored contract referenced by its [`ContractHash`], entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    hash: str
    entry_point: str

    def get_type(self) -> str:
        return "stored_contract_by_hash"

    def describe(self) -> str:
        return f"StoredContractByHash, args: {self.args}, hash: {self.hash}, entry_point: {self.entry_point}"
    
    @classmethod
    def from_json(cls, d: dict) -> 'StoredContractByHash':
        """
        Create an StoredContractByHash from the API response.
        """
        return StoredContractByHash(
            args=list(map(NamedArg.from_json, d["args"])),
            hash=d["hash"],
            entry_point=d["entry_point"]
        )

@dataclasses.dataclass
class StoredContractByName(ExecutableDeployItem):
    """Stored contract referenced by a named key existing in the signer's account context, entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    name: str
    entry_point: str

    def get_type(self) -> str:
        return "stored_contract_by_name"

    def describe(self) -> str:
        return f"StoredContractByName, args: {self.args}, name: {self.name}, entry_point: {self.entry_point}"
    
    @classmethod
    def from_json(cls, d: dict) -> 'StoredContractByName':
        """
        Create an StoredContractByName from the API response.
        """
        return StoredContractByName(
            args=list(map(NamedArg.from_json, d["args"])),
            name=d["name"],
            entry_point=d["entry_point"]
        )

@dataclasses.dataclass
class StoredVersionedContractByHash(ExecutableDeployItem):
    """Stored versioned contract referenced by its [`ContractPackageHash`], entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    hash: str
    entry_point: str
    version: Optional[int]

    def get_type(self) -> str:
        return "stored_versioned_contract_by_hash"
    
    def describe(self) -> str:
        return f"StoredVersionedContractByHash, args: {self.args}, hash: {self.hash}, entry_point: {self.entry_point}, version: {self.version}"
    
    @classmethod
    def from_json(cls, d: dict) -> 'StoredVersionedContractByHash':
        """
        Create an StoredVersionedContractByHash from the API response.
        """
        return StoredVersionedContractByHash(
            args=list(map(NamedArg.from_json, d["args"])),
            hash=d["hash"],
            entry_point=d["entry_point"],
            version=d["version"]
        )

@dataclasses.dataclass
class StoredVersionedContractByName(ExecutableDeployItem):
    """Stored versioned contract referenced by its [`ContractPackageName`], entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    name: str
    entry_point: str
    version: Optional[int]

    def get_type(self) -> str:
        return "stored_versioned_contract_by_name"

    def describe(self) -> str:
        return f"StoredVersionedContractByName, args: {self.args}, name: {self.name}, entry_point: {self.entry_point}, version: {self.version}"
    
    @classmethod
    def from_json(cls, d: dict) -> 'StoredVersionedContractByName':
        """
        Create an StoredVersionedContractByName from the API response.
        """
        return StoredVersionedContractByName(
            args=list(map(NamedArg.from_json, d["args"])),
            name=d["name"],
            entry_point=d["entry_point"],
            version=d["version"]
        )


@dataclasses.dataclass
class Transfer(ExecutableDeployItem):
    """Stored versioned contract referenced by its [`ContractPackageName`], entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]

    def get_type(self) -> str:
        return "transfer"

    def describe(self) -> str:
        return f"Transfer, args: {self.args}"

    @classmethod
    def from_json(cls, d: dict) -> 'Transfer':
        """
        Create an Transfer from the API response.
        """
        return Transfer(
            args=list(map(NamedArg.from_json, d["args"]))
        )

@dataclasses.dataclass
class Operation:
    """
    The operation info deploy.
    """
    key: str
    kind: str # Write or Read

    @classmethod
    def from_json(cls, d: dict) -> 'Operation':
        return cls(
            key=d["key"],
            kind=d["kind"],
        )


@dataclasses.dataclass
class Transform:
    """
    The transforms info deploy.
    """
    key: str
    transform: str | dict

    @classmethod
    def from_json(cls, d: dict) -> 'Transform':
        return cls(
            key=d["key"],
            transform=d["transform"]
        )

@dataclasses.dataclass
class ExecutionEffect:
    """
    The execution effect info deploy.
    """
    operations: List[Operation]
    transforms: List[Transform]

    @classmethod
    def from_json(cls, d: dict) -> 'ExecutionEffect':
        return cls(
            operations=list(map(Operation.from_json, d["operations"])),
            transforms=list(map(Transform.from_json, d["transforms"])),
        )

@dataclasses.dataclass
class ExecutionResult(ABC):
    """
    The execution result type info deploy.
    """
    
    @abstractclassmethod
    def from_json(cls, d: dict) -> 'ExecutionResult':
        """
        Create an ExecutionResult from the API response.
        """
        pass

@dataclasses.dataclass
class ExecutionResultFailure(ExecutionResult):
    """
    The result of a failed execution.
    """
    cost: int
    effect: ExecutionEffect
    error_message: str
    transfers: List[str]

    @classmethod
    def from_json(cls, d: dict) -> 'ExecutionResultFailure':
        return cls(
            cost=d['cost'],
            effect=ExecutionEffect.from_json(d['effect']),
            error_message=d['error_message'],
            transfers=d['transfers']
        )


@dataclasses.dataclass
class ExecutionResultSuccess(ExecutionResult):
    """
    The result of a successful execution.
    """
    cost: int
    effect: ExecutionEffect
    transfers: List[str]

    @classmethod
    def from_json(cls, d: dict) -> 'ExecutionResultSuccess':
        return cls(
            cost=d['cost'],
            effect=ExecutionEffect.from_json(d['effect']),
            transfers=d['transfers']
        )

execution_result_type_map = {
    "Success": ExecutionResultSuccess,
    "Failure": ExecutionResultFailure
}

@dataclasses.dataclass
class ExecutionResultWrapper:
    """
    The execution result of a single deploy.
    """
    block_hash: str
    result: ExecutionResult

    @classmethod
    def from_json(cls, d: dict) -> 'ExecutionResultWrapper':
        result_name = list(d["result"].keys())[0]
        result_class = execution_result_type_map[result_name]
        result = result_class.from_json(d["result"][result_name])

        return cls(
            block_hash=d['block_hash'],
            result=result,
        )

deploy_item_type_map = {
    "ModuleBytes": ModuleBytes,
    "StoredContractByName": StoredContractByName,
    "StoredContractByHash": StoredContractByHash,
    "StoredVersionedContractByName": StoredVersionedContractByName,
    "StoredVersionedContractByHash": StoredVersionedContractByHash,
    "Transfer": Transfer,
}

@dataclasses.dataclass
class Deploy:
    """
    The deploy info of the deploy hash.
    """
    approvals: List[Approval]
    hash: str
    header: DeployHeader
    payment: ExecutableDeployItem
    session: ExecutableDeployItem

    @classmethod
    def from_json(cls, d: dict) -> 'Deploy':
        """
        Create a Deploy from the API response.
        """
        payment_name = list(d['payment'].keys())[0]
        session_name = list(d['session'].keys())[0]
        payment_class = deploy_item_type_map[payment_name]
        session_class = deploy_item_type_map[session_name]

        return cls(
            approvals=list(map(Approval.from_json, d['approvals'])),
            hash=d['hash'],
            header=DeployHeader.from_json(d['header']),
            payment=payment_class.from_json(d['payment'][payment_name]),
            session=session_class.from_json(d['session'][session_name])
        )

@dataclasses.dataclass
class InfoGetDeployResponse:
    """
    The deploy info of the deploy hash.
    """
    api_version: str
    deploy: Deploy
    execution_results: List[ExecutionResultWrapper]

    @classmethod
    def from_json(cls, d: dict) -> 'InfoGetDeployResponse':
        """
        Create a InfoGetDeployResponse from the API response.
        """
        return cls(
            api_version=d['api_version'],
            deploy=Deploy.from_json(d['deploy']),
            execution_results=list(map(ExecutionResultWrapper.from_json, d['execution_results']))
        )