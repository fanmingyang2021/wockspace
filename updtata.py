# encode=utf-8
import base64, sqlite3
import binascii
import re


# def select_Task_len():
#     filename = r"D:\python_demo\data_compare\20210927_1043you\20210927_1043you\升级前HF1.0\real_db.db"
#     uuid = "0f3fb2e3-961b-4049-95e2-3596394ca9b7"
#     sum = []
#     suma=[]
#     result=[]
#     conne = sqlite3.connect(filename)
#     conne.text_factory = sqlite3.OptimizedUnicode()
#     cursor = conne.cursor()
#     sqlshell = "SELECT DISTINCT path_id_data FROM Area a,ProxyMap b " \
#                "WHERE a.old=1 AND b.map_id = a.map_id   AND b.uuid= '{}'".format(uuid)
#     c = cursor.execute(sqlshell)
#
#     for row in c:
#         a = binascii.b2a_hex((row[0]))
#         b = bytes.decode(a)
#         try:
#             while b:
#                 ab=b[:2]
#                 aa=b.replace(b[:2],"",1)
#                 b=aa
#                 sum.append(ab)
#
#         except IndentationError:
#             pass
#     print(sum)
#
#     while sum:
#         try:
#             sss = ""
#             for x in range(4):
#                 a = sum.pop()
#                 sss=sss+a
#                 if x==3:
#                     suma.append(sss)
#
#         except IndexError:
#             pass
#     for i in suma:
#         res=int(i,16)
#         result.append(res)
#     print(result)

def select_Zone():
    a=[]
    b=(1,21,23,)
    filename = r"D:\python_demo\data_compare\20210927_1043you\20210927_1043you\升级前HF1.0\real_db.db"
    uuid = "0f3fb2e3-961b-4049-95e2-3596394ca9b7"
    conne = sqlite3.connect(filename)
    cursor = conne.cursor()
    sqlshell = "SELECT path_id FROM Zone a,ProxyMap b " \
               "WHERE b.map_id=a.map_id AND  a.old =1 AND  b.uuid='{}' ".format(uuid)
    cursor.execute(sqlshell)
    result = cursor.execute(sqlshell)
    for i in result:
        a.append(i[0])
    # return tuple(result)
    print(a)
    c=a+b
    print(c)
select_Zone()
