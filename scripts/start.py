#!/usr/bin/python
import nftables

def add_nftables_chain_entry(table_name, chain_name, entry):
    # Initialize the nftables object
    nft = nftables.Nftables()
    
    # Add the entry to the specified chain
    cmd = {
        "nftables": [
            {"add": {"rule": {"family": "inet", "table": table_name, "chain": chain_name, "expr": entry}}}
        ]
    }
    
    try:
        nft.json_validate(cmd)
    except Exception as e:
        print(f"ERROR: failed validating json schema: {e}")
        exit(1)

    # Run the command
    rc, output, error = nft.json_cmd(cmd)
    if rc != 0:
        # do proper error handling here, exceptions etc
        print(f"ERROR: running json_cmd: {error}")
        exit(1)

    if len(output) != 0:
        # more error control?
        print(f"WARNING: output: {output}")

# Example usage
table_name = "SuchaFW"
chain_name = "forward_users_lan"
entry = [{"match": {"left": {"payload": {"protocol": "ip", "field": "daddr"}}, "op": "==", "right": "192.168.1.1"}}, {"accept": None}]

add_nftables_chain_entry(table_name, chain_name, entry)
