# FreeForWenku

免费下载百度文库收费资料，支持关键字搜索，以及url批量爬取。目前本项目仅对原项目的doc、txt爬取优化，其余的待完成优化。

本项目fork from： https://github.com/Lz1y/FreeForWenku


## 使用方法：

* ***Step 0：*** Clone项目，安装依赖(本项目基于Python3.6开发)
    ```
    pip install -r requirements.txt
    ```  
 
### 根据关键词批量爬取

* ***Step 1：*** 修改```main.py```中的参数 
    ```
        # 需要修改的参数
        search_word = '一站到底'  #  待搜索关键词
        max_page = 1  # 最大的检索页数
        # 无需求修改的参数
        session = requests.session()
        url_output_dir = os.path.join(os.getcwd(), 'url_outputs')  # 关键词搜索url结果输出位置
        txt_output_dir = os.path.join(os.getcwd(), 'txt_outputs')  # 根据url获取txt文件的输出位置
    ```
* ***Step 2：*** ```run main.py``` 

### 爬取单个doc文件

```
>>> python get_doc.py -url doc_url -out outputs
```


例子：
```
FreeForWenku>>> python get_doc.py -url https://wenku.baidu.com/view/b3ff81bcfbb069dc5022aaea998fcc22bcd14386.html?from=search -out outputs
2019-11-13 16:33:04,641 - utils.logger - DEBUG - Finish process https://wenku.baidu.com/view/b3ff81bcfbb069dc5022aaea998fcc22bcd14386.html?from=search
```

## 文件目录：

```
FreeFromWenku
│  main.py              程序入口
│  README.md            read me
│
├─log
│      error.log        error log
│
├─txt_outputs           根据url获取txt文件的输出位置
│  └─一站到底           每个关键词的相关文件存储在一个文件夹中
│          “一站到底”活动方案.txt
│
├─url_outputs               关键词搜索url结果输出位置
│      一站到底.json        关键词搜索获取的url
│
└─utils
      logger.py             logger      
      url_to_txt.py         包含根据url获取doc和txt文件
      word_to_url.py        搜索关键词，获取结果url
```