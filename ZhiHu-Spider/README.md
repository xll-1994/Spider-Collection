## 知乎爬虫系统
#### 主要功能
- [x] 采集单个问题的答案信息
- [ ] 采集单个问题的基本信息
- [ ] 采集单个问题的相关问题
- [ ] 采集单个问题的回答者信息
#### 支持的数据导出模式
- [x] mysql
- [x] mongo
- [x] xls
#### 支持的连接模式
- [x] 使用代理
- [x] 不使用代理
#### 配置导出模式
```angular2html
在setting.py中，将需要用到的导出模式设置为1，其余设置为0
# ---------- EXPORT INFO ---------- #
USE_MYSQL = 1
USE_MONGO = 0
USE_XLS = 0
# ---------- EXPORT INFO ---------- #
```
#### 下载
##### 本地端
点击 该链接 下载
##### 服务器端
```angular2html
将Spider-Collection中的全部项目clone下来，然后开始对应项目的配置。
git clone https://github.com/xll-1994/Spider-Collection.git
```
#### 配置
