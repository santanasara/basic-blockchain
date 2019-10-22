import hashlib
import json
from time import time
import copy
import random
import requests

from bitcoin.wallet import CBitcoinSecret
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage

DIFFICULTY = 4

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.nodes = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        self.createBlock(previousHash='0'*64, nonce=0)
        self.mineProofOfWork(self.prevBlock) 

    def createBlock(self, nonce=0, previousHash=None):
        if (previousHash == None):
            previousBlock = self.chain[-1]
            previousBlockCopy = copy.copy(previousBlock)
            previousBlockCopy.pop("transactions", None)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': int(time()),
            'transactions': self.memPool,
            'merkleRoot': self.generateMerkleRoot(self.memPool),
            'nonce': nonce,
            'previousHash': previousHash or self.generateHash(previousBlockCopy),
        }

        self.memPool = []
        self.chain.append(block)
        return block

    def mineProofOfWork(self, prevBlock):
        nonce = 0
        while self.isValidProof(prevBlock, nonce) is False:
            nonce += 1

        return nonce

    def createTransaction(self, sender, recipient, amount, timestamp, privKey):
        tx = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': timestamp
        }

        tx['signature'] = Blockchain.sign(privKey, json.dumps(tx, sort_keys=True)).decode('utf-8')
        self.memPool.append(tx)

        return self.prevBlock['index'] + 1

    def isValidChain(self, chain):
    
        for block in chain:
            hashBlock = self.getBlockID(block)

            if (hashBlock[:DIFFICULTY] == "0" * DIFFICULTY):
                if (block["merkleRoot"] == self.generateMerkleRoot(block["transactions"])):
                    return True
            else:
                return False


    def resolveConflicts(self):
        
        for node in self.nodes:
            chain = requests.get(self.node + "/chain")
            nodeChain = chain.json()
            
            if self.isValidChain(nodeChain):
                if len(nodeChain) > len(self.chain):
                    self.chain = nodeChain

        return self.chain


    @staticmethod
    def generateMerkleRoot(transactions):
        transactionsData = json.dumps(transactions, sort_keys=True)

        return Blockchain.generateHash(transactionsData)
        merkleTree = transactions.copy()
        if(len(merkleTree) % 2 != 0):
            merkleTree.append(merkleTree[-1])

        while (len(merkleTree)> 1):
            j = 0
            for i in range(0, len(merkleTree) - 1):
                merkleTree[j] = Blockchain.generateHash(str(merkleTree[i]) + str(merkleTree[i+1]))
                i += 2
                j += 1
            lastDelete = i - j
            del merkleTree[-lastDelete:]

        return merkleTree


    @staticmethod
    def isValidProof(block, nonce):
        block['nonce'] = nonce
        guessHash = Blockchain.getBlockID(block)
        return guessHash[:DIFFICULTY] == '0' * DIFFICULTY 

    @staticmethod
    def generateHash(data):
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()

    @staticmethod
    def getBlockID(block):
        blockCopy = copy.copy(block)
        blockCopy.pop("transactions", None)
        return Blockchain.generateHash(blockCopy)

    def printChain(self):
         for i in self.chain:

            block = (json.dumps(i, sort_keys=True, indent=2))

            block = block.replace(",", "")
            block = block.replace("\"", "")
            block = block.replace("{", "")
            block = block.replace("}", "")
            print(block, "\n")
        

    @property
    def prevBlock(self):
        return self.chain[-1]

    @staticmethod
    def sign(privKey, message):
        secret = CBitcoinSecret(privKey)
        msg = BitcoinMessage(message)
        return SignMessage(secret, msg)
        
    @staticmethod
    def verifySignature(address, signature, message):
        msg = BitcoinMessage(message)
        return VerifyMessage(address, msg, signature)


