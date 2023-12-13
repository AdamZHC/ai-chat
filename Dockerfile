# 基础镜像，python3.9
FROM python:3.8
# 镜像作者信息
MAINTAINER zhanghaocheng
WORKDIR /ai-chat
# 工作目录，这个目录对应于镜像内的工作目录，后面的所有涉及到路径的操作都可以
# 使用WORKDIR的相对路径来指定

COPY requirements.txt requirements.txt
# 拷贝requirements.txt 到 镜像中/app/requirements.txt

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 安装pip包
COPY . .
# 将当前文件中的目录复制到/app目录下
# 设置环境变量，让flask run 命令能够找到启动文件的位置
ENV FLASK_APP app

CMD ["flask","run","-h","0.0.0.0","-p","5000"]
# 执行启动命名 flask run -h 0.0.0.0 -p 5000 列表中的每个元素之间代表空格
