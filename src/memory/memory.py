class SimpleMemory:
    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self):
        return self.messages

    def get_context(self):
        return "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in self.messages]
        )