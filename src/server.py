from blockchain import Blockchain
from flask import Flask, jsonify, request

# Mining the blockchain

## Create a webapp
app = Flask(__name__)

## Mine blocks
blockchain = Blockchain()

@app.route('/mine-block')
def mine_block():
    prev_block = blockchain.get_previous_block()
    prev_nonce = prev_block['nonce']
    nonce = blockchain.proof_of_work(prev_nonce)
    blk = blockchain.add_block(nonce, blockchain.hash(prev_block) )
    return jsonify({
        'msg': "Congrats! You've just mined a block",
        'index': blk['index'],
        'created': blk['created'],
        'nonce': blk['nonce'],
        'prev_block_hash': blk['prev_block_hash'],
    }), 200

# Get the blockchain and all the hashes associated with it. This method can suffer performance problems for big data entries
@app.route('/blockchain')
def get_blockchain():
    # We want to modify a copy, not the original blockchain as it will break everything 
    # (the "hash" attribute will change all the values when a block is "hashed")
    chain = blockchain.chain
    chain_copy = []
    for blk in chain:
        # blk['hash'] = blockchain.hash(blk)
        chain_copy.append({
            'index': blk['index'],
            'created': blk['created'],
            'nonce': blk['nonce'],
            'prev_block_hash': blk['prev_block_hash'],
            'hash': blockchain.hash(blk),
        })
    return jsonify({
        'chain': chain_copy,
        'length': len(chain)
    }), 200

# Validate the blockchain and expose and HTTP request for the user to do so
@app.route('/is-valid')
def is_blockchain_valid():
    return jsonify({
        'status': 'The blockchain is valid :D' if blockchain.is_chain_valid() else 'Oops, blockchain is invalid'
    }), 200

@app.post('/hash-block')
def hash_block():
    print('the request', request)
    req = request.get_json(force=True)
    created = req['created']
    index = req['index']
    nonce = req['nonce']
    prev_block_hash = req['prev_block_hash']
    block = {
        'created': created,
        'index': index,
        'nonce': nonce,
        'prev_block_hash': prev_block_hash,
    }
    res = {
        'hash': blockchain.hash(block)
    }
    return jsonify(res), 200

@app.post('/check-proof')
def check_proof():
    req = request.get_json(force=True)
    nonce = req['nonce']
    prev_block_hash = req['prev_block_hash']

    if blockchain.is_chain_valid() == False:
        return jsonify({
            'msg': "This blockchain is invalid, needs to be fixed before checking any proof"
        }), 409
    elif prev_block_hash == '0'*64:
        return jsonify({
            'msg': "Cannot check a block before the first one. Please change the 'prev_block_hash' value."
        }), 409

    # Check proof by using the formula. Avoid checking first block because its proof is automatic.
    # Check all the blocks, assuming the list order doesn't necessarily represents the blockchain order.
    prev_nonce = -1
    blk_index = 0
    for blk in blockchain.chain:
        if blockchain.hash(blk) == prev_block_hash:
            prev_nonce = blk['nonce']
            break
        blk_index += 1

    if prev_nonce == -1:
        return jsonify({
            'msg': "Couldn't check proof, please be sure not to pass the first block's info"
        }), 409

    is_valid = blockchain.check_proof(nonce, prev_nonce)
    return jsonify({
        'msg': 'Everything ok with this proof' if is_valid else 'This is NOT a valid proof'
    }), 200

app.run(host='0.0.0.0', port=5000)

