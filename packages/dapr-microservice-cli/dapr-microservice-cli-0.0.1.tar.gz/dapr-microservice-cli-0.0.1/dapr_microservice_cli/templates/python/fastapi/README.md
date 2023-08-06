# Microservice Name

## 初始化环境

### 安装python包

```shell
pip install dapr dapr-ext-fastapi
```

### 项目结构
- config 配置文件目录
  - dev.yaml 开发配置
  - prod.yaml 生产配置
- doc 文档目录，包括：http请求文档
- service 服务代码目录
  - main.py 服务app模块文件
  - deps.py 共享依赖模块文件
  - models.py 模型模块文件，可以将其升级为models目录，拆分代码为多个文件
  - routers.py 路由模块文件，可以将其升级为routers目录，拆分代码为多个文件
  - schemas.py 校检模块文件，同上
  - middlewares.py 中间件模块，同上
- tests 服务测试代码目录
- .gitignore git忽略文件设置文件
- Dockerfile dockerfile文件
- Makefile make运行命令
- README.md 说明文档
- requirements.txt python依赖包生成文件

## 设计要点


## 实现思路


## 接口设计


## 备注


## 参考

[FastAPI Project Structure Reference](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
