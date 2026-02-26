chat_memory = []

def add_to_memory(role, text):
    chat_memory.append({"role": role, "content": text})

def get_memory():
    return chat_memory[-10:]  # last 10 messages