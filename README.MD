## usage

### 运行两个容器

```bash
scrapy-splash，这个容器是用来模拟浏览器的请求解析页面:
docker run -it -p 8050:8050 --rm scrapinghub/splash


mongoDB，存储数据:
docker run -d -p 27017:27017 mongo
```

### 爬取命令行示例

比如爬取杭州的java职位信息：
```bash
scrapy crawl bossspider -a location='hangzhou' -a position='java'
```

如果想要输出到文本：
```bash
scrapy crawl bossspider -a location='hangzhou' -a position='java' -o data.csv
```

### 注意事项
注意修改settings.py文件里面的mongoDB配置。