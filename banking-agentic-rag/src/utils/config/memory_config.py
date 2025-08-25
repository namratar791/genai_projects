from langchain.memory import ConversationBufferMemory

class MemoryConfig:
    _memory_instance = None

    @staticmethod
    def get_memory():
        if MemoryConfig._memory_instance is None:
            MemoryConfig._memory_instance = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        return MemoryConfig._memory_instance