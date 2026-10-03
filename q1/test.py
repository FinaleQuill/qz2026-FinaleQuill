import unittest
import os
from main import analyze_log

class TestAnalyzeLog(unittest.TestCase):
    current_dir = os.path.dirname(os.path.abspath(__file__))  #获取绝对路径的当前目录
    # 测试正常文件 app.jsonl
    def test_app(self):
        result = analyze_log(os.path.join(self.current_dir, "app.jsonl"))   #拼接目录
        # 验证总数
        self.assertEqual(result["total"], 5)
        # 验证 by_level
        self.assertEqual(result["by_level"], {'INFO': 3, 'ERROR': 2})
        # 验证 last_error
        self.assertEqual(result["last_error"], "超时")

    # 测试坏行文件 bad.jsonl
    def test_bad(self):
        result = analyze_log(os.path.join(self.current_dir, "bad.jsonl"))
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["by_level"], {'INFO': 1, 'ERROR': 1})
        self.assertEqual(result["last_error"], "失败")

    # 测试空文件 empty.jsonl
    def test_empty(self):
        result = analyze_log(os.path.join(self.current_dir, "empty.jsonl"))
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["by_level"], {})
        self.assertEqual(result["by_user"], {})
        self.assertIsNone(result["last_error"])

    # 测试文件不存在
    def test_not_exist(self):
        result = analyze_log(os.path.join(self.current_dir, "not_exist.jsonl"))
        self.assertEqual(result["total"], 0)
        self.assertIsNone(result["last_error"])

if __name__ == '__main__':
    unittest.main()