from dataclasses import dataclass
from typing import List, Optional
from abc import ABC, abstractclassmethod

@dataclass
class ChainGetStateRootHashResponse:
    """
    The state root hash of the chain.
    """
    api_version: str
    state_root_hash: str

    @classmethod
    def from_api(cls, api_response: dict) -> "ChainGetStateRootHashResponse":
        """
        Create a ChainGetStateRootHashResponse from the API response.
        """
        return ChainGetStateRootHashResponse(
            api_version=api_response["api_version"],
            state_root_hash=api_response["state_root_hash"]
        )

@dataclass
class NamedKey:
    """
    A named key.
    """
    name: str
    key: str

@dataclass
class AssociatedKey:
    """
    An associated key.
    """

    account_hash: str
    weight: int

@dataclass
class ActionThresholds:
    """
    The action thresholds.
    """
    deployment: int
    key_management: int

@dataclass
class Account:
    """
    The account info of the public key.
    """
    account_hash: str
    named_keys: List[NamedKey]
    main_purse: str
    associated_keys: List[AssociatedKey]
    action_thresholds: ActionThresholds

@dataclass
class StateGetAccountInfoResponse:
    """
    The account info of the public key.
    """
    api_version: str
    account: Account
    merkle_proof: str

    @classmethod
    def from_api(cls, api_response: dict) -> 'StateGetAccountInfoResponse':
        """
        Create a StateGetAccountInfoResponse from the API response.
        """
        api_version=api_response['api_version']
        account = Account(
            account_hash=api_response["account"]["account_hash"],
            named_keys=[NamedKey(**key) for key in api_response["account"]["named_keys"]],
            main_purse=api_response["account"]["main_purse"],
            associated_keys=[AssociatedKey(**key) for key in api_response["account"]["associated_keys"]],
            action_thresholds=ActionThresholds(**api_response["account"]["action_thresholds"])
        )
        merkle_proof=api_response['merkle_proof']
        return cls(
            api_version,
            account,
            merkle_proof,
        )

@dataclass
class Approval:
    """
    The approval info deploy.
    """
    signature: str
    signer: str

@dataclass
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

@dataclass
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

@dataclass
class CLType:
    """A Casper value, i.e. a value which can be stored and manipulated by smart contracts.\n\nIt holds the underlying data as a type-erased, serialized `Vec<u8>` and also holds the CLType of the underlying data as a separate member.\n\nThe `parsed` field, representing the original value, is a convenience only available when a CLValue is encoded to JSON, and can always be set to null if preferred."""
    bytes: str
    cl_type: str

@dataclass
class NamedArg:
    """Named arguments to a contract."""
    type: str
    value: CLType
    """Named $ref in the docs."""


class ExecutableDeployItem(ABC):
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

@dataclass
class ExecutableModuleBytes(ExecutableDeployItem):
    """Executable specified as raw bytes that represent WASM code and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    module_bytes: str
    """Hex-encoded raw Wasm bytes."""

    def get_type(self) -> str:
        return "module_bytes"

    def describe(self) -> str:
        return f"ExecutableModuleBytes, args: {self.args}, module_bytes: {self.module_bytes[:20]}..."

@dataclass
class ExecutableStoredContractByHash(ExecutableDeployItem):
    """Stored contract referenced by its [`ContractHash`], entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    hash: str
    entry_point: str

    def get_type(self) -> str:
        return "stored_contract_by_hash"

    def describe(self) -> str:
        return f"ExecutableStoredContractByHash, args: {self.args}, hash: {self.hash}, entry_point: {self.entry_point}"

@dataclass
class ExecutableStoredContractByName(ExecutableDeployItem):
    """Stored contract referenced by a named key existing in the signer's account context, entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    name: str
    entry_point: str

    def get_type(self) -> str:
        return "stored_contract_by_name"

    def describe(self) -> str:
        return f"ExecutableStoredContractByName, args: {self.args}, name: {self.name}, entry_point: {self.entry_point}"

@dataclass
class ExecutableStoredVersionedContractByHash(ExecutableDeployItem):
    """Stored versioned contract referenced by its [`ContractPackageHash`], entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    hash: str
    entry_point: str
    version: Optional[int]

    def get_type(self) -> str:
        return "stored_versioned_contract_by_hash"
    
    def describe(self) -> str:
        return f"ExecutableStoredVersionedContractByHash, args: {self.args}, hash: {self.hash}, entry_point: {self.entry_point}, version: {self.version}"

@dataclass
class ExecutableStoredVersionedContractByName(ExecutableDeployItem):
    """Stored versioned contract referenced by its [`ContractPackageName`], entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]
    name: str
    entry_point: str
    version: Optional[int]

    def get_type(self) -> str:
        return "stored_versioned_contract_by_name"

    def describe(self) -> str:
        return f"ExecutableStoredVersionedContractByName, args: {self.args}, name: {self.name}, entry_point: {self.entry_point}, version: {self.version}"


@dataclass
class ExecutableTransfer(ExecutableDeployItem):
    """Stored versioned contract referenced by its [`ContractPackageName`], entry point and an instance of [`RuntimeArgs`]."""
    args: List[NamedArg]

    def get_type(self) -> str:
        return "transfer"

    def describe(self) -> str:
        return f"ExecutableTransfer, args: {self.args}"

@dataclass
class Operation:
    """
    The operation info deploy.
    """
    key: str
    kind: str # Write or Read

@dataclass
class Transform:
    """
    The transforms info deploy.
    """
    key: str
    transform: str | dict

@dataclass
class ExecutionEffect:
    """
    The execution effect info deploy.
    """
    operations: List[Operation]
    transforms: List[Transform]

@dataclass
class ExecutionResult:
    """
    The execution result. Not really matching the API definition but cleaner.
    """
    block_hash: str
    cost: str
    effect: ExecutionEffect
    error_message: str
    transfers: List[str]

@dataclass
class Deploy:
    """
    The deploy info of the deploy hash.
    """
    approvals: List[Approval]
    hash: str
    header: DeployHeader
    payment: ExecutableDeployItem
    session: ExecutableDeployItem

@dataclass
class InfoGetDeployResponse:
    """
    The deploy info of the deploy hash.
    """
    api_version: str
    deploy: Deploy
    execution_results: List[ExecutionResult]

    @classmethod
    def from_api(cls, api_response: dict) -> 'InfoGetDeployResponse':
        """
        Create a InfoGetDeployResponse from the API response.
        """
        api_version=api_response['api_version']
        approvals = [Approval(**approval) for approval in api_response['deploy']['approvals']]
        header = DeployHeader(**api_response['deploy']['header'])
        payment_type = list(api_response['deploy']['payment'].keys())[0]

        # Payment is tricky, it can be a lot of different things.
        if payment_type == 'StoredContractByName':
            payment = ExecutableStoredContractByName(**api_response['deploy']['payment'][payment_type])
        elif payment_type == 'StoredContractByHash':
            payment = ExecutableStoredContractByHash(**api_response['deploy']['payment'][payment_type])
        elif payment_type == 'StoredVersionedContractByName':
            payment = ExecutableStoredVersionedContractByName(**api_response['deploy']['payment'][payment_type])
        elif payment_type == 'StoredVersionedContractByHash':
            payment = ExecutableStoredVersionedContractByHash(**api_response['deploy']['payment'][payment_type])
        elif payment_type == 'ModuleBytes':
            payment = ExecutableModuleBytes(**api_response['deploy']['payment'][payment_type])
        elif payment_type == 'Transfer':
            payment = ExecutableTransfer(**api_response['deploy']['payment'][payment_type])
        else:
            raise ValueError(f'Unknown payment type: {payment_type}')

        # Same for session.
        session_type = list(api_response['deploy']['session'].keys())[0]
        if session_type == 'StoredContractByName':
            session = ExecutableStoredContractByName(**api_response['deploy']['session'][session_type])
        elif session_type == 'StoredContractByHash':
            session = ExecutableStoredContractByHash(**api_response['deploy']['session'][session_type])
        elif session_type == 'StoredVersionedContractByName':
            session = ExecutableStoredVersionedContractByName(**api_response['deploy']['session'][session_type])
        elif session_type == 'StoredVersionedContractByHash':
            session = ExecutableStoredVersionedContractByHash(**api_response['deploy']['session'][session_type])
        elif session_type == 'ModuleBytes':
            session = ExecutableModuleBytes(**api_response['deploy']['session'][session_type])
        elif session_type == 'Transfer':
            session = ExecutableTransfer(**api_response['deploy']['session'][session_type])

        raw_results = api_response['execution_results']
        execution_results: List[ExecutionResult] = []
        for result in raw_results:
            hash = result['block_hash']
            is_success = "Success" in result["result"]
            result_type = "Success" if is_success else "Failure"
            cost = result['result'][result_type]['cost']
            operations = [Operation(**operation) for operation in result['result'][result_type]['effect']['operations']]
            transforms = [Transform(**transform) for transform in result['result'][result_type]['effect']['transforms']]
            transfers = result['result'][result_type]['transfers']
            
            execution_result = ExecutionResult(
                block_hash=hash,
                cost=cost,
                effect=ExecutionEffect(
                    operations=operations,
                    transforms=transforms,
                ),
                error_message = result['result'][result_type]['error_message'] if not is_success else None,
                transfers=transfers,
            )
            execution_results.append(execution_result)

        deploy = Deploy(
            approvals=approvals,
            hash=api_response['deploy']['hash'],
            header=header,
            payment=payment,
            session=session,
        )
        return cls(
            api_version=api_version,
            deploy=deploy,
            execution_results=execution_results,
        )
        