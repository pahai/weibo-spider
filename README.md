# weibo-spider
将uid替换成需要爬的博主的（其主页url在微博html版找到），再修改成自己的存储路径即可
支持长微博

19/7/28
  1.在爬取被封禁的账号时，requests请求中需添加cookie。
  2.每爬取30page（300条微博）左右会得到json返回值None，可以每隔1min再请求一次
  3.url用page构建依然有效。用since_id应该也是可行的，后一个since_id可以在当前xhr页面找到
