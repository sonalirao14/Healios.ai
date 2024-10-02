class Memory:
    def __init__(self):
        self.conversation_history = []

    def add_to_memory(self, user_question, response):
        self.conversation_history.append({
            "user_question": user_question,
            "response": response
        })

    def recall_from_memory(self, user_question):
        for conversation in self.conversation_history:
            if conversation["user_question"] == user_question:
                return conversation["response"]
        return None