from typing import List
from message import Message

class Block:
    def __init__(self, messages: List[Message], N_lanes: int = 2):
        """
        Initializes the Block with a list of messages.

        Args:
            messages: List of messages.
            N_lanes: Number of lanes in the block.
        """
        self.messages = messages
        self.N_lanes = N_lanes
        self.gas_used = self.get_gas_used()

    def get_gas_used(self) -> List[int]:
        """
        Computes the total gas used in each lane of the block.

        Returns:
            A list of gas used values for each lane.
        """
        total_gas_used = [0] * self.N_lanes
        for message in self.messages:
            for i in range(self.N_lanes):
                total_gas_used[i] += message.gas_used[i]
        return total_gas_used

if __name__ == '__main__':
    from opcodes import Opcode

    opcode1 = Opcode(1, "ADD")
    opcode2 = Opcode(2, "SUB")
    opcode3 = Opcode(3, "MUL")
    opcode4 = Opcode(4, "foreign_opcode", 100)

    opcode_list = [opcode1, opcode2, opcode3, opcode4]
    MESSAGE_NAME = 'msg1'
    message1 = Message(MESSAGE_NAME, [100.0, 100], [50.0, 50], opcode_list)
    print(f'Message {MESSAGE_NAME} has a gas usage of {message1.gas_used} and a gas limit of {message1.gas_limit}')

    block = Block([message1, message1, message1])
    total_gas_used = block.get_gas_used()

    print(f"Total gas used in the block: {total_gas_used}")
