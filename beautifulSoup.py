from bs4 import BeautifulSoup
from bs4 import element
import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a> and
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>and they lived at the bottom of a well</p>
"""

# 1.类型转换
# bs4 默认会调用python中的lxml 解析库,会警告提示
# 因此要主动设置调用bs4的解析库
soup = BeautifulSoup(html_doc, 'lxml')
# 2.格式化输出
# result = soup.prettify()
# print(result)
#
# 3.对象种类
# BeautifulSoup将复杂的html文档转换为树形结构，每一个节点都是一个对象，这些对象可以归纳为几种：

# (1)Tag 相当于html种的一个标签  类型:bs4.element.Tag
# <title>标签
title = soup.title
print(title, type(title))  # <title>The Dormouse's story</title> <class 'bs4.element.Tag'>
# <head>标签
head = soup.head
print(head)  # <head><title>The Dormouse's story</title></head>

# 对于Tag，有几个重要的属性：
# name:每个Tag对象的name就是标签本省的名称；
# attrs:每个Tag对象的attrs就是一个字典，包含了标签的全部属性。
print(soup.name)  # [document]
print(soup.a.name)  # a
print(soup.a.attrs)  # {'href': 'http://example.com/elsie', 'class': ['sister'], 'id': 'link1'}
# 所有属性打印输出了出来，得到的类型是一个字典
# 如果我们想要单独获取某个属性，可以这样，例如我们获取它的 class
print(soup.a['class'])  # ['sister']
# 还可以这样
print(soup.a.get('class'))  # ['sister']
# 我们可以对这些属性和内容等等进行修改，例如
soup.a['class'] = 'newclass'
print(soup.a)  # <a class="newclass" href="http://example.com/elsie" id="link1">Elsie</a>
# 还可以对这个属性进行删除，例如
del soup.a['class']
print(soup.a)  # <a href="http://example.com/elsie" id="link1">Elsie</a>

# (2)NavigableString 翻译过来叫 "可以遍历的字符串", 可以省去使用正则表达式的繁琐
# 得到了标签的内容，如果要想获取标签内部的文字怎么办呢？很简单，用 .string 即可,例如
print(soup.p.string)  # The Dormouse's story
print(type(soup.p.string))  # <class 'bs4.element.NavigableString'>
# 因此.string , 它的类型是一个 NavigableString,省去了使用正则表达式的繁琐
html_doc = '<a class="css1" href="http://example.com/cdd" id="css">abc<!--test-->gh</a>'
bs = BeautifulSoup(html_doc, 'html.parser')
print(bs.a.string)  # None
# 内容是注释和字符串混合，此时可以用contents获取全部对象
print(bs.a.contents)  # ['abc', 'test', 'gh']
# 如果需要忽略注释内容的话，可以利用get_text()或者.text：
print(bs.a.get_text())  # abcgh
print(bs.a.text)  # abcgh
# (3)BeautifulSoup
# BeautifulSoup 对象表示的是一个文档的全部内容.大部分时候,可以把它当作 Tag 对象，是一个特殊的 Tag，我们可以分别获取它的类型，名称，以及属性来感受一下
print(type(soup.name))  # <class 'str'>
print(soup.name)  # [document]
print(soup.attrs)  # {}

# (4)Comment
# Comment 对象是一个特殊类型的 NavigableString 对象，其实输出的内容仍然不包括注释符号，但是如果不好好处理它，可能会对我们的文本处理造成意想不到的麻烦。
html_doc = '''
<a class="css" href="http://example.com/test" id="test"><!-- 注释 --></a>
'''
bs = BeautifulSoup(html_doc, 'html.parser')
print(bs.a)  # <a class="css" href="http://example.com/test" id="test"><!-- 注释 --></a>
print(bs.a.string)  # 注释
print(type(bs.a.string))  # <class 'bs4.element.Comment'>
# a标签的内容是注释,但是使用.string仍然输出了,这种情况下,我们需要做下判断,判断是否是Comment类型,然后再进行操作,比如打印：
if type(bs.a.string) == element.Comment:
    print('注释内容是:', bs.a.string)  # 注释内容是: 注释

# 4.遍历文档树
# (1)直接子节点
# .contents
# tag 的 .content 属性可以将tag的子节点以列表的方式输出,结果的类型是列表,可以用索引获取数据
print(soup.head.contents)  # [<title>The Dormouse's story</title>]
print(soup.title.contents)  # ["The Dormouse's story"]
print(type(soup.title.contents))  # <class 'list'>
print(soup.title.contents[0])  # The Dormouse's story

# .children
# 它返回的不是一个 list,它是一个 list 生成器对象,我们可以通过遍历获取所有子节点.
head_list_iterator = soup.head.children
print(head_list_iterator)  # <list_iterator object at 0x0391A3D0>

# 遍历即可获取数据
for child in head_list_iterator:
    print(child)  # <title>The Dormouse's story</title>

# 获取body下的所有节点
for child in soup.body.children:
    print(child)

# (2)所有子孙节点
# .descendants
# .contents 和 .children 属性仅包含tag的直接子节点，.descendants 属性可以对所有tag的子孙节点进行递归循环，和 children类似，我们也需要遍历获取其中的内容。
print(soup.descendants)  # <generator object descendants at 0x040285D0>
# 运行结果可以发现，所有的节点都被打印出来了，先是最外层的<html>标签，其次从<head>标签一个个剥离，以此类推。
for item in soup.descendants:
    print(item)

# (3)节点内容
# 如果tag只有一个 NavigableString 类型子节点,那么这个tag可以使用 .string 得到子节点。如果一个tag仅有一个子节点,那么这个tag也可以使用 .string 方法,输出结果与当前唯一子节点的 .string 结果相同。
# 通俗点说就是：如果一个标签里面没有标签了，那么 .string 就会返回标签里面的内容。如果标签里面只有唯一的一个标签了，那么 .string 也会返回最里面的内容。例如
print(soup.head.string)  # The Dormouse's story
print(soup.title.string)  # The Dormouse's story
# 如果tag包含了多个子节点,tag就无法确定，string 方法应该调用哪个子节点的内容, .string 的输出结果是 None
print(soup.html.string)  # None

# (4)多个内容
# .strings
# 获取多个内容，不过需要遍历获取，比如下面的例子
for string in soup.strings:
    print(repr(string))  # repr() 返回带(双引号)的字符串

# .stripped_strings
# 输出的字符串中可能包含了很多空格或空行,使用 .stripped_strings 可以去除多余空白内容
for string in soup.stripped_strings:
    print(repr(string))

# (5)父节点
# .parent 属性
print(soup.p.parent.name)  # body

content = soup.head.title.string
print(content.parent.name)  # title

# (6)全部父节点
# .parents 属性
# 通过元素的 .parents 属性可以递归得到元素的所有父辈节点，例如
print(content.parents)  # <generator object parents at 0x031988D0>
for parent in content.parents:
    print(parent.name)
    # title
    # head
    # html
    # [document]

# (7)兄弟节点
# .next_sibling  .previous_sibling 属性
# 兄弟节点可以理解为和本节点处在同一级的节点，.next_sibling 属性获取了该节点的下一个兄弟节点，.previous_sibling 则与之相反，如果节点不存在，则返回 None
# 注意：实际文档中的tag的 .next_sibling 和 .previous_sibling 属性通常是字符串或空白，因为空白或者换行也可以被视作一个节点，所以得到的结果可能是空白或者换行
print('p的下一个兄弟节点:', soup.p.next_sibling)  # p的下一个兄弟节点:
# 没有上一个兄弟节点就返回None,如果上一个兄弟节点是空白,那就返回空
print('p的上一个兄弟节点:', soup.html.previous_sibling)  # p的上一个兄弟节点: None
print('p的下个兄弟节点的下个兄弟节点:', soup.p.next_sibling.next_sibling)

# (8)全部兄弟节点
# .next_siblings  .previous_siblings 属性
# 通过 .next_siblings 和 .previous_siblings 属性可以对当前节点的兄弟节点迭代输出
for sibling in soup.p.next_siblings:
    print(repr(sibling))

for sibling in soup.p.previous_siblings:
    print(repr(sibling))

# (9)前后节点
# .next_element  .previous_element 属性
# .next_element  .previous_element与 .next_sibling  .previous_sibling 不同，它并不是针对于兄弟节点，而是在所有节点，不分层次
print(soup.head.next_element)  # <title>The Dormouse's story</title>
print(soup.head.previous_element)  # 返回除<head></head>节点外的所有节点,即<head></head>的前后节点

# (10)所有前后节点
# .next_elements  .previous_elements 属性
# 通过 .next_elements 和 .previous_elements 的迭代器就可以向前或向后访问文档的解析内容,就好像文档正在被解析一样
# 先迭代上下节点,再迭代该节点中的内容,再迭代下一个节点,再迭代节点里的内容,以此类推
for element in soup.p.next_elements:
    print(element)

# 5.搜索文档树
# (1)find_all( name , attrs , recursive , text , **kwargs )
# find_all() 方法搜索当前tag的所有tag子节点,并判断是否符合过滤器的条件,返回列表

# <1>name 参数可以查找所有名字为 name 的tag,字符串对象会被自动忽略掉
# A.传入字符串
# 最简单的过滤器是字符串.在搜索方法中传入一个字符串参数,Beautiful Soup会查找与字符串完整匹配的内容,下面的例子用于查找文档中所有的<b>标签
print(soup.find_all('title'))  # [<title>The Dormouse's story</title>]
# B.传入正则表达式
# 如果传入正则表达式作为参数,Beautiful Soup会通过正则表达式的 match() 来匹配内容.下面例子中找出所有以b开头的标签,这表示<body>和<b>标签都应该被找到
for tag in soup.find_all(re.compile('^b')):
    print(tag.name)
    # body
    # b

# C.传列表
# 如果传入列表参数,Beautiful Soup会将与列表中任一元素匹配的内容返回.下面代码找到文档中所有<a>标签和<b>标签
print(soup.find_all(['a', 'b']))

# D.传True
# True 可以匹配任何值,下面代码查找到所有的tag,但是不会返回字符串节点
for tag in soup.find_all(True):
    print(tag.name)


# E.传方法
# 如果没有合适过滤器,那么还可以定义一个方法,方法只接受一个元素参数,如果这个方法返回 True 表示当前元素匹配并且被找到,如果不是则反回 False
# 下面方法校验了当前元素,如果包含 class 属性却不包含 id 属性,那么将返回 True:
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


# 将这个方法作为参数传入 find_all() 方法,将得到所有<p>标签:
print(soup.find_all(has_class_but_no_id))

# <2>keyword 参数
# 注意：如果一个指定名字的参数不是搜索内置的参数名,搜索时会把该参数当作指定名字tag的属性来搜索,比如包含一个名字为 id 的参数,Beautiful Soup会搜索每个tag的”id”属性
print(soup.find_all(id='link1'))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
print(type(soup.find_all(id='link1')[0]))  # <class 'bs4.element.Tag'>
print(soup.find_all(id='link1')[0].string)  # Elsie

# 如果传入 href 参数,Beautiful Soup会搜索每个tag的”href”属性
print(
    soup.find_all(href=re.compile('elsie')))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
print(type(soup.find_all(href=re.compile('elsie'))[0]))  # <class 'bs4.element.Tag'>
print(soup.find_all(href=re.compile('elsie'))[0].string)  # Elsie

# 使用多个指定名字的参数可以同时过滤tag的多个属性
print(soup.find_all(href=re.compile('elsie'),
                    id='link1'))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
print(soup.find_all(href=re.compile('elsie'), id='link2'))  # []

# 在这里我们想用 class 过滤，不过 class 是 python 的关键词，这怎么办？加个下划线就可以
print(soup.find_all('a', class_='sister'))

# 有些tag属性在搜索不能使用,比如HTML5中的 data-* 属性
data_soup = BeautifulSoup('<div data-foo="value">foo!</div>', 'lxml')
# data_soup.find_all(data-foo='value')  # SyntaxError: keyword can't be an expression

# 但是可以通过 find_all() 方法的 attrs 参数定义一个字典参数来搜索包含特殊属性的tag
tag = data_soup.find_all(attrs={'data-foo': 'value'})
print(tag[0])  # <div data-foo="value">foo!</div>

# <3>text参数
# 通过 text 参数可以搜索文档中的字符串内容.与 name 参数的可选值一样, text 参数接受 字符串 , 正则表达式 , 列表, True
print(soup.find_all(text='Elsie'))  # ['Elsie']
print(soup.find_all(text=['Elsie', 'Lacie', 'Tillie']))
print(soup.find_all(text=re.compile('Dormouse')))  # ["The Dormouse's story", "The Dormouse's story"]

# <4>limit 参数
# find_all() 方法返回全部的搜索结构,如果文档树很大那么搜索会很慢.如果我们不需要全部结果,可以使用 limit 参数限制返回结果的数量.效果与SQL中的limit关键字类似,当搜索到的结果数量达到 limit 的限制时,就停止搜索返回结果.
# 文档树中有3个tag符合搜索条件,但结果只返回了2个,因为我们限制了返回数量
print(soup.find_all('a', limit=2))

# <5>recursive 参数
# 调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点,如果只想搜索tag的直接子节点,可以使用参数 recursive=False
print(soup.find_all('title'))  # [<title>The Dormouse's story</title>]
print(soup.find_all('title', recursive=False))  # []

# <6>attrs 参数
print(soup.find_all('p', attrs={'class': "title"}))
print(soup.find_all('p', attrs={'class': "story"}))

# (2)find( name , attrs , recursive , text , **kwargs )
# 它与 find_all() 方法唯一的区别是 find_all() 方法的返回结果是值包含一个元素的列表,而 find() 方法直接返回结果(对象)
print(type(soup.find('title')))  # <class 'bs4.element.Tag'>
print(soup.find('title'))  # <title>The Dormouse's story</title>

# (3)find_parents()  find_parent()
# find_parents( name , attrs , recursive , string , **kwargs )
# find_parent( name , attrs , recursive , string , **kwargs )
# find_all() 和 find() 只搜索当前节点的所有子节点,孙子节点等.
# find_parents() 和 find_parent() 用来搜索当前节点的父辈节点,搜索方法与普通tag的搜索方法相同,搜索文档搜索文档包含的内容
a_string = soup.find(string='Lacie')
print(a_string)
print(a_string.find_parents('a'))  # [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
print(a_string.find_parent('p'))
print(a_string.find_parents('p', class_='story'))
print(a_string.find_parents('p', class_='title'))  # []

# (4)find_next_siblings()  find_next_sibling()
# find_next_siblings( name , attrs , recursive , string , **kwargs ) 方法返回所有符合条件的后面的兄弟节点
# find_next_sibling( name , attrs , recursive , string , **kwargs ) 只返回符合条件的后面的第一个tag节点
# 这2个方法通过 .next_siblings 属性对当 tag 的所有后面解析的兄弟 tag 节点进行迭代

first_link = soup.a
print(first_link)  # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
print(first_link.find_next_siblings('a'))
print(first_link.find_next_sibling('a'))  # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

# (5)find_previous_siblings()  find_previous_sibling()
# find_previous_siblings( name , attrs , recursive , string , **kwargs ) 方法返回所有符合条件的前面的兄弟节点
# find_previous_sibling( name , attrs , recursive , string , **kwargs ) 方法返回第一个符合条件的前面的兄弟节点
# 这2个方法通过 .previous_siblings 属性对当前 tag 的前面解析的兄弟 tag 节点进行迭代
last_link = soup.find('a', id='link3')
print(last_link)  # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
print(last_link.find_previous_siblings('a'))
print(last_link.find_previous_sibling('a'))  # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

# (6)find_all_next()  find_next()
# find_all_next( name , attrs , recursive , string , **kwargs )  方法返回所有符合条件的节点
# find_next( name , attrs , recursive , string , **kwargs )  方法返回第一个符合条件的节点
# 这2个方法通过 .next_elements 属性对当前 tag 的之后的 tag 和字符串进行迭代
first_link = soup.a
print(first_link)  # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
print(first_link.find_all_next(
    string=True))  # ['Elsie', ' and\n', 'Lacie', ' and\n', 'Tillie', 'and they lived at the bottom of a well', '\n']
print(first_link.find_next('a'))  # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

# (7)find_all_previous() 和 find_previous()
# find_all_previous( name , attrs , recursive , string , **kwargs )  方法返回所有符合条件的节点
# find_previous( name , attrs , recursive , string , **kwargs )  方法返回第一个符合条件的节点
# 这2个方法通过 .previous_elements 属性对当前节点前面的 tag 和字符串进行迭代
first_link = soup.a
print(type(first_link))  # <class 'bs4.element.Tag'>
print(first_link)  # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
print(first_link.find_all_previous('p'))
print(first_link.find_previous('title'))  # <title>The Dormouse's story</title>

# 以上（2）（3）（4）（5）（6）（7）方法参数用法与 find_all() 完全相同，原理均类似，在此不再赘述。


# 6.CSS选择器
# 这是是另一种与 find_all 方法有异曲同工之妙的查找方法
# 我们在写 CSS 时，标签名不加任何修饰，类名前加点，id名前加 #，在这里我们也可以利用类似的方法来筛选元素，用到的方法是 soup.select()，返回类型是 list
# (1)通过标签名查找
print(soup.select('title'))  # [<title>The Dormouse's story</title>]
print(soup.select('a'))
print(soup.select('b'))  # [<b>The Dormouse's story</b>]

# (2)通过类名查找
print(soup.select('.title'))  # [<p class="title"><b>The Dormouse's story</b></p>]
print(soup.select('.titles'))  # []
print(soup.select('title')[0].string)  # The Dormouse's story
print(soup.select('title')[0].contents)  # ["The Dormouse's story"]

# (3)通过id查找
print(soup.select('#link1'))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
print(soup.select('#link1')[0]['href'])  # http://example.com/elsie
print(soup.select('#link1')[0].text)  # Elsie
print(soup.select('#link1')[0].string)  # Elsie

# (4)组合查找
# 组合查找即和写 class 文件时，标签名与类名、id名进行的组合原理是一样的，例如查找 p 标签中，id 等于 link1的内容，二者需要用空格分开
print(soup.select('p #link1'))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
# 直接子标签查找 二者需要用">"和空格,或者只用空格分开
print(soup.select('head > title'))  # [<title>The Dormouse's story</title>]
print(soup.select('p a'))

# (5)属性查找
# 查找时还可以加入属性元素，属性需要用中括号括起来，注意属性和标签属于同一节点，所以中间不能加空格，否则会无法匹配到。
print(soup.select('a[class="sister"]'))
print(soup.select(
    'a[href="http://example.com/elsie"]'))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
# 同样，属性仍然可以与上述查找方式组合，不在同一节点的空格隔开，同一节点的不加空格
print(soup.select(
    'p a[href="http://example.com/elsie"]'))  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

# 以上的 select 方法返回的结果都是列表形式，可以遍历形式输出，然后用 get_text() 方法来获取它的内容。
print(soup.select('.title')[0].get_text())  # The Dormouse's story

