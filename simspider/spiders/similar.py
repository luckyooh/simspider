# -*- coding: utf-8 -*-
import json
import os

import scrapy
from ..conf import result_file, token1, token2, token3, text1, text2, token4, token5

class SimilarSpider(scrapy.Spider):
    name = 'similar'

    current_file_path = os.path.dirname(os.path.abspath(__file__))
    read_file_path = current_file_path[:-7]+"待处理/"
    cache_file_path = current_file_path[:-7]+"临时目录/"

    headers = {
        "Content-Type": "application/json"
    }
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?charset=UTF-8&access_token={}"

    def start_requests(self):
        global text1, text2
        # 读取文件
        with open(self.read_file_path+str(text1), "r", encoding="UTF-8") as f:
            jtext = f.readlines()
        with open(self.read_file_path+str(text2), "r", encoding="UTF-8") as f:
            mtext = f.readlines()

        b = (1 if text1==text2 else 0)

        for i in range((len(jtext)-1) if b else len(jtext)):
            for j in range((i+1) if b else 0, len(mtext)):
                json_data = {
                    "text_1": jtext[i].strip(),
                    "text_2": mtext[j].strip()
                }
                msg = {
                    "x": j+1,
                    "y": i+1
                }
                m = j%5
                n = m%5
                if n==0:
                    token = token1
                elif n==1:
                    token = token2
                elif n==2:
                    token = token3
                elif n==3:
                    token = token4
                elif n==4:
                    token = token5
                yield scrapy.Request(url=self.url.format(token), method="post", body=json.dumps(json_data), headers=self.headers,dont_filter=True, meta=msg)

    def parse(self, response):
        html = json.loads(response.text)
        x = response.meta.get("x")
        y = response.meta.get("y")
        try:
            score = html["score"]
            text1 = html["texts"]["text_1"]
            text2 = html["texts"]["text_2"]
            if float(score)>0.75:
                with open(self.cache_file_path+result_file.replace("xls", "txt"), "a", encoding="UTF-8") as f:
                    f.write(str(x)+","+str(y)+","+str(score)+","+text1.strip().replace(",", "，")+","+text2.strip().replace(",", "，")+"\n")
        except:
            print(html)