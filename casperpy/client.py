from dataclasses import dataclass
import requests
import jsonrpcclient
from abc import ABC, abstractmethod
from .types import ChainGetStateRootHashResponse, StateGetAccountInfoResponse, InfoGetDeployResponse
from .constants import CHAIN_GET_STATE_ROOT_HASH, STATE_GET_ACCOUNT_INFO, INFO_GET_DEPLOY

class Client(ABC):
    @abstractmethod
    def send(self, method: str, params: dict) -> dict:
        """
        Send a JSON RPC request to the client.
        """
        pass

    @abstractmethod
    def chain_get_state_root_hash(self) -> ChainGetStateRootHashResponse:
        """
        Get the state root hash of the chain.
        """
        pass

    @abstractmethod
    def state_get_account_info(self, public_key: str) -> StateGetAccountInfoResponse:
        """
        Get the account info of the public key.
        """
        pass

    @abstractmethod
    def info_get_deploy(self, deploy_hash: str) -> InfoGetDeployResponse:
        """
        Get the deploy info of the deploy hash.
        """
        pass

@dataclass
class JRPCClient(Client):
    """
    Client class for the Casper API.
    """
    host: str
    port: int

    @property
    def rpc_url(self) -> str:
        """
        The JSON RPC URL for the client.
        """
        return f"http://{self.host}:{self.port}/rpc"

    def send(self, method: str, params: dict) -> dict:
        """
        Send a JSON RPC request to the client.
        """
        req = jsonrpcclient.request(method, params)
        res = requests.post(self.rpc_url, json=req)
        return jsonrpcclient.parse(res.json()).result
    
    def chain_get_state_root_hash(self) -> ChainGetStateRootHashResponse:
        """
        Get the state root hash of the chain.
        """
        res = self.send(CHAIN_GET_STATE_ROOT_HASH, {})
        return ChainGetStateRootHashResponse.from_api(res)
    
    def state_get_account_info(self, public_key: str) -> StateGetAccountInfoResponse:
        """
        Get the account info of the public key.
        """
        res = self.send(STATE_GET_ACCOUNT_INFO, {"public_key": public_key})
        return StateGetAccountInfoResponse.from_api(res)
    
    def info_get_deploy(self, deploy_hash: str) -> InfoGetDeployResponse:
        res = self.send(INFO_GET_DEPLOY, {"deploy_hash": deploy_hash})
        return InfoGetDeployResponse.from_api(res)