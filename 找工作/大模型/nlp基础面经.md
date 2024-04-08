# 评价篇：

#### 1.n-gram

n代表连续的n个词的组合*。"n"可以是1、2、3，或者更高。

#### 2.BLEU 和ROUGE

BLEU（Bilingual Evaluation Understudy）： BLEU是一种用于评估机器翻译结果质量的指标。它主要侧重于衡量机器翻译输出与参考翻译之间的相似程度，**着重于句子的准确性和精确匹配**。BLEU通过计算N-gram（连续N个词）的匹配程度，来评估机器翻译的精确率（Precision）。

ROUGE（Recall-Oriented Understudy for Gisting Evaluation）： ROUGE是一种用于评估文本摘要（或其他自然语言处理任务）质量的指标。与BLEU不同，ROUGE主要关注机器生成的摘要中是否捕捉到了参考摘要的信息，**着重于涵盖参考摘要的内容和信息的完整性**。ROUGE通过计算N-gram的共现情况，来评估机器生成的摘要的召回率（Recall）。

一个例子理解BLEU 和ROUGE的计算过程

让我们通过一个简单的例子来解释BLEU（Bilingual Evaluation Understudy）和ROUGE（Recall-Oriented Understudy for Gisting Evaluation）指标的计算过程。

假设我们有两个句子，一个是参考翻译（Reference Translation），另一个是系统生成的翻译（Candidate Translation）。

参考翻译： "**今天天气晴朗**。"

系统生成的翻译： "**今天的天气是晴朗的**。"

我们将使用这两个句子来计算BLEU和ROUGE指标。

- BLEU指标计算过程：

a. 首先，我们将参考翻译和系统生成的翻译拆分成n-gram序列。n-gram是连续n个词的组合。

参考翻译的1-gram：["今天", "天气", "晴朗", "。"]

系统生成的翻译的1-gram：["今天", "的", "天气", "是", "晴朗", "的", "。"]

b. 接下来，我们计算系统生成的翻译中n-gram与参考翻译中n-gram的匹配数。例如，1-gram中有3个匹配：["今天", "天气", "晴朗"]

c. **计算BLEU的精确度（precision）**：将系统生成的翻译中的**匹配数除以系统生成的翻译的总n-gram数**。在这里，精确度为3/7。

d. 由于较长的翻译可能具有较高的n-gram匹配，我们使**用短文本惩罚（brevity penalty）来调整精确度**。短文本惩罚**可以防止短翻译在BLEU中得分过高。**

e. 最后，计算BLEU得分：BLEU = 短文本惩罚 * exp(1/n * (log(p1) + log(p2) + ... + log(pn)))

其中，p1, p2, ..., pn是1-gram, 2-gram, ..., n-gram的精确度，n是n-gram的最大长度。



- ROUGE指标计算过程：**着重于信息完整性和涵盖程度**

a. ROUGE指标是**用于评估文本摘要任务的**，因此我们**将参考翻译和系统生成的翻译视为两个文本摘要**。

b. 首先，我们计算系统生成的翻译中包含的n-gram在参考翻译中出现的次数。

c. 接下来，计算召回率（recall）：**将匹配的n-gram总数除以参考翻译中的总n-gram数**。例如，1-gram中有3个匹配，参考翻译总共有4个1-gram，因此召回率为3/4。

d. ROUGE得分可以根据需要使用不同的n-gram大小，通常使用ROUGE-1、ROUGE-2和ROUGE-L。

ROUGE-1 = 召回率（系统生成的1-gram匹配数 / 参考翻译中的1-gram总数）

ROUGE-2 = 召回率（系统生成的2-gram匹配数 / 参考翻译中的2-gram总数）

ROUGE-L = 最长公共子序列（Longest Common Subsequence，LCSS）的长度 / 参考翻译的总长度

请注意，这里的计算过程只是为了帮助理解，实际上，BLEU和ROUGE指标的计算还涉及一些调整和平滑方法，以便更好地评估翻译和文本摘要的质量

### 分词器

大模型分词算法：

​	BPE、WordPiece和Unigram

##### BPE

其基本思路也比较简单，也就是从基本的字母开始，然后不断合并字母，形成“单词”，也就是以“合并”的方法不断“增量”构建词典，并形成对应的分词算法。

BPE获得Subword的步骤如下：

1. 准备足够大的训练语料，并确定期望的Subword词表大小；
2. 将单词拆分为成最小单元。比如英文中26个字母加上各种符号，这些作为初始词表；
3. 在语料上统计单词内相邻单元对的频数，选取频数最高的单元对合并成新的Subword单元；
4. 重复第3步直到达到第1步设定的Subword词表大小或下一个最高频数为1.

对于给定的单词`mountain</w>`，其分词结果为：[`moun`, `tain</w>`]

### **语料解码**

语料解码就是将所有的输出子词拼在一起，直到碰到结尾为`<\w>`。举个例子，假设模型输出为：

```text
["moun", "tain</w>", "high", "the</w>"]
```

作者：谢利昂D忒待儿
链接：https://zhuanlan.zhihu.com/p/383650769
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。