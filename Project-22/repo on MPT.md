# research report on MPT
## MPT简述
Merkle Patricia Tree(MPT)是一种基于Patricia Tree和Merkle树（一种哈希树）的数据结构。它是以太坊(Ethereum)区块链中使用的一种重要的数据结构，用于存储账户、合约和交易等数据。
## Patricia Tree
Patricia Tree又称compact prefix tree（压缩前缀树）；前缀树也叫做字典树或Trie，前缀树中的节点通过它们在树中的位置（或者说从根节点到其他节点的路径）来定义。下图所示存储了"A"，"to"，"tea"，"ted"，"ten"，"i"，"in"，"inn"的key。
![image](https://github.com/Ashl703/group-xx/assets/138503504/2b6ecbb2-caa7-4336-9851-7c339a325740)
而Patricia Tree是一种更节省空间的前缀树。对于Patricia树的每个节点，如果该节点是唯一的儿子的话，就和父节点合并。因此一棵Patricia树的任何内部节点存在2个或以上的孩子节点。下图将i,in,inn合并为inn节点，就是一个压缩前缀树。值得注意的是，有压缩就有碰撞，可以通过压缩前缀树避免重复存储，同时也要注意对于压缩前缀带来的混淆问题（相关HP算法见下文）。
![image](https://github.com/Ashl703/group-xx/assets/138503504/4dcad541-df12-4ce2-aa47-c9d77ca93827)
## Merkle Tree
Merkle Tree是由计算机科学家 Ralph Merkle 在很多年前提出的，并以他本人的名字来命名；Merkle Tree被用来归纳一个区块中的所有交易，同时生成整个交易集合的数字指纹。此外，由于Merkle Tree的存在，使得在Bitcoin这种公链的场景下，扩展一种“轻节点”实现简单支付验证变成可能。下图展示了Merkle Tree的结构特点。
![image](https://github.com/Ashl703/group-xx/assets/138503504/31a8b46a-796b-4b9a-b15d-c902ef15507a)
## MPT (in Ethereum)
MPT中的节点包括空节点(NULL)、叶子节点(leaf)、扩展节点(extension)和分支节点(branch)。HP(Hex-Prefix)编码指明出现连续的半字节编码是奇数或者偶数位。
### 空节点(NULL)
用一个空的字符串表示。
### 叶子节点(leaf)
Key-end是剩下的Key的半字节编码，value是值。
### 扩展节点(extension)
Shared nibble(s)是剩下的重复的Key的半字节编码，next node字段指向另一个节点（一般为分支节点）。
### 分支节点(branch)
17元组[v0...v15,vt]。其前16个项对应于这些点在其遍历中的键的十六个可能的半字节值中的每一个。第17个字段是存储在那些在当前节点结束了的节点所存储的值。
![image](https://github.com/Ashl703/group-xx/assets/138503504/04e20deb-9f9e-4bae-9046-98ebbe30af0a)
### 构造过程
1.若当前只有一个kv(key,value)对，则直接将其构造成一个叶子节点。
2.若当前需要编码的kv集合有公共前缀，则提取公共前缀，将其构造成一个扩展节点，并将其第二个字段指向下一个节点（一般为分支节点）。
3.若不是上述两种情况，则构造分支节点按照当前key所在索引的16进制对kv集合进行划分，[0..f]分别指向[0..f]对应半字节所指向的下一个节点。如果有kv对在此节点终结，则将其存储在value中。
在上图的示例中，有公共前缀a7，提取并作为扩展节点，指向分支节点。在分支节点中a711355和a7f9365没有公共前缀，构造成叶子节点，并在叶子节点中存储后面的key（merkle tree 的性质将后面的所有key合并）。a77d337和a77d397有相同前缀，构造扩展节点（merkle tree性质将d和3合并），后接分支节点。然后作为叶节点存储。由于扩展节点并不能代表唯一的key值，所以没有存储value。而叶节点和分支节点会存储value值。上图中的两个分支节点分别可以存储key为a7和a77d3的value值。
## 总结
总的来说，MPT具有响应式能力、压缩高效、容易验证等优点，适用于对效率和安全性要求很高的场景，如区块链存储。以太坊的状态树、存储树以及账户、合约地址等的内部实现就是通过MPT的原理实现的。通过MPT能很高效的管理庞大的账户和合约数据。
MPT树的作用 1.存储任意长度的key-value键值对数据； 2.提供了一种快速计算所维护数据集哈希标识的机制； 3.提供了快速状态回滚的机制； 4.提供了一种称为默克尔证明的证明方法，进行轻节点的扩展，实现简单支付验证；
![image](https://github.com/Ashl703/group-xx/assets/138503504/b167d5d2-1ee5-4ef4-8b50-4139cb27b522)
MPT树中的节点包括空节点、叶子节点、扩展节点和分支节点:

空节点，简单的表示空，在代码中是一个空串。

叶子节点（leaf），表示为[key,value]的一个键值对，其中key是key的一种特殊十六进制编码，value是value的RLP编码。

扩展节点（extension），也是[key，value]的一个键值对，但是这里的value是其他节点的hash值，这个hash可以被用来查询数据库中的节点。也就是说通过hash链接到其他节点。

分支节点（branch），因为MPT树中的key被编码成一种特殊的16进制的表示，再加上最后的value，所以分支节点是一个长度为17的list，前16个元素对应着key中的16个可能的十六进制字符，如果有一个[key,value]对在这个分支节点终止，最后一个元素代表一个值，即分支节点既可以搜索路径的终止也可以是路径的中间节点。

MPT树中另外一个重要的概念是一个特殊的十六进制前缀(hex-prefix, HP)编码，用来对key进行编码。因为字母表是16进制的，所以每个节点可能有16个孩子。因为有两种[key,value]节点(叶节点和扩展节点)，引进一种特殊的终止符标识来标识key所对应的是值是真实的值，还是其他节点的hash。如果终止符标记被打开，那么key对应的是叶节点，对应的值是真实的value。如果终止符标记被关闭，那么值就是用于在数据块中查询对应的节点的hash。无论key奇数长度还是偶数长度，HP都可以对其进行编码。最后我们注意到一个单独的hex字符或者4bit二进制数字，即一个nibble。

HP编码很简单。一个nibble被加到key前（下图中的prefix），对终止符的状态和奇偶性进行编码。最低位表示奇偶性，第二低位编码终止符状态。如果key是偶数长度，那么加上另外一个nibble，值为0来保持整体的偶特性。

HP编码 HP-编码：特殊的十六进制前缀编码
MPT树的操作
c) 否则，创建一个分支节点。如果curr_key只剩下了一个字符，并且node是扩展节点，那么这个分支节点的remain_curr_key[0]的分支是node[1]，即存储node的value。否则，这个分支节点的remain_curr_key[0]的分支指向一个新的节点，这个新的节点的key是remain_curr_key[1:]的HP编码，value是node[1]。如果remain_key为空，那么新的分支节点的value是要参数中的value，否则，新的分支节点的remain_key[0]的分支指向一个新的节点，这个新的节点是[pack_nibbles(with_terminator(remain_key[1:])),value]

d) 如果key和curr_key有公共部分，为公共部分创建一个扩展节点，此扩展节点的value链接到上面步骤创建的新节点，返回这个扩展节点；否则直接返回上面步骤创建的新节点
下面从MPT树的更新，删除和查找过程来说明MPT树的操作。

1 更新

函数_update_and_delete_storage(self, node, key, value)

i. 如果node是空节点，直接返回[pack_nibbles(with_terminator(key)), value]，即对key加上终止符，然后进行HP编码。
ii. 如果node是分支节点，如果key为空，则说明更新的是分支节点的value，直接将node[-1]设置成value就行了。如果key不为空，则递归更新以key[0]位置为根的子树，即沿着key往下找，即调用_update_and_delete_storage(self._decode_to_node(node[key[0]]),key[1:], value)。

iii. 如果node是kv节点（叶子节点或者扩展节点），调用_update_kv_node(self, node, key, value)，见步骤iv

iv. curr_key是node的key，找到curr_key和key的最长公共前缀，长度为prefix_length。Key剩余的部分为remain_key，curr_key剩余的部分为remain_curr_key。

a) 如果remain_key==[]== remain_curr_key，即key和curr_key相等，那么如果node是叶子节点，直接返回[node[0], value]。如果node是扩展节点，那么递归更新node所链接的子节点，即调用_update_and_delete_storage(self._decode_to_node(node[1]),remain_key, value)
b) 如果remain_curr_key == []，即curr_key是key的一部分。如果node是扩展节点，递归更新node所链接的子节点，即调用_update_and_delete_storage(self._decode_to_node(node[1]),remain_key, value)；如果node是叶子节点，那么创建一个分支节点，分支节点的value是当前node的value，分支节点的remain_key[0]位置指向一个叶子节点，这个叶子节点是[pack_nibbles(with_terminator(remain_key[1:])),value]
v. 删除老的node，返回新的node

2 删除

删除的过程和更新的过程类似，而且很简单，函数名：_delete_and_delete_storage(self, key)

i. 如果node为空节点，直接返回空节点

ii. 如果node为分支节点。如果key为空，表示删除分支节点的值，直接另node[-1]=‘’, 返回node的正规化的结果。如果key不为空，递归查找node的子节点，然后删除对应的value，即调用self._delete_and_delete_storage(self._decode_to_node(node[key[0]]),key[1:])。返回新节点

iii. 如果node为kv节点，curr_key是当前node的key。

a) 如果key不是以curr_key开头，说明key不在node为根的子树内，直接返回node。

b) 否则，如果node是叶节点，返回BLANK_NODE if key == curr_key else node。

c)如果node是扩展节点，递归删除node的子节点，即调用_delete_and_delete_storage(self._decode_to_node(node[1]),key[len(curr_key):])。如果新的子节点和node[-1]相等直接返回node。否则，如果新的子节点是kv节点，将curr_key与新子节点的可以串联当做key，新子节点的value当做vlaue，返回。如果新子节点是branch节点，node的value指向这个新子节点，返回。

3 查找

查找操作更简单，是一个递归查找的过程函数名为：_get(self, node, key)

i. 如果node是空节点，返回空节点

ii. 如果node是分支节点，如果key为空，返回分支节点的value；否则递归查找node的子节点，即调用_get(self._decode_to_node(node[key[0]]), key[1:])

iii. 如果node是叶子节点，返回node[1] if key == curr_key else ‘’

iv. 如果node是扩展节点，如果key以curr_key开头，递归查找node的子节点，即调用_get(self._decode_to_node(node[1]),key[len(curr_key):])；否则，说明key不在以node为根的子树里，返回空
