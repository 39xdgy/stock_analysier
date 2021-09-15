# stock_analysier

English | [简体中文](./README-zh_CN.md)

This is a application that would screen the stock and send message/auto buy/sell stocks by using an webull account. 

## Installation 

```bash
pip install -r requirement.txt
```
Very old school lol

## How to use it

You have to create a "Data" folder to host all your data. Inside that folder, you will have to have the file "webull_credentials.json" to host all your data for webull login. About the detail of that file, please check the link in the help section. 

After you create the folder with the file inside. just go to the "Run" folder and run the file "self_main.py" for the auto trading that created for myself.

### TODO
* Add trade record into the user (finished code, need testing)
* Add Japanese readme
* make it more user interactive with all the rules
* add comments in my code(Sorry I will try my best to make it better)


### Helps

Some nice tips that you might run into

* https://github.com/pydata/pandas-datareader/issues/170

* Since the webull api is not offical, developed by [tedchou12](https://github.com/tedchou12), please take a good look on how to login/use the api. Here are some good links for that. YOU HAVE TO READ THROUGH THIS TO BE ABLE TO LOGIN TO WEBULL!
    * https://github.com/tedchou12/webull/wiki/Workaround-for-Login

    * https://github.com/tedchou12/webull/issues/260

### notes

* I am working on this by myself. I know this still looks broken lol. I would love to accept all comments + questions on this repo in issue. Thank you so much for checking this out and hope you would have a nice day :)