import xlwt
import os
from simspider.conf import text1, text2, result_file
#
current_file_path = os.path.dirname(os.path.abspath(__file__))
read_file_path = current_file_path+"/simspider/待处理/"
cache_file_path = current_file_path+"/simspider/临时目录/"
write_file_path = current_file_path+"/simspider/已处理/"

# 读取文件
with open(read_file_path+str(text1), "r", encoding="UTF-8") as f:
    jtext = f.readlines()

# 读取临时目录
with open(cache_file_path+result_file.replace("xls", "txt"), "r", encoding="UTF-8") as f:
    cache_text = f.readlines()

# ct2_set = set()
# for ct in cache_text:
#     ct2_set.add(ct.split(",")[-2])
#
# # 初始化excel
# f = xlwt.Workbook()
# sheet = f.add_sheet("短文本相似", cell_overwrite_ok=False)
#
# for t in jtext:
#     sheet.write(jtext.index(t)+1, t)
# ct2_list = list(ct2_set)

for jt in jtext:
    with open(write_file_path+result_file.replace("xls", "txt"), "a", encoding="UTF-8") as f:
        f.write(("\n" if jtext.index(jt) else "")+"Q"+str(jtext.index(jt)+1) + "\t" + jt.strip() + "\n")
    for ct in cache_text:
        if jt.strip() == ct.split(",")[-2].strip():
            with open(write_file_path+result_file.replace("xls", "txt"), "a", encoding="UTF-8") as f:
                f.write(str("%.3f"%float(ct.split(",")[2])) + "\t" + ct.split(",")[-1])