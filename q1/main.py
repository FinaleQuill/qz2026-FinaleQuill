import json
import os

def analyze_log(filepath: str) -> dict:
    #初始化返回值
    result = {
        "total": 0,
        "by_level": {},
        "by_user": {},
        "last_error": None
        }
    try:
        with open(filepath, "r",encoding="utf-8") as f:
            for line in f:
                line = line.strip()         #格式化

                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue                #剔除错误行
                result["total"] += 1

                # print(data)
                level = data["level"]   #level =info
                user = data["user"]     #user = zhangsan

                result["by_level"][level] = result["by_level"].get(level, 0) + 1
                result["by_user"][user] = result["by_user"].get(user, 0) + 1

                if level == "ERROR":
                    result["last_error"] = data["message"]

        return result
    except FileNotFoundError:
        return result

if __name__ == "__main__":
    print(analyze_log("app.jsonl"))


# result = analyze_log("not_exist.jsonl")
#示例1
# print(json.dumps(result, indent=4, ensure_ascii=False))
# print(result["total"])        # 5
# print(result["by_level"])     # {'INFO': 3, 'ERROR': 2}
# print(result["by_user"])      # {'张三': 2, '李四': 2, '王五': 1}
# print(result["last_error"])   # 超时

#示例2
#文件不存在
# result = analyze_log("not_exist.jsonl")
# print(result)
# {'total': 0, 'by_level': {}, 'by_user': {}, 'last_error': None}

#示例3
# 文件存在但内容为空
# result = analyze_log("bad.jsonl")
# print(result["total"])      # 2（跳过格式错误行）
# print(result["by_level"])    # {'INFO': 1, 'ERROR': 1}
# print(result["last_error"])  # 失败