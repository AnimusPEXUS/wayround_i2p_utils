import hashlib
import Crypto.Cipher.AES
import pickle

def _fill(num):
    t = ''
    for i in range(num):
        t += 'x'
    return t

def encrypt_data(data, password):
    wrapper = {}
    wrapper['salt'] = ''


    # additional data type checks for security reasons
    suitable_instance = False
    for i in ['dict', 'str', 'unicode']:
        if isinstance(data, eval(i)):
            wrapper['type'] = i
            suitable_instance = True

    if not suitable_instance:
        return None

    wrapper['data'] = data

    pickled = None

    try:
        pickled = pickle.dumps(wrapper)
    except:
        return None

    pickled_l = len(pickled)

    mod = pickled_l % 16.0

    sub = 0
    if mod != 0.0:
        sub = int(16 - mod)

        wrapper['salt'] = _fill(sub)

    try:
        pickled = pickle.dumps(wrapper)
    except:
        return None

    ret = None

    try:
        ret = Crypto.Cipher.AES.new(
            hashlib.md5(password).hexdigest()).encrypt(pickled)
    except:
        return None

    return ret

def decrypt_data(data, password):
    pickled = None
    try:
        pickled = Crypto.Cipher.AES.new(
            hashlib.md5(password).hexdigest()).decrypt(data)
    except:
        return None

    try:
        depickled = pickle.loads(pickled)
    except:
        return None

    # additional data type checks for security reasons
    if not 'type' in depickled:
        return None

    if not isinstance(depickled['type'], str):
        return None

    data_type = None

    if not depickled['type'] in ['dict', 'str', 'unicode']:
        return None

    data_type = depickled['type']
    data_type_evalueated = None
    try:
        data_type_evalueated = eval(data_type)
    except:
        return None


    if not 'data' in depickled:
        return None

    if not isinstance(depickled['data'], data_type_evalueated):
        return None

    ret_data = depickled['data']

    del depickled

    return ret_data
