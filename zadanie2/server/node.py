import struct
from collections import deque


TEXTFIELD_SIZE = 50*1000


class TreeNode:
    def __init__(self, data_16: int, data_32: int, text: str):
        self.data_16 = data_16
        self.data_32 = data_32
        self.text = text
        self.left = None
        self.right = None


def deserialize_tree(data: bytes, offset: int = 0):
    if offset >= len(data):
        return None, offset
    
    data_16_size = 2
    data_32_size = 4
    text_size = TEXTFIELD_SIZE

    data_16 = struct.unpack_from('!H', data, offset)[0]
    offset += data_16_size

    data_32 = struct.unpack_from('!I', data, offset)[0]
    offset += data_32_size

    text = data[offset:offset + text_size].decode('utf-8').rstrip('\x00')
    offset += text_size

    root = TreeNode(data_16=data_16, data_32=data_32, text=text)
    queue = deque([root])

    while queue and offset < len(data):
        current_node = queue.popleft()

        if offset < len(data):
            data_16 = struct.unpack_from('!H', data, offset)[0]
            offset += data_16_size

            data_32 = struct.unpack_from('!I', data, offset)[0]
            offset += data_32_size

            text = data[offset:offset + text_size].decode('utf-8').rstrip('\x00')
            offset += text_size

            left_node = TreeNode(data_16=data_16, data_32=data_32, text=text)
            current_node.left = left_node
            queue.append(left_node)

        if offset < len(data):
            data_16 = struct.unpack_from('!H', data, offset)[0]
            offset += data_16_size

            data_32 = struct.unpack_from('!I', data, offset)[0]
            offset += data_32_size

            text = data[offset:offset + text_size].decode('utf-8').rstrip('\x00')
            offset += text_size

            right_node = TreeNode(data_16=data_16, data_32=data_32, text=text)
            current_node.right = right_node
            queue.append(right_node)

    return root, offset
