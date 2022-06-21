from casperpy.types import ExecutableModuleBytes, ExecutableStoredContractByHash, ExecutableStoredContractByName, ExecutableStoredVersionedContractByHash, ExecutableStoredVersionedContractByName, ExecutableTransfer
from casperpy.client import Client, JRPCClient


def show_named_keys(client: Client, public_key: str) -> None:
    """
    Show the named keys of the account.
    """
    res = client.state_get_account_info(public_key)
    print("Named keys:")
    for named_key in res.account.named_keys:
        print(f"  {named_key.name}: {named_key.key}")

def show_state_root_hash(client: Client) -> None:
    """
    Show the state root hash of the chain.
    """
    res = client.chain_get_state_root_hash()
    print("State root hash:")
    print(f"  {res.state_root_hash}")

def show_deploy_info(client: Client, deploy_hash: str) -> None:
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

    

if __name__ == "__main__":
    public_key = "019df5db374352d8ba8d9f4ede91daccb8ad21c0cc662fb6a3552e63457dddf680"
    deploy_hash = "5abeb03d7c11dc1f1319f4b1c3f6d6d42222a06aae127e5762e991f58c6dab2f"
    client = JRPCClient("16.162.124.124", 7777)
    
    # show_state_root_hash(client)
    # show_named_keys(client, public_key)
    show_deploy_info(client, deploy_hash)

    
