orders = """
54144428801849
54144428794341
54144428786789
54144428776265
54144428768591
54144428760872
54144428753026
54144428742303
54144428733207
54144428696846
16144428565650
15144428506496
16144428550956
15144428505721
15144428504374
16144428538427
13144428538354
15144428503102
15144428501313
16144428528022
13144428525100
15144428500411
16144428515722
13144428511196
13144428494104
13144428482050
13144428461683
49144428426456
13144428367236
49144428406674
15144428382474
15144428385897
19144428385756
49144428381509
19144428376505
15144427903182
19144428365037
15144427902174
49144428357243
19144428352900
19144428341315
15144427901288
19144428324321
19144428275100
49144428275375
19144428259813
49144428245580
19144428238744
19144428225843
19144428213019
49144428207952
16144428203846
45144428202930
19144428200612
16144428191886
19144428187562
45144428180820
16144428174126
19144428163554
16144428163253
16144428150750
19144428149250
19144428136690
16144428134406
19144428120671
19144428108118
16144428102945
19144428094430
16144428083682
19144428080876
19144428064188
19144428037113
49144428002940
16144428002037
16144427982381
49144427975976
15144427900332
15144427899271
54144427922511
15144427898192
49144427896802
46144427856490
49144427763141
13144427830850
19144427800162
19144427782714
45144427773431
19144427765789
19144427749794
45144427729590
19144427714794
45144427697190
19144427684048
49144427673282
49144427612209
13144427567116
46144427500985
12144427503209
19144427486602
12144427472943
19144427469922
45144427361533
19144427446342
42144427385176
19144427407715
19144427362593
19144427337590
45144427303429
15144427277751
19144427266323
15144427265585
45144427188292
41144427230932
19144420225041
40144426837360
15144426827183
15144426797266
24144426598155
"""
orders_no="""
12144427472943
13144427567116
15144427265585
15144427277751
19144420225041
19144427266323
19144427337590
19144427362593
19144427407715
19144427446342
19144427469922
19144428080876
40144426837360
41144427230932
42144427385176
45144427188292
45144427303429
45144427361533
46144427500985
"""
#sql_form = """insert `api_logs`(`gmt_created`,`gmt_modified`,`deleted`,`logs_type`,`key_params`,`reqeust_url`,`status`) values('2015-10-08 15:44:34','2015-10-08 15:44:38',0,1,'{0}','http://sc.raychina.com.cn:8080/interfaceService/restApi/clearance',0);"""
#for o in orders_no.split():
#    print sql_form.format(o)

g="""
53144427825695
54144429118045
54144429112515
54144429107093
54144429098497
54144429092105
54144429085288
54144429067078
12144427472943
13144427567116
19144420225041
19144427337590
19144427362593
19144427407715
19144427446342
19144427469922
40144426837360
41144427230932
42144427385176
45144427188292
45144427303429
45144427361533
46144427500985
54144429046640
54144429039191
54144429032581
54144429026220
54144429020932
54144429015414
54144429009299
54144429004540
54144428995167
54144428988475
54144428981979
54144428975122
54144428967658
54144428961502
54144428954249
54144428947361
54144428940303
57144428900107
54144428926541
54144428912255
54144428900265
54144428893329
54144428887594
54144428881304
54144428874195
54144428866269
54144428858254
54144428851372
54144428840729
54144428831447
54144428821520
54144428814944
54144428808267
54144428801849
54144428794341
54144428786789
54144428776265
54144428768591
54144428760872
54144428753026
54144428742303
54144428733207
54144428696846
15144428505721
13144428538354
15144428501313
13144428525100
15144428500411
16144428515722
13144428511196
13144428494104
13144428482050
13144428461683
13144428367236
49144428426456
49144428406674
15144428382474
49144428381509
19144428385756
19144428376505
19144428365037
49144428357243
19144428352900
19144428341315
19144428324321
19144428275100
49144428275375
19144428259813
49144428245580
19144428238744
19144428225843
49144428207952
19144428213019
19144428200612
19144428187562
45144428180820
19144428163554
19144428149250
19144428136690
19144428120671
19144428108118
19144428094430
16144428083682
19144428080876
19144428064188
49144428002940
19144428037113
16144428002037
16144427982381
49144427975976
15144427900332
54144427922511
15144427899271
15144427898192
46144427856490
49144427896802
49144427763141
13144427830850
19144427800162
19144427782714
45144427773431
19144427765789
19144427749794
45144427729590
19144427714794
45144427697190
49144427673282
19144427684048
49144427612209
12144427503209
15144426797266
15144426827183
39144410600832
19144427486602
38144396498773
38144388237935
36144368226731
36144368162221
36144368200221
36144368140222
36144368077500
36144368048503
24144366773833
34144361570351
34144361506951
18144360699018
24144360593760
29144360063930
23144360291410
29144360270390
21144360070391
21144359997264
21144360035280
21144359957998
21144359523543
20144359419215"""

print  ''.join(["'"+o+"'," for o in g.split()])