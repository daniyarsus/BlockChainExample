import hashlib
import time


class Block:
    def __init__(
            self,
            index,
            previous_hash,
            timestamp,
            data,
            hash
    ) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    @staticmethod
    def calculate_hash(index, previous_hash, timestamp, data) -> hash:
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    @staticmethod
    def create_genesis_block() -> 'Block':
        return Block(
            0, "0", int(time.time()), "Genesis Block",
            Block.calculate_hash(0, "0", int(time.time()), "Genesis Block")
        )

    @staticmethod
    def create_new_block(previous_block, data) -> 'Block':
        index = previous_block.index + 1
        timestamp = int(time.time())
        previous_hash = previous_block.hash
        hash = Block.calculate_hash(index, previous_hash, timestamp, data)
        return Block(index, previous_hash, timestamp, data, hash)


class Blockchain:
    def __init__(self) -> None:
        self.chain = [Block.create_genesis_block()]

    def get_latest_block(self) -> hash:
        return self.chain[-1]

    def add_block(self, data) -> None:
        previous_block = self.get_latest_block()
        new_block = Block.create_new_block(previous_block, data)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != Block.calculate_hash(
                    current_block.index,
                    current_block.previous_hash,
                    current_block.timestamp,
                    current_block.data
            ):
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


if __name__ == "__main__":
    blockchain_instance = Blockchain()

    print("Creating genesis-block...")
    print("Genesis-block: ", vars(blockchain_instance.chain[0]))

    print("\nAdding blocks to the chain...")
    blockchain_instance.add_block("First block after genesis")
    blockchain_instance.add_block("Second block after genesis")
    blockchain_instance.add_block("Third block after genesis")

    for block in blockchain_instance.chain:
        print(vars(block))

    print("\nChain integrity check: ", blockchain_instance.is_chain_valid())
