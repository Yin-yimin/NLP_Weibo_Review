## 爬虫数据说明 (见data.xlsx)

#### 【sheet说明】

**铁链女：是搜索关键词爬下来的**

\#丰县八孩：是tag #丰县八孩案一审宣判# 中爬下来的

\#董志民：tag #董志民获刑9年#

\#徐州通报：tag #徐州通报丰县生育八孩女子处理情况#

因为微博只爬到了两千多条数据，将微博有评论且没被屏蔽掉的爬了下来

**铁链女评论：铁链女下的评论**

\#丰县八孩评论：#丰县八孩 的评论

\#董志民评论： #董志民 的评论

\#徐州通报： #徐州通报 的评论

汇总是以上所有sheet表的汇总， 所有的表都删掉了weibo_emoji和texts变量均为空值的数据


#### 【变量说明】

comments_count: 微博评论/评论的评论 的数量

attitudes_count: 点赞数量

reposts_count: 转发数量，微博评论被转发的次数不可得，全按0填充

created_at: 发表时间

status_country, status_province, status_city: IP地址

user_id, id: 为了方便爬虫的变量，可以不用管

isLongText: 是长文本，即为True，长文本在微博显示的时候会隐藏除规定字数之外的部分

user_verified: 有些用户有微博认证，例如大V之类的，粉丝会更多、影响更大

user_gender: 性别

user_follow_count： 用户关注人数量

user_followers_count： 用户粉丝数量

user_verified_reason： 一些认证用户的认证理由

weibo_emoji: 微博自带的emoji不能用输入法表示出来，原文本是带了链接的表情，因此单独弄了一列使用的微博表情

tags: 原微博中带的话题，其中四个话题微博的评论特别简短，反映不出谈到的话题，因此给所有评论都加了它是在哪个词条微博中的评论以做区分

texts: 删除了原文本中的链接、微博表情（另做一列），带的tag的文字

## 情感分析

请按照以下顺序运行

1. SentimentAnalysis.ipynb
- 词云图：保存在output路径下 wordcloud.png
- 基于cemotion的情感极性：保存在output路径下 data_cemotion.xlsx（已与原数据其他列concat）
  - sentiment_polar这一列，[0,1]连续变量，数值越大，表示越可能是positive
- 基于情感词典的情感分类：保存在output路径下 data_emo_classify.xlsx
  - 输出的是情感分类：happy, anger...
  - ps：后续使用过程中，计数类的应该要根据len(words)进行scale

2. 情感分析_Baidu_API.py
- **一共做了两类情感极性：可以相互对比佐证 or 取平均值；看之后怎么处理比较好**
  - 一类是上述的cemotion（BERT预训练模型），一类是调用百度大脑的api（基于Bi-LSTM模型，能够充分融合上下文的语义进行情感分析，**准确率较高**）
- 这一文件是基于百度大脑的情感极性分析
- 输出：output/df_baidu.csv【尚未与其他列merge】
  - pm：情感正负；pp：positive的可能性；np：negative的可能性（pp+np=1）

3. emotion_score.py
- 基于情感词典（见dictionary目录）输出情感分数
- 输出output/emotion_score.csv【采用百度大脑api处理情感分类后的文件，尚未与其他列merge】
- **这个具体算的逻辑是自由的，可以再看看！！！我想用情感极性来代表情绪的强弱（区别于positive or negative）**

4. 文本处理.ipynb
- 进行一些表格的处理合成

目前所有数据汇总在这张表里：data_process_all.xlsx

【变量说明】
cemotion_senti：基于cemotion得到的情感极性，[0,1]，越靠近1，越positive；可以认为超过0.5是正，小于0.5是负；
<br/> 
baidu_pm：百度api调用得到的情感正负；

baidu_pp：百度api调用得到的positive的概率；

baidu_np：百度api调用得到的negative的概率；
<br/> 
length：分词总数；

positive：正向单词数（基于规则，见SentimentAnalysis.ipynb中）；

negative：负向单词数；

anger：分类单词数；

disgust：分类单词数；

fear：分类单词数；

sadness：分类单词数；

surprise：分类单词数；

good：分类单词数；

happy：分类单词数；

words：分词（去除停用词和标点符号）；

emo_score：情绪强度（这里的计算看看要不要调整，因为带正负，思考要不要绝对值还是什么）。


PS:如果重复跑的话，记得把文件删掉再run，不然写入的表格行数会累加
PPS：API调用那个尽量别跑了，免费调用额度有限   (我的账号key：'edm1TDwkPh6xlFEeCh9k7u1hH9HkW1tF')


## 综合强度计算

1.文本情感强度计算

weighted_score：结合百度API输出的情感极性、是否为长文本、情感强度及使用emoji的数量，加权所得的文本情感强度



2.微博话题强度计算

START：数据起始时间

END：数据终止时间

h：单个时间戳长度

start：储存每个时间戳起始时间

C：每个时间戳内对应的话题讨论度（由转评赞及文本数量计算所得）

Stext：每个时间戳内文本的文本情感强度总和

Stopic：每个时间戳对应的话题强度


3.综合情感计算及舆情变化趋势检测

SE：通过Stext与Stopic计算所得，各时间戳内的综合情感值

y：SE变化趋势，即揭示话题热度（包括情感强度）的变化

PS：由于随起止时间、时间戳长度的不同，C、SE也会变化，本代码并未将输出储存为文件，若有需求可自行输出