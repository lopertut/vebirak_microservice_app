import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def get_chat_id(user1, user2):
    users = sorted([user1, user2])
    return f"chat:{users[0]}:{users[1]}"


def create_chat(user1_id: int, user2_id: int):
    stream_name = get_chat_id(user1_id, user2_id)

    try:
        r.xgroup_create(stream_name, "chat_group", id="0", mkstream=True)
        return "chat created"
    except Exception as e:
        return f"somthing went wrond: {e}"


def send_message(sender_id, receiver_id, text):
    stream_name = get_chat_id(sender_id, receiver_id)

    r.xadd(stream_name, {"sender": sender_id, "message": text})

    print("Message sent")


def read_messages(user1_id: int, user2_id: int, last_id="0"):
    stream_name = get_chat_id(user1_id, user2_id)
    messages = r.xread({stream_name: last_id}, block=5000, count=10)
    return messages


def is_online(user_id: int):
    return r.exists(f"user:{user_id}:online")


def set_online(user_id: int):
    r.set(f"user:{user_id}:online", 1)


def set_offline(user_id: int):
    r.delete(f"user:{user_id}:online")


r.close()
