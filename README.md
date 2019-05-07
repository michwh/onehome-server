
vue+django+mysql实现移动端二手交易应用后端部分

# 相关仓库

- [onehome](https://github.com/michwh/onehome)：项目前端部分

- [onehomeServer](https://github.com/michwh/onehome-server)：项目后端部分

- [onehomeDoc](https://github.com/michwh/onehomeDoc)：项目的一些文档

# 技术栈

- django

- django-rest-framework

- channels

# 使用说明

当项目下载到本地以后，在onehomeServer文件夹下新建config_default.py文件。文件格式如下：

```python
configs = {
    'db_host': 'xxx', # 主机地址
    'db_name': 'xxx', # 数据库名称
    'db_user': 'xxx', # 数据库用户名
    'db_password': 'xxx', # 数据库密码
    'qiniu': {
        'AK': 'xxx', # 七牛云AK
        'SK': 'xxx', # 七牛云SK
        'bucket_name': 'xxx', # 七牛云存储空间名称
        'domain': 'xxx', # 图片下载地址，七牛给的测试域名或者自己绑定的域名，例如：http://qiniu.fanfei.site
    },
}
```

创建虚拟环境以后执行 `pip install -r requirements.txt` 安装项目依赖

执行 `python manage.py runserver` 启动项目

