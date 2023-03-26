class Chat:
    def __init__(self):
        self.conversation = []
        self.token_size = 0

    def add_message(self,message):
        message_text = message['content']
        tokens = nltk.word_tokenize(message_text)
        self.token_size += len(tokens)

        self.conversation.append(message)

    def clear_chat(self):
        self.conversation = [{"role": "system", "content": "You are a therapist and friend. Your pretend name in every conversation is Lana always, do not forget. Introduce yourself as Lana and respond briefly"}]
        self.token_size = 0
