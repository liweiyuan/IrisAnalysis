import sys
import os

# 获取当前测试文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 计算 src 目录的路径
src_dir = os.path.join(current_dir, "..", "src")
# 将 src 目录添加到模块搜索路径中
sys.path.insert(0, src_dir)

import unittest
from unittest.mock import patch, MagicMock
import requests
import pandas as pd
import logging
import io

# 修改导入语句，从 main.py 中导入要测试的函数
from main import fetch_data, load_data, clean_data, explore_data, calculate_statistics


class TestIrisDataProcessing(unittest.TestCase):

    def setUp(self):
        # 配置日志记录到缓冲区，方便检查日志信息
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.log_capture = io.StringIO()
        ch = logging.StreamHandler(self.log_capture)
        self.logger.addHandler(ch)

    def tearDown(self):
        # 移除日志处理程序
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

    @patch("requests.get")
    def test_fetch_data_success(self, mock_get):
        """
        测试 fetch_data 函数在请求成功时的行为。

        此测试用例模拟了请求成功的情况，通过设置 mock_get 的返回值来模拟请求响应。
        然后调用 fetch_data 函数，并验证其返回值、调用参数和日志信息。

        参数:
        mock_get (MagicMock): 用于模拟 requests.get 函数的 MagicMock 对象。
        """
        # 模拟请求成功
        mock_response = MagicMock()
        # 模拟请求响应不抛出异常
        mock_response.raise_for_status.return_value = None
        # 模拟请求响应的文本内容
        mock_response.text = "test data"
        # 设置 mock_get 的返回值为模拟的响应对象
        mock_get.return_value = mock_response

        # 定义测试用的 URL 和文件路径
        url = "test_url"
        file_path = "test_file"
        # 调用 fetch_data 函数并获取返回结果
        result = fetch_data(url, file_path)

        # 断言 fetch_data 函数的返回值为 True，表示请求成功
        self.assertEqual(result, True)
        # 断言 mock_get 函数被调用了一次，并且调用参数与预期一致
        mock_get.assert_called_once_with(url)
        # 断言日志中包含数据获取成功并保存到文件的信息
        self.assertIn("数据获取成功并保存到文件。", self.log_capture.getvalue())

        # 删除 test_file 文件，首先检查文件是否存在
        if os.path.exists(file_path):
            os.remove(file_path)

    @patch("requests.get")
    def test_fetch_data_failure(self, mock_get):
        # 模拟请求失败
        mock_get.side_effect = requests.RequestException("Test error")

        url = "test_url"
        file_path = "test_file"
        result = fetch_data(url, file_path)

        self.assertEqual(result, False)
        mock_get.assert_called_once_with(url)
        self.assertIn("请求失败: Test error", self.log_capture.getvalue())
        # 删除 test_file文件,首先文件存在
        if os.path.exists(file_path):
            os.remove(file_path)

    @patch("pandas.read_csv")
    def test_load_data_success(self, mock_read_csv):
        # 模拟数据加载成功
        mock_data = MagicMock()
        mock_read_csv.return_value = mock_data

        file_path = "test_file"
        col_names = ["col1", "col2"]
        result = load_data(file_path, col_names)

        self.assertEqual(result, mock_data)
        mock_read_csv.assert_called_once_with(file_path, header=None, names=col_names)
        self.assertIn("数据加载成功。", self.log_capture.getvalue())

        # 删除 test_file文件,首先文件存在
        if os.path.exists(file_path):
            os.remove(file_path)

    @patch("pandas.read_csv")
    def test_load_data_failure(self, mock_read_csv):
        """
        测试 load_data 函数在数据加载失败时的行为。

        此测试用例模拟了数据加载失败的情况，通过设置 mock_read_csv 的 side_effect 抛出异常。
        然后调用 load_data 函数，并验证其返回值、调用参数和日志信息。

        参数:
        mock_read_csv (MagicMock): 用于模拟 pandas.read_csv 函数的 MagicMock 对象。
        """
        # 模拟数据加载失败，当调用 mock_read_csv 时抛出异常
        mock_read_csv.side_effect = Exception("Test error")

        # 定义测试用的文件路径和列名
        file_path = "test_file"
        col_names = ["col1", "col2"]
        # 调用 load_data 函数并获取返回结果
        result = load_data(file_path, col_names)

        # 断言 load_data 函数的返回值为 None
        self.assertEqual(result, None)
        # 断言 mock_read_csv 函数被调用了一次，并且调用参数与预期一致
        mock_read_csv.assert_called_once_with(file_path, header=None, names=col_names)
        # 断言日志中包含数据加载失败的信息
        self.assertIn("数据加载失败: Test error", self.log_capture.getvalue())

        # 删除 test_file 文件，首先检查文件是否存在
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_clean_data_with_missing_values(self):
        # 模拟包含缺失值的数据
        data = pd.DataFrame({"col1": [1, None, 3]})
        result = clean_data(data)

        self.assertEqual(result.isnull().values.any(), False)
        self.assertIn("已处理缺失值。", self.log_capture.getvalue())

    def test_clean_data_without_missing_values(self):
        # 模拟不包含缺失值的数据
        data = pd.DataFrame({"col1": [1, 2, 3]})
        result = clean_data(data)

        self.assertEqual(result.isnull().values.any(), False)
        self.assertIn("数据中没有缺失值。", self.log_capture.getvalue())

    @patch("builtins.print")
    def test_explore_data(self, mock_print):
        # 模拟数据
        data = pd.DataFrame({"col1": [1, 2, 3]})
        result = explore_data(data)

        self.assertEqual(result.equals(data), True)
        self.assertIn("数据基本信息：", self.log_capture.getvalue())
        self.assertIn("数据集共有 3 行，1 列", self.log_capture.getvalue())
        self.assertIn("数据前几行信息：", self.log_capture.getvalue())

    def test_calculate_statistics(self):
        # 模拟数据
        data = pd.DataFrame({"col1": [1, 2, 3]})
        result = calculate_statistics(data)

        self.assertEqual(isinstance(result, pd.DataFrame), True)
        self.assertIn("数值列的基本统计信息：", self.log_capture.getvalue())


if __name__ == "__main__":
    unittest.main()
