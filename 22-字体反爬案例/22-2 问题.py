"""
1.想要获取月票数据的时候
    --elements里面>𘞽𘟆𘟆𘟀𘟇𘟂
    --response里面>&#100285;&#100294;&#100294;&#100288;&#100295;&#100290;
        elements是网页源代码   先有的response 再有的elements
        &#100285;&#100294;&#100294;&#100288;&#100295;&#100290; > 𘞽𘟆𘟆𘟀𘟇𘟂
    --检查一下，月票数据的xpath语法，是会得到空白数据还是&#100285;&#100294;&#100294;&#100288;&#100295;&#100290;
2.字体反爬数据包
    --表面上有三个，经过分析，确定是第三个字体反爬数据包
3.当我们下载了字体反爬文件的数据包，发现打开的是一个乱码
    --需要一个第三方库 pip install fonttools
    --把该字体加密文件，进行一个类型的转换
"""




# import re
#
# str_ = """</style><span class="OhpHUOcw">&#100285;&#100294;&#100294;&#100288;&#100295;&#100290;</span></span>月票</p>"""
#
#
#
# # span标签里面的class属性不固定，不能写固定，经过测试得知
# poll_list = re.findall(r'</style><span class=".*?">(.*?)</span></span>月票</p>',str_)
# print(poll_list)








"""
字体的反爬:
    --正常用户可以看到的正常数据，直接使用爬虫去进行获取，得到的却是看不懂的密文
        --起点的月票数据 电影网站的评论数据 大众点评 
"""

"""
字体反爬是如何实现的
浏览器????
依靠的是数据包 > 单独地做字体反爬的数据包

已经获取到了转换了类型的字体加密文件xml
1 > a 
2 > b 
3 > c 
&#100285;&#100294;&#100294;&#100288;&#100295;&#100290;
关系映射表 {'a':1,'b':2} >> 存在于map部分
因为字体反爬文件不同了，所以不一样

字体反爬数据包的特征:
    --1.每一个网站的都不一样，可以理解是一种加密算法
    --2.是一种后缀为woff的文件
    --3.每一次请求的字体反爬数据包都不一样
"""
# from fontTools.ttLib import TTFont
# # 创建对象
# font_obj = TTFont('NtFlyiPG.woff')
#
# # 转格式(让我们看得懂)
# font_obj.saveXML('font01.xml')
#
# # 获取加密关系映射表
# # xpath语法  正则
# cmap_dict = font_obj.getBestCmap()
# print(cmap_dict)
"""
每一次请求的字体加密文件不一样
&#100285;&#100294;&#100294;&#100288;&#100295;&#100290;  response得到的数据   866102
{100285: 'eight', 100294: 'six', 100288: 'one', 100295: 'zero', 100290: 'two', 100349: 'five', 100350: 'four', 100351: 'nine', 100352: 'three', 100353: 'seven', 100354: 'period'}
进行替换得到明文数据

发现有点不一样 >> 发生了自动转义 response里面的就是经过了转义之后的数据
0x187f7 > eight
100343  > eight
"""
# a = "0x187f7"
# aa = int(a,16)   # 16进制的一个转义
# print(aa)


# 替换掉response加密月票数据的特殊符号
# font = '100285,100294,100294,100288,100295,100290'
#
# # 把加密映射表里面的英文，替换成中文
# dict_ = {100285: 'eight', 100294: 'six', 100288: 'one', 100295: 'zero', 100290: 'two', 100349: 'five', 100350: 'four', 100351: 'nine', 100352: 'three', 100353: 'seven', 100354: 'period'}
#
# dict_e_a = {
#     'one':'1','two':'2','three':'3','four':'4','five':'5',"six":'6',"seven":'7',"eight":"8","nine":'9','zero':'0','period':'.'
# }
#
# for i in dict_:   # 这个dict_字典它的值 等于 dict_e_a它的键名
#     for j in dict_e_a:
#         if dict_[i] == j:
#             dict_[i] = dict_e_a[j]
#
# print('解析之后的字体加密关系映射表:',dict_)

"""
1.书名列表
2.月票数据密文列表 [&#100285;&#100294;&#100294;&#100288;&#100295;&#100290;&#100285;&#100294;&#100294;&#100288;&#100295;&#100290;]
3.拿到了解析之后的关系映射表 {100285: '8', 100294: '6', 100288: '1', 100295: '0', 100290: '2', 100349: '5', 100350: '4', 100351: '9', 100352: '3', 100353: '7', 100354: '.'}

"""

"""
1.每一次请求的字体反爬数据包都不一样
    --实时获取  数据包  >> url  寻找数据包的url
    --通过全局搜索，分析到存在于response里面
    --是style标签里面的文本，得到文本之后，再进行正则获取 
"""


import re

str_ = """@font-face { font-family: HvdLMmfU; src: url('https://qidian.gtimg.com/qd_anti_spider/HvdLMmfU.eot?') format('eot'); src: url('https://qidian.gtimg.com/qd_anti_spider/HvdLMmfU.woff') format('woff'), url('https://qidian.gtimg.com/qd_anti_spider/HvdLMmfU.ttf') format('truetype'); } .HvdLMmfU { font-family: 'HvdLMmfU' !important;     display: initial !important; color: inherit !important; vertical-align: initial !important; }"""
# format('eot'); src: url('https://qidian.gtimg.com/qd_anti_spider/HvdLMmfU.woff') format('woff')
res_ = re.findall(r"format\('eot'\); src: url\('(.*?)'\) format\('woff'\)",str_)[0]
print(res_)