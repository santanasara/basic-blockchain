import hashlib
import json
import time
import copy
class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.createGenesisBlock()
        #difficulty ='0000'

    def createGenesisBlock(self):
        self.createBlock(0, 000000)
    
   

    def createBlock(self, nonce, previousHash):
       
        index = len(self.chain)
        timestamp = int(time.time())

        #Creates genesis block
        if(index==0):
            block = {
            'index': index,
            'timestamp': timestamp,
            'nonce': 0,
            'merkleRoot': 0,
            'previousHash': 0,
            'transactions': self.memPool
            }
        #Creates other blocks
        else:
            block = {
                'index': index,
                'timestamp': timestamp,
                'nonce': 0,
                'merkleRoot': 0,
                'previousHash': self.generateHeaderHash(),
                'transactions': self.memPool
            }
            
        
        self.chain.append(block)
    
    # @property
    # def prevBlock(self):
    #     prevBlock = (self.chain[-1].copy())['transactions'].pop()
    #     return prevBlock
    
    @staticmethod
    def generateHash(data):
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()
    
    def generateHeaderHash(self):
        #Copies the last block in the chain and hashes the header
        header = (self.chain[-1]).copy()
        header.pop('transactions')
        return self.generateHash(header)
    
    def getBlockId(self, block):
        return self.generateHash(block)
        

    def mineProofOfWork(self):
        difficulty = '0000'
        block = self.chain[-1].copy()
        block.pop('transactions')
        validNonce = 0
        while(True):
            validNonce+=1
            block['nonce'] = validNonce
            proofOfWork = self.getBlockId(block)
            
            if(proofOfWork[:4] == difficulty):
                break

        return validNonce
    
    def isValidProof(self,  nonce):
        difficulty = '0000'
        block = self.chain[-1].copy()
        block.pop('transactions')
        block['nonce']=nonce
        checkBlockId = self.getBlockId(block)
        if(checkBlockId[:4]==difficulty):
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

            
            # if(count>0):
            #     header = copy.deepcopy(self.chain)
            #     header[count-1].pop('transactions')
        
            #     print("Hash da header do bloco de indice ",count-1,": ", self.generateHash(header[count-1]))
            
            print(block, "\n")
            count = count+1

    
# Teste
blockchain = Blockchain()


for x in range(0, 10): blockchain.createBlock(0, 0)
#blockchain.printChain()
print("valid nonce: ", blockchain.mineProofOfWork())
print("is valid? ", blockchain.isValidProof(blockchain.mineProofOfWork()))

