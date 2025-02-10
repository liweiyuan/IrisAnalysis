import sys
import os
# 获取当前测试文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 计算 src 目录的路径
src_dir = os.path.join(current_dir, '..', 'src')
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

    @patch('requests.get')
    def test_fetch_data_success(self, mock_get):
        # 模拟请求成功
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = 'test data'
        mock_get.return_value = mock_response

        url = 'test_url'
        file_path = 'test_file'
        result = fetch_data(url, file_path)

        self.assertEqual(result, True)
        mock_get.assert_called_once_with(url)
        self.assertIn("数据获取成功并保存到文件。", self.log_capture.getvalue())

    @patch('requests.get')
    def test_fetch_data_failure(self, mock_get):
        # 模拟请求失败
        mock_get.side_effect = requests.RequestException("Test error")

        url = 'test_url'
        file_path = 'test_file'
        result = fetch_data(url, file_path)

        self.assertEqual(result, False)
        mock_get.assert_called_once_with(url)
        self.assertIn("请求失败: Test error", self.log_capture.getvalue())

    @patch('pandas.read_csv')
    def test_load_data_success(self, mock_read_csv):
        # 模拟数据加载成功
        mock_data = MagicMock()
        mock_read_csv.return_value = mock_data

        file_path = 'test_file'
        col_names = ['col1', 'col2']
        result = load_data(file_path, col_names)

        self.assertEqual(result, mock_data)
        mock_read_csv.assert_called_once_with(file_path, header=None, names=col_names)
        self.assertIn("数据加载成功。", self.log_capture.getvalue())

    @patch('pandas.read_csv')
    def test_load_data_failure(self, mock_read_csv):
        # 模拟数据加载失败
        mock_read_csv.side_effect = Exception("Test error")

        file_path = 'test_file'
        col_names = ['col1', 'col2']
        result = load_data(file_path, col_names)

        self.assertEqual(result, None)
        mock_read_csv.assert_called_once_with(file_path, header=None, names=col_names)
        self.assertIn("数据加载失败: Test error", self.log_capture.getvalue())

    def test_clean_data_with_missing_values(self):
        # 模拟包含缺失值的数据
        data = pd.DataFrame({'col1': [1, None, 3]})
        result = clean_data(data)

        self.assertEqual(result.isnull().values.any(), False)
        self.assertIn("已处理缺失值。", self.log_capture.getvalue())

    def test_clean_data_without_missing_values(self):
        # 模拟不包含缺失值的数据
        data = pd.DataFrame({'col1': [1, 2, 3]})
        result = clean_data(data)

        self.assertEqual(result.isnull().values.any(), False)
        self.assertIn("数据中没有缺失值。", self.log_capture.getvalue())

    @patch('builtins.print')
    def test_explore_data(self, mock_print):
        # 模拟数据
        data = pd.DataFrame({'col1': [1, 2, 3]})
        result = explore_data(data)

        self.assertEqual(result.equals(data), True)
        self.assertIn("数据基本信息：", self.log_capture.getvalue())
        self.assertIn("数据集共有 3 行，1 列", self.log_capture.getvalue())
        self.assertIn("数据前几行信息：", self.log_capture.getvalue())

    def test_calculate_statistics(self):
        # 模拟数据
        data = pd.DataFrame({'col1': [1, 2, 3]})
        result = calculate_statistics(data)

        self.assertEqual(isinstance(result, pd.DataFrame), True)
        self.assertIn("数值列的基本统计信息：", self.log_capture.getvalue())


if __name__ == '__main__':
    unittest.main()