import hashlib
import json
import time
import copy
class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.memPool = []
        self.createGenesisBlock()

    def createGenesisBlock(self):
        self.createBlock(0, 000000)
    
   

    def createBlock(self, nonce, previousHash):
        # Implemente aqui o método para retornar um bloco (formato de dicionário)
        # Lembre que o hash do bloco anterior é o hash na verdade do CABEÇALHO do bloco anterior.
        
        index = len(self.chain)
        timestamp = int(time.time())

        if(index==0):
            block = {
            'index': index,
            'timestamp': timestamp,
            'nonce': 0,
            'merkleRoot': 0,
            'previousHash': 0,
            'transactions': self.memPool
            }
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
        #print("aqui",self.chain)

    @staticmethod
    def generateHash(data):
        blkSerial = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(blkSerial).hexdigest()
    
    def generateHeaderHash(self):
        #Cria copia do chain
        header = (self.chain[-1]).copy()
        #Header do bloco anterior
        header.pop('transactions')
        return self.generateHash(header)

    def printChain(self):
        # Implemente aqui um método para imprimir de maneira verbosa e intuitiva o blockchain atual.
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
blockchain.printChain()

