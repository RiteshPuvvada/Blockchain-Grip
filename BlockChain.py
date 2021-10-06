import datetime
import hashlib
import json
from flask import Flask, jsonify, escape, request
from werkzeug.wrappers import response


# Building a blockchain

class BlockChain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self,proof,previous_hash):
        Block = {
            "index": len(self.chain) + 1,
            "timestamp" : str(datetime.datetime.now()),
            "proof" : proof,
            "previous_hash" : previous_hash
        } 
        self.chain.append(Block)
        return Block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000' : 
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

# Mining Blockchain

app = Flask(__name__) # Initializing a Web app

blockchain = BlockChain() # Creating a Blockchain

@app.route('/mine_block', methods = ['GET']) # Mining a new block

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Successfully mined a block :)',
                "index": block['index'],
                "timestamp" : block['timestamp'],
                "proof" : block['proof'],
                "previous_hash" : block['previous_hash']
                }
    return  jsonify(response), 200


@app.route('/get_chain', methods = ['GET']) # Getting the Blockchain

def get_chain():
    response = {'chian' : blockchain.chain,
                'length' : len(blockchain.chain)
                }
    return  jsonify(response), 200

@app.route('/is_valid', methods = ['GET']) # Checking if the Blockchain is valid

def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : 'Everything is fine. Blockchain is valid ^_^'}
    else:
        response = {'message' : 'We have a problem. Blockchain is invalid :('}
    return  jsonify(response), 200

app.run(host = '127.0.0.1', port=5000)