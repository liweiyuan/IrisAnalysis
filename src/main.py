import requests
import pandas as pd

# 定义数据集的URL
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'

# 通过requests获取数据
# requests.get()方法返回一个Response对象
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 将数据写入文件
    with open('iris.data', 'w') as f:
        f.write(response.text)

    # 读取数据
    # 使用pandas的read_csv()方法读取数据
    # 定义列名
    col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
    data = pd.read_csv('iris.data', header=None, names=col_names)

    # 数据的基本信息
    print("数据基本信息：")
    print(data.info())

    # 查看数据集行数和列数
    rows, columns = data.shape

    if rows > 0 and columns > 0:
        # 数据清洗：处理缺失值
        if data.isnull().values.any():
            data = data.dropna()  # 删除包含缺失值的行
            print("已处理缺失值。")
        else:
            print("数据中没有缺失值。")

        # 数据探索：查看数据集行数和列数
        rows, columns = data.shape
        print(f"数据集共有 {rows} 行，{columns} 列")

        # 查看数据集行数和列数
        print("数据前几行信息：")
        print(data.head().to_csv(sep='\t', na_rep='nan'))

        # 数据计算：计算数值列的基本统计信息
        numerical_columns = data.select_dtypes(include=['number'])
        statistics = numerical_columns.describe()
        print("数值列的基本统计信息：")
        print(statistics)
    else:
        print("数据集中没有数据。")

else:
    print(f"请求失败，状态码：{response.status_code}")
