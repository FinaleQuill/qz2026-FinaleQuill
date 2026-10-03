import unittest
import os
import json
from main import UserManager  # 确保 main.py 和 test.py 在同一个文件夹 (q2) 下


class TestUserManager(unittest.TestCase):

    def setUp(self):
        # 初始化 UserManager 实例和测试文件名
        self.um = UserManager()
        self.test_filename = "test_users_temp.json"

    def tearDown(self):
        # 清理测试文件，确保每次测试后删除临时文件
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_user(self):
        # 测试添加用户
        user1 = self.um.add_user("张三", 18)
        self.assertEqual(user1, {"id": 1, "name": "张三", "age": 18})

        user2 = self.um.add_user("李四", 20)
        self.assertEqual(user2, {"id": 2, "name": "李四", "age": 20})

    def test_get_user(self):
        # 测试查询用户
        self.um.add_user("张三", 18)

        # 查存在的
        user = self.um.get_user(1)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "张三")

        # 查不存在的
        missing_user = self.um.get_user(99)
        self.assertIsNone(missing_user)

    def test_update_age(self):
        # 测试修改年龄
        self.um.add_user("张三", 18)

        #修改存在用户
        result = self.um.update_age(1, 19)
        self.assertTrue(result)
        self.assertEqual(self.um.get_user(1)["age"], 19)

        #修改不存在用户
        fail_result = self.um.update_age(99, 20)
        self.assertFalse(fail_result)

    def test_remove_user(self):
        #测试删除用户：验证删除成功返回True，删除不存在返回False
        self.um.add_user("张三", 18)

        #删除存在用户
        result = self.um.remove_user(1)
        self.assertTrue(result)
        self.assertIsNone(self.um.get_user(1))

        #再次删除同一个用户
        fail_result = self.um.remove_user(1)
        self.assertFalse(fail_result)

    def test_list_users(self):
        # 测试列出所有用户：验证是否按添加顺序返回
        self.um.add_user("张三", 18)
        self.um.add_user("李四", 20)

        users = self.um.list_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]["name"], "张三")
        self.assertEqual(users[1]["name"], "李四")

    #JSON持久化与加载

    def test_save_and_load_json(self):
        # 测试保存和加载JSON
        # 1. 准备数据并保存
        self.um.add_user("张三", 18)
        self.um.add_user("李四", 20)
        self.um.remove_user(2)
        self.um.save_to_json(self.test_filename)

        # 2. 验证文件确实存在
        self.assertTrue(os.path.exists(self.test_filename))

        # 3. 创建新实例并加载
        um2 = UserManager()
        um2.load_from_json(self.test_filename)

        # 4. 验证加载的数据与保存前一致
        self.assertEqual(um2.list_users(), [{"id": 1, "name": "张三", "age": 18}])

        # 5. 测试id是否正确
        new_user = um2.add_user("王五", 25)
        self.assertEqual(new_user["id"], 2, "加载后新增用户的 ID 未正确接续！")

    def test_load_empty_json(self):
        # 测试加载空 JSON 文件时，ID 是否重置为 1#
        # 手动创建一个空的 JSON 列表文件
        with open(self.test_filename, 'w', encoding='utf-8') as f:
            json.dump([], f)

        um2 = UserManager()
        um2.load_from_json(self.test_filename)

        self.assertEqual(um2.list_users(), [])

        # 加载空文件后添加用户，ID 应该从 1 开始
        new_user = um2.add_user("新用户", 20)
        self.assertEqual(new_user["id"], 1, "加载空文件后，ID 未正确重置为 1！")


if __name__ == '__main__':
    unittest.main()