# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ChengduqiyePipeline(object):
    def process_item(self, item, spider):

        print(item['product'])
        item['product']=item['product'][4:-5]
        item['product']=item['product'].replace('（未取得相关行政许可（审批） , 不得开展经营活动）','')
        item['product']=item['product'].replace('【依法须经批准的项目 , 经相关部门批准后方可开展经营活动 , 未取得相关行政许可（审批） , 不得开展经营活动】','')
        item['product']=item['product'].replace('（依法须经批准的项目 , 经相关部门批准后方可开展经营活动）','')
        
        # 删除括号及其里面的内容
        # 注意改后采用了倒叙检查，因为一般情况下省略的是')'而不是'('
        # !!!此算法已被禁用，列外：(asd(asd)(asd
        aitem = item['product']
        while '（' in aitem:
            if '）' not in aitem:
                insybo = aitem[aitem.find('（'):]
            else:
                insybo = aitem[aitem.find('（'):aitem.find('）')+1]
            aitem = aitem.replace(insybo,'')
        while '(' in aitem:
            if ')' not in aitem:
                insybo = aitem[aitem.find('('):]
            else:
                insybo = aitem[aitem.find('('):aitem.find(')')+1]
            aitem = aitem.replace(insybo,'')
        while '【' in aitem:
            if '】' not in aitem:
                insybo = aitem[aitem.find('【'):]
            else:
                insybo = aitem[aitem.find('【'):aitem.find('】')+1]
            aitem = aitem.replace(insybo,'')
        item['product'] = aitem
        # 取消上述算法，列外：(),asd(asd(asd)(asd,()
        # ——成功证明有能实现“括号内数据清理”的有效算法在能够承受的时间复杂度内无法实现，采用第一版本的算法，虽然会造成无效数据，但是影响不大，可以继续使用（具体的证明来我寝室找我要纸）
        
        products = item['product'].split(',')
        
        # # 删除前后空格
        # for product in products:
        #     products[products.index(product)] = product.strip()
        
        for product in products:
            re_product = product
            
            # 提取超链接中的文字
            if "a href" in re_product:
                re_product = re_product[re_product.find('>')+1:re_product.rfind('<')]
            
            # 删除'。'、' '和'.'
            re_product = re_product.replace('。','')
            re_product = re_product.replace(' ','')
            re_product = re_product.replace('.','')

            # 例如：'销售：水果' ——> '水果'
            if '：' in re_product:
                re_product = re_product[re_product.index('：')+1:]
            if ':' in re_product:
                re_product = re_product[re_product.index(':')+1:]

            products[products.index(product)] = re_product

        item['product'] = products
        return item