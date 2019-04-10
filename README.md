# FreeForWenku

免费下载百度文库收费资料，支持url批量爬取。目前本项目仅对原项目的doc、txt爬取优化，其余的待完成优化。

本项目fork from： https://github.com/Lz1y/FreeForWenku


## 使用方法：

### Step 1： 定义需要爬去的文件链接信息

文件链接信息存储在```file_info.json```文件中，存储格式为：
```
[
  {
    "type": "doc",
    "url": "https://wenku.baidu.com/view/9ff1b7e64a7302768e9939f4.html?from=search"
  },````
  {
    "type": "",
    "url": ""
  }
]
```
注意： type的可选值有```DOC TXT```，大小写不限

### Step 2： 运行```FreeForWenku.py```

本脚本支持DOC、TXT文档的爬取，爬去结果会以TXT文件的形式存储在```output```文件夹中，文件命名为```file_title.txt```


### Step 3： Log

运行时的error log存储在```log\error.log```中