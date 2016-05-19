#encoding:utf-8
__author__ = 'binpo'

def img_compression(img_size=0,img_type=''):
    '''
        jpg格式压缩
        原图:876K
        80q压缩:134
        43q压缩:70
        30q压缩:55
    '''
    paras=''

    img_size = img_size and int(img_size) or 0
    if img_size>4000:
        return '@50q_0r.jpg'
    elif img_size>3000:
        return  '@60q_0r.jpg'
    elif img_size>2000:
        return  '@65q_0r.jpg'
    elif  img_size>1000:
        return  '@70q_0r.jpg'
    elif  img_size>500:
        return  '@90q_0r.jpg'
    elif img_size<300:
        return ''#'@100q_0r.jpg'
    else:
        return '@80q_0r.jpg'

def img_qulities_compression(img_size=0,img_type=''):
    '''
        质量压缩率处理
    '''
    img_size = img_size/1000
    if img_size>4000:
        return '50'
    elif img_size>3000:
        return  '60'
    elif img_size>2000:
        return  '65'
    elif  img_size>1000:
        return  '70'
    elif  img_size>500:
        return  '90'
    elif img_size<300:
        return '100'#'@100q_0r.jpg'
    else:
        return '80'