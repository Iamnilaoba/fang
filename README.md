screpy-redis分布式爬虫写法：

1. 创建爬虫项目

   1. 创建爬虫项目:

      scrapy startproject aa  -------->创建一个爬虫项目（aa）

   2. 创建普通爬虫程序：

      scrapy genspider xh xiaohuar.com ——->创建普通爬虫程序（有多种创建方法）

      scrapy genspider -t crawl xh xiaohuar.com —————–>使用crawl模板创建爬虫程序

      xh：程序名称           xiaohuar.com：要爬取的域名

   3. 文件说明：

      - scrapy.cfg  项目的配置信息，主要为Scrapy命令行工具提供一个基础的配置信息。（真正爬虫相关的配置信息在settings.py文件中）
      - items.py    设置数据存储模板，用于结构化数据，如：Django的Model
      - pipelines    数据处理行为，如：一般结构化的数据持久化
      - settings.py 配置文件，如：递归的层数、并发数，延迟下载等
      - spiders      爬虫目录，如：创建文件，编写爬虫规则

2. 写爬虫

   详细代码请下载参考上面代码部分

3. 修改爬虫，使其成为分布式爬虫

   要将一个`Scrapy`项目变成一个`Scrapy-redis`项目只需修改以下三点就可以了：

   1. 将爬虫的类从`scrapy.Spider`变成`scrapy_redis.spiders.RedisSpider`；或者是从`scrapy.CrawlSpider`变成`scrapy_redis.spiders.RedisCrawlSpider`。
   2. 将爬虫中的`start_urls`删掉。增加一个`redis_key="xxx"`。这个`redis_key`是为了以后在`redis`中控制爬虫启动的。爬虫的第一个url，就是在redis中通过这个发送出去的。
   3. 在配置文件中增加如下配置：

   ```python
       # Scrapy-Redis相关配置
       # 确保request存储到redis中
       SCHEDULER = "scrapy_redis.scheduler.Scheduler"
   
       # 确保所有爬虫共享相同的去重指纹
       DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
   
       # 设置redis为item pipeline
       ITEM_PIPELINES = {
           'scrapy_redis.pipelines.RedisPipeline': 300
       }
   
       # 在redis中保持scrapy-redis用到的队列，不会清理redis中的队列，从而可以实现暂停和恢复的功能。
       SCHEDULER_PERSIST = True
   
       # 设置连接redis信息
       REDIS_HOST = '127.0.0.1'
       REDIS_PORT = 6379
   ```

4. 部署到服务器

   1.window系统可直接使用pycharm进行上传，上传到远程服务器上（上传之前请导入本地项目所用到的包）

   ​    pycharm命令行输入：pip freeze > aa.txt    （项目里的包全导入在aa.txt里，方便远程服务器下载）

   2.Mac系统可通过cmd命令行使用scp命令拷贝本地项目到远程服务器上（也可使用pycharm上传）

   3.在远程服务器上cd到aa.txt当前文件夹里，通过pip下载项目所需要的包

   ​    pip install -r aa.txt

   备注：下载过程中可能会出现某个包下载失败的情况，解决办法：www.baidu.com

5. 开启redis  （远程服务器redis下载：http://www.runoob.com/redis/redis-install.html）

   ```python
   $ cd src
   $ ./redis-server
   ```

6. 启动爬虫

   在爬虫服务器上。进入爬虫文件所在的路径，然后输入命令：`scrapy runspider [爬虫名字]`

7. 外部服务器连接redis

   要想让外部服务器连接到远程服务器redis上，需修改配置文件，将其bind对应的ip地址改为0.0.0.0

8. 爬虫工作

   在`Redis`服务器上，推入一个开始的url链接：`redis-cli> lpush [redis_key] start_url`开始爬取
