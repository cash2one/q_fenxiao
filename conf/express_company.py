#encoding:utf-8
__author__ = 'wangjinkuan'

express_company = {'ems':'EMS',
                   'huitongkuaidi':'汇通快运',
                   'jiajiwuliu':'佳吉物流',
                   'shunfeng':'顺丰速递',
                   'tiantian':'天天快递',
                   'tnt':'TNT',
                   'ups':'UPS',
                   'zhaijisong':'宅急送',
                   'yuantong':'圆通速递',
                   'yunda':'韵达快运',
                   'shentong':'伸通'
                   }



'''
fedexcn	Fedex-国际件-中文结果
fedexus	Fedex-美国件-英文结果(说明：如果无效，请偿试使用fedex）
feikangda	飞康达物流
feikuaida	飞快达
rufengda	凡客如风达
fengxingtianxia	风行天下
feibaokuaidi	飞豹快递
G
ganzhongnengda	港中能达
guotongkuaidi	国通快递
guangdongyouzhengwuliu	广东邮政
youzhengguonei	挂号信（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
youzhengguonei	国内邮件（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
youzhengguoji	国际邮件（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
gls	GLS
gongsuda	共速达
H
huitongkuaidi	汇通快运
huiqiangkuaidi	汇强快递
tiandihuayu	华宇物流
hengluwuliu	恒路物流
huaxialongwuliu	华夏龙
tiantian	海航天天
haiwaihuanqiu	海外环球
hebeijianhua	河北建华（暂只能查好乐买的单，其他商家要查，请发邮件至 wensheng_chen#kingdee.com(将#替换成@)开通权限
haimengsudi	海盟速递
huaqikuaiyun	华企快运
haihongwangsong	山东海红
J
jiajiwuliu	佳吉物流
jiayiwuliu	佳怡物流
jiayunmeiwuliu	加运美
jinguangsudikuaijian	京广速递
jixianda	急先达
jinyuekuaidi	晋越快递
jietekuaidi	捷特快递
jindawuliu	金大物流
jialidatong	嘉里大通
K
kuaijiesudi	快捷速递
kangliwuliu	康力物流
kuayue	跨越物流

lianhaowuliu	联昊通
longbanwuliu	龙邦物流
lanbiaokuaidi	蓝镖快递
lejiedi	乐捷递（暂只能查好乐买的单，其他商家要查，请发邮件至 wensheng_chen#kingdee.com(将#替换成@)开通权限
lianbangkuaidi	联邦快递（Fedex-中国-中文结果）（说明：国外的请用 fedex）
lianbangkuaidien	联邦快递(Fedex-中国-英文结果）
lijisong	立即送（暂只能查好乐买的单，其他商家要查，请发邮件至 wensheng_chen#kingdee.com(将#替换成@)开通权限)
longlangkuaidi	隆浪快递
M
menduimen	门对门
meiguokuaidi	美国快递
mingliangwuliu	明亮物流
O
ocs	OCS
ontrac	onTrac
Q
quanchenkuaidi	全晨快递
quanjitong	全际通
quanritongkuaidi	全日通
quanyikuaidi	全一快递
quanfengkuaidi	全峰快递
sevendays	七天连锁
R
rufengda	如风达快递
shentong	伸通（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
shunfeng	顺丰速递（中文结果）（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
shunfengen	顺丰（英文结果）（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
santaisudi	三态速递
shenghuiwuliu	盛辉物流
suer	速尔物流
shengfengwuliu	盛丰物流
shangda	上大物流
santaisudi	三态速递
haihongwangsong	山东海红
saiaodi	赛澳递
haihongwangsong	山东海红（暂只能查好乐买的单，其他商家要查，请发邮件至 wensheng_chen#kingdee.com(将#替换成@)开通权限）
sxhongmajia	山西红马甲（暂只能查天天网的单，其他商家要查，请发邮件至 wensheng_chen#kingdee.com(将#替换成@)开通权限)
shenganwuliu	圣安物流
suijiawuliu	穗佳物流
T
tiandihuayu	天地华宇
tiantian	天天快递
tnt	TNT（中文结果）
tnten	TNT（英文结果）
tonghetianxia	通和天下（暂只能查好乐买的单，其他商家要查，请发邮件至 wensheng_chen#kingdee.com(将#替换成@)开通权限）
U
ups	UPS（中文结果）
upsen	UPS（英文结果）
youshuwuliu	优速物流
usps	USPS（中英文）
W
wanjiawuliu	万家物流
wanxiangwuliu	万象物流
weitepai	微特派（暂只能查天天网的单，其他商家要查，请发邮件至 wensheng_chen#kingdee.com(将#替换成@)开通权限)
X
xinbangwuliu	新邦物流
xinfengwuliu	信丰物流
xingchengjibian	星晨急便（暂不支持，该公司已不存在）
xinhongyukuaidi	鑫飞鸿（暂不支持，该公司已不存在）
cces	希伊艾斯(CCES)（暂不支持，该公司已不存在）
xinbangwuliu	新邦物流
neweggozzo	新蛋奥硕物流
hkpost	香港邮政
Y
yuantong	圆通速递（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
yunda	韵达快运（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
yuntongkuaidi	运通快递
youzhengguonei	邮政小包（国内），邮政包裹（国内）、邮政国内给据（国内）（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
youzhengguoji	邮政小包（国际），邮政包裹（国际）、邮政国内给据（国际）（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
yuanchengwuliu	远成物流
yafengsudi	亚风速递
yibangwuliu	一邦速递
youshuwuliu	优速物流
yuanweifeng	源伟丰快递
yuanzhijiecheng	元智捷诚
yuefengwuliu	越丰物流
yuananda	源安达
yuanfeihangwuliu	原飞航
zhongxinda	忠信达快递
zhimakaimen	芝麻开门
yinjiesudi	银捷速递
yitongfeihong	一统飞鸿（暂只能查天天网的单，其他商家要查，请发邮件至 wensheng_chen#kingdee.com(将#替换成@)开通权限)
Z
zhongtong	中通速递（暂只支持HtmlAPI,要JSON、XML格式结果和签收状态state请联系企业QQ 800036857 转“小佰”）
zhaijisong	宅急送
zhongyouwuliu	中邮物流
zhongxinda	忠信达
zhongsukuaidi	中速快件
zhimakaimen	芝麻开门
zhengzhoujianhua	郑州建华（暂只能查好乐买的单，其他商家要查，请发邮件至 wensheng_chen#kingdee.com(将#替换成@)开通权限）
zhongtianwanyun	中天万运
'''