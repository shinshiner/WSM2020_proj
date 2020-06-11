class Case():
    def __init__(self, idx=1):
        self.type = 'case'
        self.data1 = '案号'
        self.data2 = '（2015）浦执字第10396号'
        self.data3 = 'sdajklsjkljdaljs'
        # self.data4 = {'1':1, '2':'a', '3':'123456abc'}
        self.data4 = 1234

        self.k_money = '执行标的金额（元）'
        self.v_money = float(idx)
        self.k_executee = '被执行人'
        self.v_executee = '上海琦沁金属材料有限公司（法定代表人：周建斌）'
        self.k_executor = '申请执行人'
        self.v_executor = '中国民生银行股份有限公司上海分行'
        self.k_court = '承办法院、联系电话'
        self.v_court = '浦东新区人民法院  38794518'

    def __str__(self):
        return str(self.data1) + self.data2 + self.data3



class Instrument():
    def __init__(self, idx=1):
        self.type = 'instrument'
        self.data1 = '案号'
        self.data2 = '（2015）浦执字第10396号'
        self.data3 = 'sdajklsjkljdaljs'
        # self.data4 = {'1':1, '2':'a', '3':'123456abc'}
        self.data4 = 1234

        self.k_title = '标题'
        self.v_title = '王雷与徐金林、江彪提供劳务者受害责任纠纷一审民事判决书责任纠纷一审民事判决书责任纠纷一审民事判决书'
        self.k_category = '文书类别'
        self.v_category = '判决书'
        self.k_reason = '案由'
        self.v_reason = '提供劳务者受害责任纠纷'
        self.k_court = '承办部门'
        self.v_court = '民事审判庭'
        self.k_level = '级别'
        self.v_level = '一审'
        self.k_date = '结案日期'
        self.v_date = '2019-05-'+str(idx)
        self.v_date_sort = float(''.join(self.v_date.split('-')))

    def __str__(self):
        return str(self.data1) + self.data2 + self.data3