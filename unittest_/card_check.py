#encoding:utf-8
__author__ = 'binpo'
def jiaoyanma(shenfenzheng17):
    def haoma_validate(shenfenzheng17):
        print type('310108198510140552')
        if type(shenfenzheng17) in [str,list,tuple]:
            if len(shenfenzheng17) == 17:
                return True
        raise Exception('Wrong argument')

    if haoma_validate(shenfenzheng17):
        if type(shenfenzheng17) == str:
            seq = map(int,shenfenzheng17)
        elif type(shenfenzheng17) in [list,tuple]:
            seq = shenfenzheng17

        t = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
        s = sum(map(lambda x:x[0]*x[1],zip(t,map(int,seq))))
        b = s % 11
        bd={
            0: '1',
            1: '0',
            2: 'x',
            3: '9',
            4: '8',
            5: '7',
            6: '6',
            7: '5',
            8: '4',
            9: '3',
           10: '2'
        }
        print shenfenzheng17
        return bd[b]


import re
#Errors=['验证通过!','身份证号码位数不对!','身份证号码出生日期超出范围或含有非法字符!','身份证号码校验错误!','身份证地区非法!']
def checkIdcard(idcard):
  Errors=['验证通过!','身份证号码位数不对!','身份证号码出生日期超出范围或含有非法字符!','身份证号码校验错误!','身份证地区非法!']
  area={"11":"北京","12":"天津","13":"河北","14":"山西","15":"内蒙古","21":"辽宁","22":"吉林","23":"黑龙江","31":"上海","32":"江苏","33":"浙江","34":"安徽","35":"福建","36":"江西","37":"山东","41":"河南","42":"湖北","43":"湖南","44":"广东","45":"广西","46":"海南","50":"重庆","51":"四川","52":"贵州","53":"云南","54":"西藏","61":"陕西","62":"甘肃","63":"青海","64":"宁夏","65":"新疆","71":"台湾","81":"香港","82":"澳门","91":"国外"}
  idcard=str(idcard)
  idcard=idcard.strip()
  idcard_list=list(idcard)
  #地区校验
  if(not area[(idcard)[0:2]]):
    print Errors[4]
  #15位身份号码检测
  if(len(idcard)==15):
    if((int(idcard[6:8])+1900) % 4 == 0 or((int(idcard[6:8])+1900) % 100 == 0 and (int(idcard[6:8])+1900) % 4 == 0 )):
      erg=re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')#//测试出生日期的合法性
    else:
      ereg=re.compile('[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')#//测试出生日期的合法性
    if(re.match(ereg,idcard)):
      print Errors[0]
    else:
      print Errors[2]
  #18位身份号码检测
  elif(len(idcard)==18):
    #出生日期的合法性检查
    #闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
    #平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
    if(int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10])%4 == 0 )):
      ereg=re.compile('[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')#//闰年出生日期的合法性正则表达式
    else:
      ereg=re.compile('[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')#//平年出生日期的合法性正则表达式
    #//测试出生日期的合法性
    if(re.match(ereg,idcard)):
      #//计算校验位
      S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (int(idcard_list[1]) + int(idcard_list[11])) * 9 + (int(idcard_list[2]) + int(idcard_list[12])) * 10 + (int(idcard_list[3]) + int(idcard_list[13])) * 5 + (int(idcard_list[4]) + int(idcard_list[14])) * 8 + (int(idcard_list[5]) + int(idcard_list[15])) * 4 + (int(idcard_list[6]) + int(idcard_list[16])) * 2 + int(idcard_list[7]) * 1 + int(idcard_list[8]) * 6 + int(idcard_list[9]) * 3
      Y = S % 11
      M = "F"
      JYM = "10X98765432"
      M = JYM[Y]#判断校验位
      if(M == idcard_list[17]):#检测ID的校验位
        print Errors[0]
      else:
        print Errors[3]
    else:
      print Errors[2]
  else:
    print Errors[1]

def check_again():
    import sys

    Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7,9, 10, 5, 8, 4, 2]
    IndexTable = { #此处实际是无需使用字典的，使用一个包含11个元素的数组便可，数组中存放
            0 : '1', #相应位置的号码，但是这也正好演示了Python高级数据结构的使用
            1 : '0',
            2 : 'x',
            3 : '9',
            4 : '8',
            5 : '7',
            6 : '6',
            7 : '5',
            8 : '4',
            9 : '3',
            10 : '2'
        }
    No = []
    sum = 0
    if (len(sys.argv[1:][0]) != 17):
        print "error number"
        sys.exit()
    for x in sys.argv[1:][0]:
            No.append(x)
    for i in range(17):
        sum = sum + (int(No[i]) * Wi[i])
    Index = sum % 11
    print "So, your indicates parity is : %s" % (IndexTable[Index])



USAGE="""\
USAGE: python shenfenzheng.py shenfenzhenghao
"""

chmap = {
  '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
  'x':10,'X':10
  }

def ch_to_num(ch):
  return chmap[ch]

def verify_string(s):
  char_list = list(s)
  num_list = [ch_to_num(ch) for ch in char_list]
  return verify_list(num_list)

def verify_list(l):
  sum = 0
  for ii,n in enumerate(l):
    i = 18-ii
    weight = 2**(i-1) % 11
    sum = (sum + n*weight) % 11

#    print "i=%d,weight=%d,n=%d,sum=%d"%(i,weight,n,sum)

#  print sum
  return sum==1

if __name__=='__main__':
  import sys
  # if len(sys.argv)!=2:
  #   print USAGE
  #   sys.exit(1)
  result = verify_string('310108198510140552')
  if result:
    print "Valid"
  else:
    print "Invalid"

# if __name__ == '__main__':
#     checkIdcard('310108198510140552')
#     print jiaoyanma('310108198510140552')
