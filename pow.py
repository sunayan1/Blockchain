import hashlib
from ecdsa import SigningKey, SECP256k1

admin_private= SigningKey.generate(curve=SECP256k1)
admin_public= admin_private.get_verifying_key()

class Block:
    def __init__(self, data, prev_hash):
        self.data= data
        self.prev_hash= prev_hash
        self.nonce=0
        target= "0000"
        while True:
            self.hash= self.calc_hash()
            if self.hash.startswith(target):
                break
            self.nonce += 1
        self.signature= self.sign_block()

    def calc_hash(self):
        sha= hashlib.sha256()
        sha.update((self.data + self.prev_hash + str(self.nonce)).encode('utf-8'))  
        return sha.hexdigest()
    
    def sign_block(self):
        signature= admin_private.sign(self.hash.encode('utf-8'))
        return signature
    

class Blockchain:
    def __init__(self):
        self.chain= [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block('Genesis Block', "0")
    
    def add_block(self, data):
        prev_block= self.chain[-1]
        current_block= Block(data, prev_block.hash)

        if self.verify_block(current_block, prev_block):
            self.chain.append(current_block)
            print("block added")
        else:
            print("Invalid block dsfsdf")

    def verify_block(self, block, prev_block):
        if(block.prev_hash != prev_block.hash):
            return False
        
        sha= hashlib.sha256()
        sha.update((block.data + block.prev_hash + str(block.nonce)).encode('utf-8'))
        recalculated_hash= sha.hexdigest()
        if recalculated_hash != block.hash:
            return False
        
        if not block.hash.startswith("0000"):  # same difficulty as mining
            return False

        
        try:
            admin_public.verify(block.signature, block.hash.encode('utf-8'))
        except:
            return False
        
        return True
    
    def validate_chain(self):

        for i in range (1, len(self.chain)):
            current_block= self.chain[i]
            prev_block= self.chain[i-1]

            if current_block.prev_hash != prev_block.hash:
                print(f"Prev hash doesnt match in Block{i}")
                return False
            
            recalculated_hash= hashlib.sha256((current_block.data + current_block.prev_hash).encode('utf-8'))
            if recalculated_hash != current_block.hash:
                print(f"Stored Hash: {current_block.hash}")
                print(f"Actual Hash: {recalculated_hash}")
                return False
            
            try:
              admin_public.verify(current_block.signature, current_block.hash.encode('utf-8'))
            except:
              print(f"INVALID: Block {i} Signature is invalid!")
              return False

        print("Blockchain is valid.")
        return True
    

blockchain= Blockchain()
            
blockchain.add_block('First Block')

print('Blockchain: ')
for block in blockchain.chain:
  print('Data: ', block.data)
  print('Previous hash: ', block.prev_hash)
  print('Hash: ', block.hash)
  print('Signature: ', block.signature.hex())




        
