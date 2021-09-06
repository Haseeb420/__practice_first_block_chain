from flask import Flask,jsonify
import datetime
import json
import hashlib
app = Flask(__name__)

class BlockChain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1,previous_hash='0')

    def create_block(self,proof,previous_hash):
        block={
            'index':len(self.chain)+1,
            'time_stamp':str(datetime.datetime.now()),
            'proof':proof,
            'previous_hash':previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[len(self.chain)-1]

    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=="0000":
                check_proof=True
            else:
                new_proof+=1
        return new_proof

    def hash(self,block):
        encode_block=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()

    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index<len(chain):
            block=chain[block_index]
            if block['previous_hash']!= self.hash(previous_block):
                return False
            previous_proof=previous_block['proof']
            proof=block['proof']
            hash_operation=hashlib.sha256(str((proof**2)-(previous_proof**2)).encode).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            previous_block=block
            block_index+=1
        return True
myBlockChain=BlockChain()

@app.route("/")
def home():
    return "Hello World"


@app.route("/mine_block",methods=["GET","POST"])
def mine_block():
    previous_block=myBlockChain.get_previous_block()
    previous_proof=previous_block['proof']
    print(previous_proof)
    proof=myBlockChain.proof_of_work(previous_proof)
    previous_hash=myBlockChain.hash(previous_block)
    block=myBlockChain.create_block(proof,previous_hash)
    response={"message":"congratulation on new block!",
        'index':block['index'],
        'time_stamp':block['time_stamp'],
         'proof':block['proof'],
         'previous_hash':block['previous_hash']
    }
    return jsonify(response),200 

@app.route("/get_chain",methods=["GET"])
def get_chain():
    response={"chain":myBlockChain.chain,
        "length":len(myBlockChain.chain)
    }
    return jsonify(response),200 

@app.route("/is_valid",methods=["GET"])
def is_valid():
    is_valid=myBlockChain.is_chain_valid(myBlockChain.chain)
    if is_valid:
        response={"message":"Everything is fine"}
    else:
        response={"message":"some data is change in chian"}
        
    return jsonify(response),200 


    
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)
