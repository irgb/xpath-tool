xpath tutorial: http://zvon.org/xxl/XPathTutorial/General/examples.html

#### rules.yaml:
yaml 语法简介: https://rollout.io/blog/yaml-tutorial-everything-you-need-get-started/

rules中是一系列的解析规则，如
```
com.sznews.sztqb:
  title_xpath:
    - '//div[@class="newsdetatit"]/h3/text()'
  date_xpath:
    - '//div[@class="newsdetatit"]/p/span[contains(text(), "年") and contains(text(), "月") and contains(text(), "日")]/text()'
  author_xpath:
    - ''
  content_xpath: # 注意 content 选择的是html源码，而不是文本
    - '//div[@class="newsdetatext"]'
```

站点 com.sznews.sztqb 包含四个规则: title_xpath, date_xpath, author_xpath, content_xpath, 分别用于提取 标题，日期，作者，正文. 每个站点都应该包含这四个规则.
每个规则都是一个xpath list. 这是为了应对一个站点多套模版的情况. 解析时从上到下依次解析，知道解析出的内容部位空为止. 所以如果站点有多套模版，要保证多个xpath相互不会重复.
其中作者信息不需要提取，所以是一个空list.

**Attention**

1. 难于提取的作者和日期字段可以为空，但标题和正文不能为空
2. 只需要提取出包含内容的最小单元即可，如以下的html:
```html
<tr>
<td align=center>
2018-12-31 12:26:00　　中国水产养殖网 出处：中国天气网&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;浏览量： 3259 次
<a href="#001">我要评论</a>
</td>
</tr>
```
如果要提取date，只需要使用xpath: '//tr/td[@align="center"]/text()' 即可, 程序会自动从中解析出时间
3. xpath 尽量准确，尽量保证网页变化之后，不会抽出错误的内容

#### 准备工作
python 版本 3.6.6, Linux 安装方法:
```bash
CONDA_HOME=/path/to/conda
PYTHON_VERSION=3.6.6
curl -sS -o conda.sh https://repo.continuum.io/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh
bash conda.sh -b -p $CONDA_HOME
$CONDA_HOME/bin/conda install -yq python==$PYTHON_VERSION
rm conda.sh
echo "export CONDA_HOME=$CONDA_HOME" >> ~/.bashrc
echo 'export PATH=$CONDA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```
安装依赖库:
pip install -r requirements.txt --user

#### main.py 使用方法:
python main.py [reversed domain] [base64 coded url]

example:
1. python main.py
读取rules下的所有域名，解析dataset下这些域名文件夹下的所有html文件. 用于全量解析

2. python main.py cn.com.techweb.www
只解析 dataset/cn.com.techweb.www 下的html文件. 用于批量测试一个站点

3. python main.py cn.com.techweb.www aHR0cDovL21pLnRlY2h3ZWIuY29tLmNuL3RtdC8yMDE5LTAyLTAyLzI3MjI5MDAuc2h0bWwK.html
只解析 dataset/cn.com.techweb.www/aHR0cDovL21pLnRlY2h3ZWIuY29tLmNuL3RtdC8yMDE5LTAyLTAyLzI3MjI5MDAuc2h0bWwK.html, 用于测试单个文件的解析效果
