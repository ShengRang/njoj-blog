title: 发布文章流程
date: 2016-01-29 16:53:01
tags:
---
本文介绍从写作到发布的流程.
<!-- more -->
### 准备工作
0. 安装 `git`
>推荐使用包管理器安装

1. 安装 `NodeJs` & `Npm`
>使用包管理器或者源码安装. 参见[建站过程](http://www.njoj.org/2016/01/23/build-site/)

2. 安装 `Hexo`
```bash
npm install -g hexo-cli
```


### 安装
1. 克隆项目到本地
```bash
git clone git@github.com:NJUST-FishTeam/njoj-blog.git
```

2. 安装依赖的包和主题
```bash
cd njoj-blog
npm install #推荐用cnpm
git clone https://github.com/ShengRang/hexo-theme-apollo themes/apollo
```

3. 本地查看博客
```bash
#确保在项目根目录下
hexo s #hexo会根据 source/ 下的文章生成站点, 并提供本地web访问
#或者
hexo g #根据 source/ 下文章在 public/ 生成静态页.
# 通过python -m SimpleHTTPServer 或者其他方式查看页面效果.
```

### 写作流程
0. 创建你的分支
```bash
git checkout -b [你的分支名]
```

1. 拉取更新
```bash
git pull
```

2. 新建文章
```bash
hexo n [文章的文件名(title)]
# 命令行会输出你的新文章所在地址
```

3. 写作
> 根据前面得到的文件地址, 编辑你的文章. 直到满意

4. 推送
```bash
git add .
git commit #简要说明提交
git push origin [你的分支名]
```

5. 提交Pull Request
> 在项目的 [GitHub页面](https://github.com/NJUST-FishTeam/njoj-blog) 提交 Pull Request.

6. 审核
> 他人审核通过后, 网站会自动同步到最新的master分支.
