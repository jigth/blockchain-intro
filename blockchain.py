#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 10:55:04 2022

@author: jigth

Module 1 - Create a blockchain. Taken and adapted (written by hand) from:
    Blockchain & Cryptocurrency A-Z Complete Masterclass | Learn How To Build 
    Your First Blockchain
"""

# Libraries used in the tutorial (except for 'timezone')
from datetime import datetime, timezone
import hashlib
import json

# Building the blockchain...
class Blockchain:
    def __init__(self):
        self.chain = [] # List with all the blocks
        self.LEADING_ZEROES = 4
        self.add_block(1, '0'*64)
    
    def print_blockchain(self):
        print('\n\n')
        print('Blockchain', self.chain)

    def get_previous_block(self):
        return self.chain[-1]

    def add_block(self, nonce, prev_block_hash):
        block = {
            'index': len(self.chain) + 1,                   # Number
            'created': str( datetime.now(timezone.utc) ),   # Timestamp (convertable to UTC date)
            'nonce': nonce,                                 # Number
            'prev_block_hash': prev_block_hash,             # SHA256
        }
        self.chain.append(block)
        return block
    
    def check_proof(self, nonce, prev_nonce):
        proof_formula = nonce**5 + 2*nonce - (5+prev_nonce) ** 99
        block_hash = hashlib.sha256( json.dumps(proof_formula, sort_keys=True).encode() ).hexdigest()
        return block_hash[:self.LEADING_ZEROES] == '0'*self.LEADING_ZEROES
            
    # Returns the block with the calculated "nonce" when it has been mined
    def proof_of_work(self, prev_nonce):
        nonce = 0 # "nonce" A.K.A "proof value"
        was_found = False
        while was_found is not True:
            is_proof_valid = self.check_proof(nonce, prev_nonce)
            if is_proof_valid:
                was_found = True
            else:
                nonce += 1
        return nonce

    # Get a block hash based on its information. 'block' argument should be an object.
    def hash(self, block):
        block_encoded_str = json.dumps(block, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_encoded_str)
        return block_hash.hexdigest()

    # Checks for each block of the chain that it is effectively "chained" with the previous one
    def is_chain_valid(self):
        index = 1
        prev_block = self.chain[0]
        while len(self.chain) > index:
            curr_block = self.chain[index]
            if curr_block['prev_block_hash'] != self.hash(prev_block):
                return False
            elif self.check_proof(curr_block['nonce'], prev_block['nonce']) is False:
                return False
            prev_block = self.chain[index]
            index += 1
        
        return True

# blockchain = Blockchain()
# hashed = blockchain.hash({
#     "created": "2022-07-19 15:03:45.867697+00:00",
#     "index": 2,
#     "nonce": 62225,
#     "prev_block_hash": "fc4c28430a3bd5c98e8a5b9c0d90e1456eb708ba6e762fbe3808c798f1b9e172"
# })

# print('the hash', hashed)
