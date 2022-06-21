from casperpy.types import InfoGetDeployResponse

def parse_deploy_info() -> InfoGetDeployResponse:
    """
    Parse the deploy info.
    """
    print("[+] Parsing deploy info...")
    mock_deploy_info = {
        "api_version": "1.4.6",
        "deploy": {
            "approvals": [
                {
                    "signature": "012dbf03817a51794a8e19e0724884075e6d1fbec326b766ecfa6658b41f81290da85e23b24e88b1c8d9761185c961daee1adab0649912a6477bcd2e69bd91bd08",
                    "signer": "01d9bf2148748a85c89da5aad8ee0b0fc2d105fd39d41a4c796536354f0ae2900c"
                }
            ],
            "hash": "5c9b3b099c1378aa8e4a5f07f59ff1fcdc69a83179427c7e67ae0377d94d93fa",
            "header": {
                "account": "01d9bf2148748a85c89da5aad8ee0b0fc2d105fd39d41a4c796536354f0ae2900c",
                "body_hash": "d53cf72d17278fd47d399013ca389c50d589352f1a12593c0b8e01872a641b50",
                "chain_name": "casper-example",
                "dependencies": [
                    "0101010101010101010101010101010101010101010101010101010101010101"
                ],
                "gas_price": 1,
                "timestamp": "2020-11-17T00:39:24.072Z",
                "ttl": "1h"
            },
            "payment": {
                "StoredContractByName": {
                    "args": [
                        [
                            "amount",
                            {
                                "bytes": "e8030000",
                                "cl_type": "I32",
                                "parsed": 1000
                            }
                        ]
                    ],
                    "entry_point": "example-entry-point",
                    "name": "casper-example"
                }
            },
            "session": {
                "Transfer": {
                    "args": [
                        [
                            "amount",
                            {
                                "bytes": "e8030000",
                                "cl_type": "I32",
                                "parsed": 1000
                            }
                        ]
                    ]
                }
            }
        },
        "execution_results": [
            {
                "block_hash": "6b5db3585233ed0076910d3a81fa7d23fc4325f35e06d31f293043aef3f4c98d",
                "result": {
                    "Success": {
                        "cost": "123456",
                        "effect": {
                            "operations": [
                                {
                                    "key": "account-hash-2c4a11c062a8a337bfc97e27fd66291caeb2c65865dcb5d3ef3759c4c97efecb",
                                    "kind": "Write"
                                },
                                {
                                    "key": "deploy-af684263911154d26fa05be9963171802801a0b6aff8f199b7391eacb8edc9e1",
                                    "kind": "Read"
                                }
                            ],
                            "transforms": [
                                {
                                    "key": "uref-2c4a11c062a8a337bfc97e27fd66291caeb2c65865dcb5d3ef3759c4c97efecb-007",
                                    "transform": {
                                        "AddUInt64": 8
                                    }
                                },
                                {
                                    "key": "deploy-af684263911154d26fa05be9963171802801a0b6aff8f199b7391eacb8edc9e1",
                                    "transform": "Identity"
                                }
                            ]
                        },
                        "transfers": [
                        "transfer-5959595959595959595959595959595959595959595959595959595959595959",
                        "transfer-8282828282828282828282828282828282828282828282828282828282828282"
                        ]
                    }
                }
            }
        ]
    }
    return InfoGetDeployResponse.from_api(mock_deploy_info)

if __name__ == "__main__":
    parse_deploy_info()
    print("Tests passed successfully.")
