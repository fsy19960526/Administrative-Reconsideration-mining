# Administrative-Reconsideration-minining

------------------------------------------------

### part1：一个对于行政复议文书的爬虫

### part2：通过关键词、文本向量和集成模型对于行政复议失败案例的归因与分类

-------------------------------------------------

### 文档说明：

#### spider:爬虫文档，爬取openlaw与中国裁判文书网的文书正文

1、sel_openlaw_spider：爬取openlaw文书
选取爬取法院名称
```
    root_url = "https://openlaw.cn/search/judgement/type?courtId=&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}"
    #选定爬取的url,实例代码中的分别是：1、北京中院2、北京第二中院3、河北郑州中院4、山东济南中院
    url_list = ['https://openlaw.cn/search/judgement/type?courtId=789a41bf0fd74e07a2a642d9aaba6520&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}',
                'https://openlaw.cn/search/judgement/type?courtId=8d166c5739394a6db7f79a84bc2d624a&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}',
                'https://openlaw.cn/search/judgement/type?courtId=99db8cf5f8594b42abb97150e7904844&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}',
                'https://openlaw.cn/search/judgement/type?courtId=b99edfb9e66c4783b61b44e5825ba0f6&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}']
```
2、docspider：爬取裁判文书网文书（16年以前的数据）

#### key_words：文书关键词发掘，利用jieba分词库，对于败诉文书与胜诉文书的词频进行处理


#### stacking_datamining：文书关键词发掘与stacking分类

1、feature_eng：特征工程，提取文书的重要信息，包括原告法人类别、被告机构类别、庭审程序、庭审类别、关键词等
得到features_dummy文件

生成用于训练的dataset：X.npy、Y.npy

2、model_stacking：模型使用、套用xgb、lgb、rf等模型并stacking集成、得到对于胜诉与否的一个强分类器


#### word2vec：使用word2vec获取意见的每一个分词在word2vec模型的相关性向量。最终得到此篇文章在word2vec模型中的相关性向量。每一篇文书被转化为100维的相关性文本词向量用于训练分类模型


#### 总结：关于项目整体完成的手册


