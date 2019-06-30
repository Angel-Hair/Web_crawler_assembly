# 我的爬虫程序库

这里是我用来存放用于数据分析的爬虫程序的库，实现语言为 Python，测试环境为 window10 专业版，编辑软件为 VS code。

因为这些程序都是我在竞赛和做分析时写的，可能比较粗糙，大家见谅（逃）

## 直接对接的爬虫

### cnki

tools: Selenium、Geckodriver、FireFox-headless、PyQt5

这个例子是用来爬取知网上指定关键字搜索的前200页（可改）所有论文的一些信息（标题、作者、摘要、关键字）。**因为用到了 Geckodriver 所以注意程序执行目录下面一定有 `geckodriver.exe` 文件！**

实现细节： 搜索页面（父级页面）是直接用 Selenium 对接 FireFox-headless 模式实现的，论文详情页面（子级页面）是直接用 requests 和 HTMLParser 库处理的。界面用 PyQt5 多线程做的。

## 基于Scrapy的爬虫

### chengduqiye

tools：Scarpy

这个例子用的是顺企网的成都信息与计算机企业黄页，由于顺企网没有整合页面，所以如果要爬取其他地域或者行业，需要把 `url` 改为对应的地址。

实现细节： 注意使用了 `Item Pipeline` 来清理数据。

### lagouwangpaqu

tools: Scarpy、Selenium、Geckodriver、FireFox-headless

这个例子用的是拉勾网所有企业的爬取，**注意修改 `headers` 和设置 `start` 和 `max_list` **，分别对应最低存在企业页面数（2018.11.30测试结果为7页开始有企业）和最高企业数（首页有公布数据），爬取二级信息（招聘）的代码被我注释掉了（包括Downloader Middleware），有需要的可以解开使用。

值得一提的是拉勾网默认企业名录只显示20页，很明显，没有显示全部，所以这里是直接穷举了所有企业的链接。

实现细节： Scrapy下载中间件（Downloader Middleware）对接 Selenium 实现的，Selenium 驱动 FireFox-headless 模式，需要额外支持 Geckodriver 。  
**PS：PhantomJS已死,有事烧纸。**

## 关于远程部署到Linux上的建议

远程ssh在linux上用Scrapy对接Selenium的爬虫的时候，就算用nohup &命令在后台挂起，当你关掉ssh连接的时候，还是会关掉附属进程，然后Scrapy会直接pass掉剩下的所有页面。  
解决方案是不要用ssh，用VNC或者其他远程桌面协议连接，然后在桌面上开终端运行命令（都不用挂后台了...而且测试headers和cookie的时候用图像界面的浏览器方便些...）

测试服务器： Debian 9
测试工具： Xshell 、VNC Viewer

## 参考

* [Scrapy 1.5 documentation](https://doc.scrapy.org/en/latest/index.html)
* [Scrapy 对接 Selenium](https://cloud.tencent.com/developer/article/1005650)
* [Selenium with Python中文翻译文档](https://selenium-python-zh.readthedocs.io/en/latest/index.html)
* [html.parser——简单的 HTML 和 XHTML 解析器](https://docs.python.org/zh-cn/3.7/library/html.parser.html?highlight=htmlparser#html.parser.HTMLParser.reset)
