import hashlib
import json
import time
import copy
from bitcoin.wallet import CBitcoinSecret
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage

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
        blockCopy = prevBlock.copy()
        blockCopy['nonce'] = nonce
        
        checkBlockId = Blockchain.getBlockId(blockCopy)

        if(checkBlockId[:Blockchain.difficulty]=='0'*Blockchain.difficulty):
            return True
       
        del blockCopy
        return False
        
    def mineProofOfWork(self, prevBlock):
        validNonce = 0
        blockCopy = prevBlock.copy()
        while(True):
            validNonce+=1
            blockCopy['nonce'] = validNonce
            proofOfWork = self.getBlockId(blockCopy)
            
            if(self.isValidProof(blockCopy, validNonce)):
                self.prevBlock['nonce'] = validNonce
                break
        
        del blockCopy
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


    @staticmethod
    def sign(privKey, message):
        secret = CBitcoinSecret(privKey)
        message = BitcoinMessage(message)
        return SignMessage(secret, message)
        
        
    @staticmethod
    def verifySignature(address, signature, message):
        
        msg = BitcoinMessage(message)
        return VerifyMessage(address, msg, signature)

# Teste
address = '15phrcdLM2R3kE5QS91o4PRtXmxMhbiYP5'
privKey = 'KwUVGQq1iWyLdKdFZh2ioCPbjAirbtrFfwqcpjSHAGQGkN3VJHc9'

message = 'Bora assinar essa mensagem?'

signature = Blockchain.sign(privKey, message)
print('Assinatura gerada: {}'.format(signature))

print('Assinatura válida para mensagem e endereço indicado? {}'.format(Blockchain.verifySignature(address, signature, message)))