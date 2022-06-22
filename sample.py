import datetime
import hashlib 
from typing import List
import enum
from hashlib import blake2b

import casperpy.types.deploy as deploy_types
import casperpy.types.cl_values as cl_values
import casperpy.types.cl_types as cl_types
import casperpy.client as casper_client


def show_named_keys(client: casper_client.Client, public_key: str) -> None:
    """
    Show the named keys of the account.
    """
    res = client.state_get_account_info(public_key)
    print("Named keys:")
    for named_key in res.account.named_keys:
        print(f"  {named_key.name}: {named_key.key}")

def show_state_root_hash(client: casper_client.Client) -> None:
    """
    Show the state root hash of the chain.
    """
    res = client.chain_get_state_root_hash()
    print("State root hash:")
    print(f"  {res.state_root_hash}")

def show_deploy_info(client: casper_client.Client, deploy_hash: str) -> None:
    """
    Show the deploy info of the deploy hash.
    """
    res = client.info_get_deploy(deploy_hash)
    print("Deploy info:")
    print(f"  Hash: {res.deploy.hash}")
    print(f"  Header:")
    print(f"    Account: {res.deploy.header.account}")
    print(f"    Chain: {res.deploy.header.chain_name}")
    print(f"    Timestamp: {res.deploy.header.timestamp}")
    print(f"  Approvals:")
    for approval in res.deploy.approvals:
        print(f"    Signer: {approval.signer} -> {approval.signature}")
    print(f"  Payment: {res.deploy.payment.describe()}")
    print(f"  Session: {res.deploy.session.describe()}")
    print(f"  Execution results:")
    for execution_result in res.execution_results:
        if execution_result.error_message:
            print(f"    {execution_result.error_message}")
        else:
            print(f"    {execution_result}")


class ERC20_INSTANTIATION_PARAMETERS(enum.Enum):
    """
    ERC20 entry points.
    """
    TOKEN_DECIMALS = "token_decimals"
    TOKEN_NAME = "token_name"
    TOKEN_SYMBOL = "token_symbol"
    TOKEN_INITIAL_SUPPLY = "token_initial_supply"

    

if __name__ == "__main__":
    public_key = "019df5db374352d8ba8d9f4ede91daccb8ad21c0cc662fb6a3552e63457dddf680"
    deploy_hash = "5abeb03d7c11dc1f1319f4b1c3f6d6d42222a06aae127e5762e991f58c6dab2f"
    client = casper_client.JRPCClient("16.162.124.124", 7777)
    
    # show_state_root_hash(client)
    # show_named_keys(client, public_key)
    # show_deploy_info(client, deploy_hash)

    # res = client.info_get_deploy(deploy_hash)
    # print(res)
    
    # Create deploy
    deploy_args = {
        'path_to_operator_secret_key': './wallet/secret_key.pem',
        'path_to_operator_public_key': './wallet/public_key.pem',
        'type_of_operator_secret_key': 'ED25519',
        'path_to_wasm': './erc20.wasm',
        'chain_name': 'casper-test',
        'deploy_payment': 50000000000, 
        'node_host': '16.162.124.124',
        'node_port_rpc': 7777, 
        'token_decimals': 11, 
        'token_name': 'Acme Token',
        'token_total_supply': 1000000000000000.0, 
        'token_symbol': 'ACME'
    }

    with open(deploy_args['path_to_operator_secret_key'], 'r') as f:
        secret_key = f.read()
    
    with open(deploy_args['path_to_operator_public_key'], 'r') as f:
        public_key = f.read()

    params = {
        'account_public_key': public_key,
        'chain_name': deploy_args['chain_name'],
        'timestamp': round(datetime.datetime.now(tz=datetime.timezone.utc).timestamp(), 3),
        'ttl': 3600_000,
        'dependencies': [],
    }

    payment = deploy_types.ModuleBytes(
        args = {
            "amount": cl_values.CL_U512(deploy_args['deploy_payment']),
        }
    )

    session = deploy_types.ModuleBytes(
        args = {
            ERC20_INSTANTIATION_PARAMETERS.TOKEN_DECIMALS: cl_values.CL_U8(deploy_args['token_decimals']),
            ERC20_INSTANTIATION_PARAMETERS.TOKEN_NAME: cl_values.CL_String(deploy_args['token_name']),
            ERC20_INSTANTIATION_PARAMETERS.TOKEN_SYMBOL: cl_values.CL_String(deploy_args['token_symbol']),
            ERC20_INSTANTIATION_PARAMETERS.TOKEN_INITIAL_SUPPLY: cl_values.CL_U256(deploy_args['token_total_supply']),
        },
        raw_wasm_payload=open(deploy_args['path_to_wasm'], 'rb').read(),
    )

    # b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\x06\x00\x00\x00amount\x06\x00\x00\x00\x05\x00t;\xa4\x0b\x08'
    res = payment.encode_value()
    print(res)

    # Create body
    # hash_payload = payment.encode_value() + session.encode_value()
    # hash = hashlib.blake2b(b'', digest_size=32).hexdigest()

    # Create header