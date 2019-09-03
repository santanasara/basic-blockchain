import hashlib
import json
import time
import copy
class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.createGenesisBlock()
        self.difficulty ='0000'
        

    def createGenesisBlock(self):
        self.createBlock(0, 000000)
    
   
    def createBlock(self, nonce, previousHash):
       
        index = len(self.chain)
        timestamp = int(time.time())

        # Creates genesis block
        if(index==0):
            block = {
            'index': index,
            'timestamp': timestamp,
            'nonce': 0,
            'merkleRoot': 0,
            'previousHash': 0,
            'transactions': self.memPool
            }
        # Creates other blocks
        else:
            block = {
                'index': index,
                'timestamp': timestamp,
                'nonce': 0,
                'merkleRoot': 0,
                'previousHash': self.getBlockId(self.prevBlock),
                'transactions': self.memPool
            }
            
        
        self.chain.append(block)
       
    
    @staticmethod
    def generateHash(data):

        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()
    
    
    @property
    def prevBlock(self):

        prevBlockHeader = self.chain[-1].copy()
        prevBlockHeader.pop('transactions')
        return prevBlockHeader

    def getBlockId(self, block):

        return self.generateHash(block)
        

    def mineProofOfWork(self):

        block = self.prevBlock
        validNonce = 0

        while(True):
            validNonce+=1
            block['nonce'] = validNonce
            proofOfWork = self.getBlockId(block)
            
            if(proofOfWork[:4] == self.difficulty):
                break

        return validNonce
    
    def isValidProof(self,  nonce):
        
        block = self.prevBlock
        block['nonce'] = nonce
        checkBlockId = self.getBlockId(block)

        if(checkBlockId[:4]==self.difficulty):
            return True
        
        return False
        

    def printChain(self):
        count = 0
        for i in self.chain:
            
            block = (json.dumps(i, sort_keys=True, indent=2))
            
            block = block.replace(",", "")
            block = block.replace("\"", "")
            block = block.replace("{", "")
            block = block.replace("}", "")

            
            print(block, "\n")
            count = count+1

    
# Teste
blockchain = Blockchain()

for x in range(0, 10): blockchain.createBlock(0, 0)
#blockchain.printChain()

testNonce = blockchain.mineProofOfWork()
print("Valid nonce: ", testNonce)
print("Is valid? ", blockchain.isValidProof(testNonce))
