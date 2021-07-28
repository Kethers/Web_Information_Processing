import scrapy
from ..items import TeacherItem
class MySpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["cs.hitsz.edu.cn"]
    start_urls = [
        "http://cs.hitsz.edu.cn/szll/qzjs.htm",
        # "http://cs.hitsz.edu.cn/szll/qzjs/2.htm",
    ]    
    
    def __init__(self, name=None, **kwargs):
        self.teacher_item_list = []
        self.domains = ["http://cs.hitsz.edu.cn/szll/qzjs/"]
        super().__init__(name=name, **kwargs)

    def parse(self, response):
        pass
        teacher_ul = response.xpath("//div[@class='teacher-content']/ul")
        teacher_list = teacher_ul.xpath(".//li")    # xpath相对路径前一定要加“.”
        for index, teacher in enumerate(teacher_list):
            item = TeacherItem()
            item['name']        = teacher.xpath(".//div[@class='teacher-left']/p/text()").extract()
            item['position']    = teacher.xpath(".//div[@class='teacher-box']/dl/dt[contains(text(),'任职：')]/../dd/text()").extract()
            item['phone']       = teacher.xpath(".//div[@class='teacher-box']/dl/dt[contains(text(),'电话：')]/../dd/text()").extract()
            item['fax']         = teacher.xpath(".//div[@class='teacher-box']/dl/dt[contains(text(),'传真')]/../dd/text()").extract()
            item['email']       = teacher.xpath(".//div[@class='teacher-box']/dl/dt[contains(text(),'Email')]/../dd/a/text()").extract()
            item['research']    = teacher.xpath(".//div[@class='teacher-box']/dl/dt[contains(text(),'研究方向：')]/../dd/text()").extract()
            
            # print("===================")
            # print("main span: " + str(teacher.extract()))
            # print("name: " + str(item['name']))
            # print("position: " + str(item['position']))
            # print("phone: ", str(item['phone']))
            # print("fax:", str(item['fax']))
            # print("email: ", str(item['email']))
            # print("research: ", str(item['research']))
            # print("check:")
            # print(len(item['email']))
            # print(teacher.xpath(".//div[@class='teacher-box']/dl/dt[contains(text(),'Email')]/../dd/text()").extract() == None)
            self.teacher_item_list.append(item)
            yield item

        next_link = response.xpath("//span[@class='p_next p_fun']/a/@href").extract()
        if len(next_link)==0:
            return None
        
        next_url = self.domains[0] + next_link[0].split('/')[-1]
        print('next_url',next_url)
        yield scrapy.Request(url=next_url, callback=self.parse)