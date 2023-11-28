import os
import tiktoken
import time
import openai

max_retries = 3
retry_delay = 5

start_prompt=os.getenv("START_PROMPT")
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_token_number(messages,model="gpt-3.5-turbo-0613"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens


def reply_request(conversation):
    for _ in range(max_retries):
        try:
            completion = openai.ChatCompletion.create( 
                model="gpt-3.5-turbo",
                messages=conversation)
            return completion
        except openai.error.APIConnectionError as e:
            print(f"API connection error: {e}")
            time.sleep(retry_delay)
    print("Max retries reached. Unable to communicate with OpenAI.")



        

