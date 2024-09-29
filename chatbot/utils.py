from llama_wrapper import get_completion

def handle_user_message(user_message):
    response = get_completion(user_message)
    return response