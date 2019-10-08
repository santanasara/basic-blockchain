import hashlib
import json
from time import time
import copy
import random
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
        # Creates genesis block
        if(index==0):
            block = {
            'index': index,
            'timestamp': int(time()),
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
                'merkleRoot': self.generateMerkleRoot(self.memPool),
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
            block = block.replace("[", "")
            block = block.replace("]", "")
            
            print(block, "\n")
            count = count+1


    @staticmethod
    def sign(privKey, message):
        secret = CBitcoinSecret(privKey)
        message = BitcoinMessage(message)
        return SignMessage(secret, message).decode()
        
        
    @staticmethod
    def verifySignature(address, signature, message):
        
        msg = BitcoinMessage(message)
        return VerifyMessage(address, msg, signature)


    def createTransaction(self, sender, recipient, amount, timestamp, privKey):
        
        message = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "timestamp": timestamp,
        }

        blkSerial = json.dumps(message, sort_keys=True)
        signature = Blockchain.sign(privKey, blkSerial)
        
        transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
        "timestamp": timestamp,
        "signature": signature
        }
        
        
        self.memPool.append(transaction)
        #print("\n", self.memPool)

    @staticmethod
    def generateMerkleRoot(transactions):
        transactionsData = json.dumps(transactions, sort_keys=True)
        
        return Blockchain.generateHash(transactionsData)

# Teste
blockchain = Blockchain()

sender = '19sXoSbfcQD9K66f5hwP5vLwsaRyKLPgXF'
recipient = '1MxTkeEP2PmHSMze5tUZ1hAV3YTKu2Gh1N'

# Cria 5 blocos, incluindo o Genesis, contendo de 1-4 transações cada, com valores aleatórios, entre os endereços indicados em sender e recipient.
for x in range(0, 4): 
    for y in range(0, random.randint(1,4)) : 
        timestamp = int(time())
        amount = random.uniform(0.00000001, 100)
        blockchain.createTransaction(sender, recipient, amount, timestamp, 'L1US57sChKZeyXrev9q7tFm2dgA2ktJe2NP3xzXRv6wizom5MN1U')
    blockchain.createBlock()
    blockchain.mineProofOfWork(blockchain.prevBlock)

blockchain.printChain()