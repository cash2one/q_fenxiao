#encoding:utf-8
__author__ = 'binpo'


import random
_letter_cases = "abcdefghjkmnpqrstuvwxy" # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper() # 大写字母
_numbers = ''.join(map(str, range(3, 10))) # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


def get_chars():
    '''生成给定长度的字符串，返回列表格式'''
    return ''.join(random.sample(init_chars,int(random.random()*10)))

def create_random_digit(n):
    # random.randint(10, 100)
    ran_str=''
    for x in xrange(n):
        ran_str+=str(random.randint(10,99))
    return ran_str


import string
def get_random_char(digit):
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for x in range(random.randint(6, digit)))
    return password


#print create_random_digit(2)