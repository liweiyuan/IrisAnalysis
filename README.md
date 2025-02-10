# Iris Analysis

这是一个用于分析鸢尾花数据集的Python项目。

## 项目结构

- `main.py`: 主程序文件，包含数据分析的主要逻辑。
- `iris.data`: 鸢尾花数据集文件。

## 安装依赖

在项目根目录下运行以下命令以安装所需的Python依赖：

```bash
git clone ...
python -m venv venv
source venv/bin/activate # 激活虚拟环境
pip install -r requirements.txt
```

## 运行项目

在项目根目录下运行以下命令以启动数据分析：

```bash
python src/main.py
```

## 格式化项目
在项目根目录下运行以下命令以格式化代码：
```bash
black src/
```

## 鸢尾花数据集

鸢尾花数据集包含150条记录，每条记录包含以下四个特征：

- 萼片长度
- 萼片宽度
- 花瓣长度
- 花瓣宽度

数据集分为三类，每类50条记录，分别对应三种鸢尾花：Setosa、Versicolour和Virginica。

## 贡献

欢迎提交问题和贡献代码！请确保在提交之前阅读并遵守我们的贡献指南。

## 许可证

本项目采用MIT许可证，详情请参阅LICENSE文件。
