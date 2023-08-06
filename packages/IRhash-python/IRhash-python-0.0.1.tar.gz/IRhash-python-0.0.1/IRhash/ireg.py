import hashlib

def Ireg(text):
    hash_1 = hashlib.sha256(text.encode()).hexdigest()
    hash_2 = hashlib.sha256(hash_1.encode()).hexdigest()
    hash_3 = hashlib.sha256(hash_2.encode()).hexdigest()
    hash_4 = hashlib.sha256(hash_3.encode()).hexdigest()
    hash_5 = hashlib.sha256(hash_4.encode()).hexdigest()
    main_hash = hash_1+hash_3+hash_5+hash_4+hash_2
    perfect_hash_1 = main_hash[27:43]
    perfect_hash_2 = main_hash[15:31]
    perfect_hash_3 = main_hash[40:56]
    final_hash = perfect_hash_1+perfect_hash_2+perfect_hash_3
    return final_hash


