title: 建立过程
date: 2016-01-23 12:01:13
tags: [OJ]
---

由于在阿里云完成备案, 需要留一个页面显示备案信息.
于是 [blog](http://www.njoj.org) 留一个静态页. 放一些ACM算法上的分享, 也可能放一些OJ组的分享

网站用 [Hexo](http://hexo.io/) 搭建.
项目在 [GitHub](https://github.com/ShengRang/njoj-blog) 上托管.
并且使用 `GitHub WebHook` 自动更新.
<!-- more -->
### Hexo
Hexo 是一个快速、简洁且高效的博客框架。Hexo 使用 Markdown（或其他渲染引擎）解析文章，在几秒内，即可利用靓丽的主题生成静态网页。

##### 安装 Node.js
使用包管理器或者下载源码编译安装. 编译安装的时候记得升级编译器到支持C++11.

##### 使用 Npm
Node.js 已经自带npm. 但是由于 *种种原因* npm下载的时候容易抽风. 推荐使用 [淘宝镜像](http://npm.taobao.org/)

##### 安装 Hexo
```bash
npm install -g hexo-cli
```
初始化博客
```bash
hexo init
npm install
```

##### 主题
使用 [apollo](https://github.com/pinggod/hexo-theme-apollo)主题. 这个主题抄的 [vuejs.org](http://cn.vuejs.org) . 比较清新.

fork之后进行了一些定制. 比如添加了备案信息的footer. 这个主题的css用scss写的, 所以修改了css需要gulp重新构建.

##### 写作
```bash
hexo n [title] #创建一个新的post. 然后编辑对应的.md文件
```


### 使用WebHook
目标是部署之后可以由他人在 GitHub 上一起维护博客项目. 静态页面在服务器自动生成, 自动更新.

在GitHub的项目的Settings里设置WebHook. 并设置一个secret.

自己写了个简易的自动更新, 生成页面. (webhook.py)

### 部署
##### nginx
WebServer 为 nginx.
由于是静态页, 配置很好写. 对于WebHook, 用反代.
配置如下:
```
upstream tornado {
		server 127.0.0.1:8080;
}
server{
		listen 80;
		server_name www.njoj.org;
		index index.html;
		location /refresh {
				proxy_pass_header Server;
				proxy_set_header Host $http_host;
				proxy_redirect off;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Scheme $scheme;
				proxy_pass http://tornado;
		}
		root /web/njoj-blog/public;
		access_log /var/log/nginx_oj_blog_access.log;
		error_log /var/log/nginx_oj_blog_error.log;
}
```

##### supervisor
webhook.py 使用 `supervisor` 进行管理.
```bash
pip install supervisor  #安装supervisor
echo_supervisord_conf > /etc/supervisord.conf   #生成一份配置文件
```

在/etc/supervisord.conf 最后添加
```
[include]
files = /etc/supervisord.d/*.ini
```

编辑/etc/supervisord.d/webhook.ini
```
[program:njoj-blog-refresh]
directory=/web/njoj-blog
user=root
command=python /web/njoj-blog/webhook.py
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile = /var/log/supervisord/tornado_server.log
```

启动
```bash
sudo supervisord
```
