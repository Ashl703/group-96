import hashlib
if __name__ == '__main__':
    md5 = hashlib.md5()
    msg = "this is a md5 Test."
    md5.update(msg.encode(encoding='utf-8'))
    hash_msg=md5.hexdigest()
    msg_append = "860514"
    msg_extend, hash_extend = extend_length_attack(hash_msg, msg[-2:], len(msg), "hack")
    md5_ = hashlib.md5()
    md5_.update((msg[:-2] + msg_extend).encode(encoding='utf-8'))
    hash_attack = md5_.hexdigest()
    print("原始消息:",msg)
    print("扩展消息:",msg_append)
    print("构造的hash值:", hash_attack)
    print("新消息的hash值:", hash_extend)
    if hash_attack == hash_extend:
        print("长度扩展攻击成功！")
    else:
        print("攻击失败...")
