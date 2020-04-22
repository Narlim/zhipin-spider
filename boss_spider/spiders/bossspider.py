# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest


class BossspiderSpider(scrapy.Spider):
    name = 'bossspider'
    
    def __init__(self, location=None, position=None, **kwargs):
        super().__init__(**kwargs)
        self.location = location
        self.position = position
        self.lua_script1 = f'''
        function main(splash, args)
            splash.private_mode_disable = false
            splash:on_request(function(request)
            request:set_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0")')
            end)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(5))
            input_box = assert(splash:select(".ipt-search"))
            input_box:focus()
            input_box:send_text("{self.position}")
            assert(splash:wait(0.5))
            input_box:send_keys("<Enter>")
            assert(splash:wait(10))
            return splash:html()
        end
        '''
        self.lua_script2 = f'''
        function main(splash, args)
            splash.private_mode_disable = false
            splash:on_request(function(request)
            request:set_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0")')
            end)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(5))
            return splash:html()
        end
        '''

    def start_requests(self):
        yield SplashRequest(url=f"https://www.zhipin.com/{self.location}/",
                            callback=self.parse,
                            endpoint="execute",
                            args={'lua_source': self.lua_script1})
    

    def parse(self, response):
        for job in response.xpath("//div[@class='job-primary']"):
            yield {
                'job_name': job.xpath(".//span[@class='job-name']/a/text()").get(),
                'job_area': job.xpath(".//span[@class='job-area']/text()").get(),
                'company': job.xpath(".//div[@class='company-text']/h3/a/text()").get(),
                'salary': job.xpath(".//span[@class='red']/text()").get(),
                'required': job.xpath(".//div[@class='job-limit clearfix']/p/text()").get().replace('\n', ' ')
            }

        next_page = response.xpath("//a[@class='next']/@href").get()
        if next_page:
            yield SplashRequest(url=f"https://www.zhipin.com{next_page}",
                            callback=self.parse,
                            endpoint="execute",
                            args={'lua_source': self.lua_script2})
