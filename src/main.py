import requests
import pandas as pd
import logging

def fetch_data(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'w') as f:
            f.write(response.text)
        logging.info("数据获取成功并保存到文件。")
    except requests.RequestException as e:
        logging.error(f"请求失败: {e}")
        return False
    return True

def load_data(file_path, col_names):
    try:
        data = pd.read_csv(file_path, header=None, names=col_names)
        logging.info("数据加载成功。")
        return data
    except Exception as e:
        logging.error(f"数据加载失败: {e}")
        return None

def clean_data(data):
    if data.isnull().values.any():
        data = data.dropna()
        logging.info("已处理缺失值。")
    else:
        logging.info("数据中没有缺失值。")
    return data

def explore_data(data):
    logging.info("数据基本信息：")
    logging.info(data.info())
    rows, columns = data.shape
    logging.info(f"数据集共有 {rows} 行，{columns} 列")
    logging.info("数据前几行信息：")
    logging.info(data.head().to_csv(sep='\t', na_rep='nan'))
    return data

def calculate_statistics(data):
    numerical_columns = data.select_dtypes(include=['number'])
    statistics = numerical_columns.describe()
    logging.info("数值列的基本统计信息：")
    logging.info(statistics)
    return statistics

def main():
    logging.basicConfig(level=logging.INFO)
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    file_path = 'iris.data'
    col_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

    if fetch_data(url, file_path):
        data = load_data(file_path, col_names)
        if data is not None:
            data = clean_data(data)
            data = explore_data(data)
            calculate_statistics(data)

if __name__ == "__main__":
    main()
