from hashlib import md5
from .common import SHINGLE_LEN, MIN_LENGTH_FILE, THRESHOLD_VALUE, FILE_DICT


def canonize(text):
    rough_text = ''
    canonize_text = []
    excess_symbols = ['.', ',', ':', ';', '!', '?', '-', '_',
                      '(', ')', '[', ']', '}', '{', '`', '\'',
                      '\"', '&', '\n', '\r', '—']
    excess_words = (u'а', u'и', u'но', u'не', u'что', u'как', u'так',
                    u'на', u'от', u'это', u'в', u'над', u'до', u'за',
                    u'с', u'ли', u'во', u'со', u'для', u'о', u'же',
                    u'ну', u'вы')
    for symbol in text:
        if symbol not in excess_symbols and type(symbol) is str:
            rough_text += symbol.lower()
    for word in rough_text.split():
        if word not in excess_words:
            canonize_text.append(word)
    return canonize_text


def take_hash(list_worlds):
    has_list = []
    for word in list_worlds:
        has_list.append(md5(word.encode('utf-8')).hexdigest())
    return has_list


def generation_shingle(hash_list):
    shingle_list = []
    for i in range(len(hash_list) - (SHINGLE_LEN - 1)):
        shingle_list.append(hash_list[i:i + SHINGLE_LEN])
    return shingle_list


def check_similarity(shingle_list1, shingle_list2):
    same = 0
    for i in range(len(shingle_list1)):
        if shingle_list1[i] in shingle_list2:
            same += 1
    return same * 2 / (len(shingle_list1) + len(shingle_list2)) * 100


def take_shingle(text):
    step1 = canonize(text)
    step2 = take_hash(step1)
    return generation_shingle(step2)


def check_plagiat(text_from_file):
    plagiat_dict = {'originals': []}
    hash_from_new_file = take_shingle(text_from_file)
    if (len(hash_from_new_file)+(SHINGLE_LEN-1)) > MIN_LENGTH_FILE:
        for i in FILE_DICT:
            name = i
            text = FILE_DICT.get(i)
            hash_old_file = take_shingle(text)
            matched = check_similarity(hash_from_new_file, hash_old_file)
            if matched > THRESHOLD_VALUE:
                result_dict = {'filename': name, 'matched': matched, 'text': text}
                plagiat_dict['originals'].append(result_dict)
        if len(plagiat_dict['originals']) > 0:
            return plagiat_dict
        else:
            return True
    else:
        return False
