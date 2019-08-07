# Get-All-Math-Activities-in-BeiJing
我就随便写两句吧

因为懒，五次三番错过隔壁和科院的报告、讲座。痛定思痛我决定写个爬虫，把这两个地方的学术报告信息都汇总起来，并且提醒我去参加。当当当，这就是GitHub上的这个东西了（尽管现在仅仅支持Bicmr）！鉴于我垃圾的编程水平，这个Project写的肯定很烂，没办法先忍着吧~

目前这个程序能够爬取Bicmr网站上的信息，并将尚未开始的报告、会议、讨论班的信息整理下来。如果用户输入了关键词，它还可以将符合关键词的会议等信息单独罗列出来。最重要的是，当出现新的会议信息的时候，它可以按照用户的设置，发送邮件进行提醒。

我的程序功能虽然少，但是卫星却不少！现阶段的卫星包括，添加对晨兴中心、大清数学中心网站的支持，添加日历提醒功能。。。（大型咕咕现场）

然后是几点对程序功能的说明：
密码、邮箱等信息写在configuration.txt文件里。注意，等号后没有空格！
需要检索的网页，写在PKUweb.txt里面。
需要提醒的关键词，写在KeyWords.txt里面

尚未开始的会议等，在Upcoming Activities in PKU.csv里看
触发了关键词的会议等，能在Interesting Academic Activities in PKU.csv里找到
新的会议会给你发邮件提醒


最后我使用了yuantailing的tunet包。这个项目的地址是https://github.com/yuantailing/tunet-python

感谢大佬！
