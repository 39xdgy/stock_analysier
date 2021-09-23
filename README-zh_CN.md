# 股票自动交易系统

[English](./README.md) | 简体中文 | [日本語(まだ完成しておりません)](./README-JP.md)

这个repo是一个使用股票指数来选股，以及使用webull的api去进行自动交易的脚本

## 安装

直接clone这个repo就可以使用

```bash
git clone https://github.com/39xdgy/stock_analysier.git
cd stock_analysier
pip install -r requirement.txt
```

## 如何使用

首先要在这个repo里面创造一个文件夹叫做Data用来储存所有文件以及数据。然后在里面创建一个json文件叫做webull_credentials.json。具体储存什么内容请查看helps里面的连接

当你把上述内容全部完成之后，可以直接进入Run文件夹然后运行self_main.py来使用我为了自己所开发的指标/股票。

### TODO
* 使用trade class来记录所有交易
* 开发一个用户界面/用户输入系统来交易股票
* 代码中增加注释

### 帮助

* https://github.com/pydata/pandas-datareader/issues/170

* 由于webull的api是由[tedchou12](https://github.com/tedchou12)个人开发，请仔细阅读下面这些链接。！！！你一定要阅读下面的链接才能够成功登陆webull！！！
    * https://github.com/tedchou12/webull/wiki/Workaround-for-Login

    * https://github.com/tedchou12/webull/issues/260

### 其他

* 这是个个人开发的小程序，其中有很多需要修改并且改进的地方。欢迎各位大佬可以在issue里面提出各种建议以及问题（求不要骂得太狠wwwww，我是新手wwww）。最后感谢各位赏脸能够看到或者使用这个repo，祝安好～