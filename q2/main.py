import json

class UserManager():
    def __init__(self):
        self.users = []
        self.user_id = 1

    def add_user(self, username, age):
        user={
            "id": self.user_id,
            "name": username,
            "age": age
        }
        self.users.append(user)
        self.user_id += 1
        return user

    def get_user(self, id):
        for user in self.users:
            if user["id"] == id:
                return user
        return None

    def update_age(self, id, age):
        for user in self.users:
            if user["id"] == id:
                user["age"] = age
                return True
        return False

    def remove_user(self, id):
        for i, user in enumerate(self.users):
            if user["id"] == id:
                del self.users[i]
                return True
        return False

    def list_users(self):
        return self.users

    def save_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.users, f,ensure_ascii=False)

    def load_from_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.users = json.load(f)

        # 重新计算 self.user_id
        if len(self.users) > 0:
        # 找出当前最大的 id
            max_id = max(user["id"] for user in self.users)
            self.user_id = max_id + 1
        else:
        # 如果文件里是空的，重置为 1
            self.user_id = 1

if __name__ == "__main__":
    um = UserManager()
    um.add_user("张三", 18)
    um.add_user("李四", 20)
    um.get_user(1)
    um.get_user(99)
    um.update_age(1, 19)
    um.remove_user(2)
    um.remove_user(2)
    um.list_users()
    um.save_to_json("users.json")
    um2 = UserManager()
    um2.load_from_json("users.json")
    um2.list_users()

