import hashlib
import json
import time
import copy
class Blockchain(object):
    difficulty = 4
    def __init__(self):
        self.chain = []
        self.memPool = []
        self.createGenesisBlock()
        
        

    def createGenesisBlock(self):
        self.createBlock()
        genesisBlock = self.chain[-1]
        genesisBlock['nonce'] = self.mineProofOfWork(self.prevBlock)
    
   
    def createBlock(self):
       
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
       
    @property
    def prevBlock(self):
        return self.chain[-1]

    @staticmethod
    def generateHash(data):
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()
    

    @staticmethod
    def getBlockId(block):
        blockHeader = block.copy()
        blockHeader.pop('transactions')
        return Blockchain.generateHash(blockHeader)
        

    
    @staticmethod
    def isValidProof(prevBlock, nonce):
        block = prevBlock.copy()
        block['nonce'] = nonce
        
        checkBlockId = Blockchain.getBlockId(block)

        if(checkBlockId[:Blockchain.difficulty]=='0'*Blockchain.difficulty):
            return True
        
        return False
        
    def mineProofOfWork(self, prevBlock):
        validNonce = 0
        BlockCopy = prevBlock.copy()
        while(True):
            validNonce+=1
            BlockCopy['nonce'] = validNonce
            proofOfWork = self.getBlockId(BlockCopy)
            
            if(self.isValidProof(BlockCopy, validNonce)):
                self.prevBlock['nonce'] = validNonce
                break

        return validNonce

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

for x in range(0, 3): 
    blockchain.createBlock()
    blockchain.mineProofOfWork(blockchain.prevBlock)

blockchain.printChain()

for x in blockchain.chain :
    print('[Bloco #{} : {}] Nonce: {} | É válido? {}'.format(x['index'], blockchain.getBlockId(x), x['nonce'], blockchain.isValidProof(x,x['nonce'])))
    
    