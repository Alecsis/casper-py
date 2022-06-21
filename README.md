# casper-py

A SDK framework for the Casper Network blockchain. It is implementing a few methods to dialog with the network.

Example usage:

```py
from casperpy.client import Client, JRPCClient

def show_named_keys(client: Client, public_key: str) -> None:
    """
    Show the named keys of the account.
    """
    res = client.state_get_account_info(public_key)
    print("Named keys:")
    for named_key in res.account.named_keys:
        print(f"  {named_key.name}: {named_key.key}")

if __name__ == "__main__":
    public_key = "019df5db374352d8ba8d9f4ede91daccb8ad21c0cc662fb6a3552e63457dddf680"
    client = JRPCClient("16.162.124.124", 7777) # Testnet seed
    
    show_named_keys(client, public_key)
```

Roadmap:

- [x] chain_get_state_root_hash
- [x] info_get_deploy
- [x] state_get_account_info
- [ ] chain_get_block
- [ ] chain_get_block_transfers
- [ ] chain_get_state_root_hash
- [ ] chain_get_era_info_by_switch_block
- [ ] account_put_deploy
- [ ] info_get_peers
- [ ] info_get_status
- [ ] info_get_validator_changes
- [ ] state_get_item
- [ ] state_get_balance
- [ ] state_get_auction_info
- [ ] state_get_account_info
- [ ] state_get_dictionary_item
- [ ] query_global_state
- [ ] state_get_trie
