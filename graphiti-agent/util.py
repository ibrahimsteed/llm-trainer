import re


# 该函数用于根据用户的名字和姓氏生成一个一致的用户ID。它通过将名字和姓氏连接起来，转换为小写，并移除所有非单词字符来实现。如果生成的ID为空，则返回默认用户ID "default_user"。
def generate_user_id(first_name, last_name):
    """从名字和姓氏生成一致的用户ID。"""
    user_id = re.sub(r"\W+", "", (first_name + last_name).lower())
    return user_id if user_id else "default_user"
