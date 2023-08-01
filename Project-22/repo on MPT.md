# research report on MPT
## MPT简述
Merkle Patricia Tree(MPT)是一种基于Patricia Tree和Merkle树（一种哈希树）的数据结构。它是以太坊(Ethereum)区块链中使用的一种重要的数据结构，用于存储账户、合约和交易等数据。<br>
## Patricia Tree
Patricia Tree又称compact prefix tree（压缩前缀树）；前缀树也叫做字典树或Trie，前缀树中的节点通过它们在树中的位置（或者说从根节点到其他节点的路径）来定义。下图所示存储了"A"，"to"，"tea"，"ted"，"ten"，"i"，"in"，"inn"的key。<br>
![image](https://github.com/Ashl703/group-xx/assets/138503504/2b6ecbb2-caa7-4336-9851-7c339a325740)

而Patricia Tree是一种更节省空间的前缀树。对于Patricia树的每个节点，如果该节点是唯一的儿子的话，就和父节点合并。因此一棵Patricia树的任何内部节点存在2个或以上的孩子节点。下图将i,in,inn合并为inn节点，就是一个压缩前缀树。值得注意的是，有压缩就有碰撞，可以通过压缩前缀树避免重复存储，同时也要注意对于压缩前缀带来的混淆问题（相关HP算法见下文）。

![image](https://github.com/Ashl703/group-xx/assets/138503504/4dcad541-df12-4ce2-aa47-c9d77ca93827)

## Merkle Tree
Merkle Tree是由计算机科学家 Ralph Merkle 在很多年前提出的，并以他本人的名字来命名；Merkle Tree被用来归纳一个区块中的所有交易，同时生成整个交易集合的数字指纹。此外，由于Merkle Tree的存在，使得在Bitcoin这种公链的场景下，扩展一种“轻节点”实现简单支付验证变成可能。下图展示了Merkle Tree的结构特点。

![image](https://github.com/Ashl703/group-xx/assets/138503504/31a8b46a-796b-4b9a-b15d-c902ef15507a)

## MPT (in Ethereum)
MPT中的节点包括空节点(NULL)、叶子节点(leaf)、扩展节点(extension)和分支节点(branch)。HP(Hex-Prefix)编码指明出现连续的半字节编码是奇数或者偶数位。
* 空节点(NULL):用一个空的字符串表示。
* 叶子节点(leaf):Key-end是剩下的Key的半字节编码，value是值。
* 扩展节点(extension):Shared nibble(s)是剩下的重复的Key的半字节编码，next node字段指向另一个节点（一般为分支节点）。
* 分支节点(branch):17元组[v0...v15,vt]。其前16个项对应于这些点在其遍历中的键的十六个可能的半字节值中的每一个。第17个字段是存储在那些在当前节点结束了的节点所存储的值。
叶子节点和扩展节点
~~~
type shortNode struct {
        Key   []byte
        Val   node
        flags nodeFlag
}
~~~
Key：用来存储属于该节点范围的key；<br>
Val：用来存储该节点的内容；<br>

分支节点
~~~
type fullNode struct {
        Children [17]node // Actual trie node data to encode/decode (needs custom encoder)
        flags    nodeFlag
}
// nodeFlag contains caching-related metadata about a node.
type nodeFlag struct {
    hash  hashNode // cached hash of the node (may be nil)
    gen   uint16   // cache generation counter
    dirty bool     // whether the node has changes that must be written to the database
}
~~~
![image](https://github.com/Ashl703/group-xx/assets/138503504/04e20deb-9f9e-4bae-9046-98ebbe30af0a)

## MPT构造过程
1.若当前只有一个kv(key,value)对，则直接将其构造成一个叶子节点。<br>
2.若当前需要编码的kv集合有公共前缀，则提取公共前缀，将其构造成一个扩展节点，并将其第二个字段指向下一个节点（一般为分支节点）。<br>
3.若不是上述两种情况，则构造分支节点按照当前key所在索引的16进制对kv集合进行划分，[0..f]分别指向[0..f]对应半字节所指向的下一个节点。如果有kv对在此节点终结，则将其存储在value中。<br>
在上图的示例中，有公共前缀a7，提取并作为扩展节点，指向分支节点。在分支节点中a711355和a7f9365没有公共前缀，构造成叶子节点，并在叶子节点中存储后面的key（merkle tree 的性质将后面的所有key合并）。a77d337和a77d397有相同前缀，构造扩展节点（merkle tree性质将d和3合并），后接分支节点。然后作为叶节点存储。由于扩展节点并不能代表唯一的key值，所以没有存储value。而叶节点和分支节点会存储value值。上图中的两个分支节点分别可以存储key为a7和a77d3的value值。
## HP编码
HP编码的规则如下：

* 若原key的末尾字节的值为16（即该节点是叶子节点），去掉该字节；
* 在key之前增加一个半字节，其中最低位用来编码原本key长度的奇偶信息，key长度为奇数，则该位为1；低2位中编码一个特殊的终止标记符，若该节点为叶子节点，则该位为1；
* 若原本key的长度为奇数，则在key之前再增加一个值为0x0的半字节；
* 将原本key的内容作压缩，即将两个字符以高4位低4位进行划分，存储在一个字节中（Hex扩展的逆过程）
> 若Hex编码为[3, 15, 3, 13, 4, 10, 16]，则HP编码的值为[32, 63, 61, 74]

## MPT基本操作
### Get
Get(self, node, key)是一个递归查找的过程;<br>
* 如果node是空节点，返回空节点
* 如果node是分支节点，如果key为空，返回分支节点的value；否则递归查找node的子节点，即调用_get(self._decode_to_node(node[key[0]]), key[1:])
* 如果node是叶子节点，返回node[1] if key == curr_key else ‘’
* 如果node是扩展节点，如果key以curr_key开头，递归查找node的子节点，即调用_get(self._decode_to_node(node[1]),key[len(curr_key):])；否则，说明key不在以node为根的子树里，返回空
### Insert
对于一个插入过程，首先找到与新插入节点拥有最长相同路径前缀的节点，记为Node；<br>
若该Node为分支节点：

（1）剩余的搜索路径不为空，则将新节点作为一个叶子节点插入到对应的孩子列表中；

（2）剩余的搜索路径为空（完全匹配），则将新节点的内容存储在分支节点的第17个孩子节点项中（Value）；

若该节点为叶子／扩展节点：

（1）剩余的搜索路径与当前节点的key一致，则把当前节点Val更新即可；

（2）剩余的搜索路径与当前节点的key不完全一致，则将叶子／扩展节点的孩子节点替换成分支节点，将新节点与当前节点key的共同前缀作为当前节点的key，将新节点与当前节点的孩子节点作为两个孩子插入到分支节点的孩子列表中，同时当前节点转换成了一个扩展节点（若新节点与当前节点没有共同前缀，则直接用生成的分支节点替换当前节点）；
若插入成功，则将被修改节点的dirty标志置为true，hash标志置空（之前的结果已经不可能用），且将节点的诞生标记更新为现在；

### Delete

找到与需要插入的节点拥有最长相同路径前缀的节点，记为Node；

若Node为叶子／扩展节点：

（1）若剩余的搜索路径与node的Key完全一致，则将整个node删除；<br>
（2）若剩余的搜索路径与node的key不匹配，则表示需要删除的节点不存于树中，删除失败；<br>
（3）若node的key是剩余搜索路径的前缀，则对该节点的Val做递归的删除调用；<br>

若Node为分支节点：

（1） 删除孩子列表中相应下标标志的节点；<br><br>
（2） 删除结束，若Node的孩子个数只剩下一个，那么将分支节点替换成一个叶子／扩展节点；<br>

若删除成功，则将被修改节点的dirty标志置为true，hash标志置空（之前的结果已经不可能用），且将节点的诞生标记更新为现在；<br>


## 总结
总的来说，MPT具有响应式能力、压缩高效、容易验证等优点，适用于对效率和安全性要求很高的场景，如区块链存储。以太坊的状态树、存储树以及账户、合约地址等的内部实现就是通过MPT的原理实现的。通过MPT能很高效的管理庞大的账户和合约数据。


