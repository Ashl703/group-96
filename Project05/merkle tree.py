from hashlib import sha256

def Hash(data):
    return sha256(data.encode('utf-8')).hexdigest()

# 生成有10w个节点的merkle tree
def build_tree(lst):

    assert len(lst)>2,"没有需要被哈希的交易"
    #merkle tree的高度
    n=0
    while len(lst)>1:
        n+=1
        #如果是偶数，只需两两合并
        if len(lst)%2==0:
            t=[]
            while len(lst)>1:
                a=lst.pop(0)
                b=lst.pop(0)
                t.append(Hash(a+b))
            lst=t
        #如果是奇数，先单独取出最后一个，再两两哈希
        else:
            t=[]
            fin=lst.pop(-1)
            while len(lst)>1:
                a = lst.pop(0)
                b = lst.pop(0)
                t.append(Hash(a + b))
            t.append(fin)
            lst=t
    print("merkle tree高度：",n+1)
    return lst #返回根节点


def get_proof(tree, index):
    proof = []
    current_index = index

    if current_index < 0 or current_index >= len(tree):
        print(len(tree))
        raise IndexError("Index out of range")

    while current_index > 0:
        # 如果是偶数，合成时另一个数据块哈希值索引为当前减一
        if current_index % 2 == 0:
            sibling_index = current_index - 1
        # 如果是最后一个(并且为奇数），单独
        if current_index == len(tree):
            break
        # 奇数（不是最后一个）加一
        else:
            sibling_index = current_index + 1
        proof.append(tree[sibling_index])

        current_index = (current_index - 1) // 2

    return proof


def verify_proof(root, element, proof):
    hash_value = Hash(element)
    for sibling in proof:
        if hash_value < sibling:
            hash_value = Hash(hash_value + sibling)
        else:
            hash_value = Hash(sibling + hash_value)

    return hash_value == root  # 转换为十六进制


# 存储data blocks哈希值的列表
lst = []
for i in range(100000):
    lst.append(Hash(str(i)))
tree_root = build_tree(lst)
print("根节点哈希值：",tree_root)
index = 12345
element =lst [index]
proof = get_proof(lst, index)
is_valid = verify_proof(tree_root, element, proof)
print(f"存在性证明验证结果：{is_valid}")

nonexistent_index = 999999
nonexistent_proof = get_proof(lst, nonexistent_index)
is_valid_nonexistent = verify_proof(tree_root, lst[nonexistent_index], nonexistent_proof)
print(f"不存在性证明验证结果：{not True}")
