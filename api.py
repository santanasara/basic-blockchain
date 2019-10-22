from blockchain import Blockchain
from time import time
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
blockchain = Blockchain()

@app.route("/transactions/create", methods = ["POST"])
def createTranscation():
	data = request.get_json(force=True)
	sender = data["sender"]
	recipient =  data["recipient"]
	amount = data["amount"]
	privKey = data["privKey"]
	blockchain.createTransaction(sender, recipient , amount, int(time()), privKey)
	
	return jsonify(blockchain.memPool[-1])



@app.route("/transactions/mempool", methods = ["GET"])
def getMempool():
	return jsonify(blockchain.memPool)

@app.route("/mine", methods = ["GET"])
def mine():
	block = blockchain.createBlock()
	blockchain.mineProofOfWork(blockchain.prevBlock)
	return jsonify(block)

@app.route("/chain", methods = ["GET"])
def chain():
	return jsonify(blockchain.chain)

@app.route("/nodes/register", methods = ["POST"])
def register():
	nodes = request.get_json(force=True)	
	node = nodes["node"]
	
	blockchain.nodes.append(node)	
	return jsonify([node for node in blockchain.nodes])


@app.route("/nodes/resolve", methods = ["GET"])
def resolve():
	return jsonify(blockchain.resolveConflicts())

if __name__ == '__main__':
    app.run(port=8080)