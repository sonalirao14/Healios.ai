from langchain_community.llms import Ollama
from llama_index.core.llms import ChatMessage
from memory import Memory

llm = Ollama(model="llama3", num_ctx=258)
memory = Memory()


def get_completion(user_question):
    prompt = '''
        Provide a clear and concise answer to the user's health-related question.
        Assume the user is a layperson with a basic understanding of health concepts,
        but may not be familiar with technical medical terminology. Respond in a
        formal and empathetic tone, using simple language and avoiding jargon.

        Specific Requirements:

        * Provide a direct and accurate answer to the user's question
        Keep the response concise and focused on the user's query
        Use simple language and avoid technical jargon
        Include any relevant context or background information that might be helpful
        for the user to understand the answer

        Tone and Style:

        Formal and informative, yet approachable and empathetic
        Use simple language and concise sentences
        Include transitional phrases to connect ideas and improve readability

        Examples:

        User: What is the cause of diabetes?
        Answer: Diabetes is a group of metabolic disorders characterized by high blood sugar levels...
        User: What is the treatment for breast cancer?
        Answer: The treatment for breast cancer depends on the type and stage of the cancer...
        User: What are the symptoms of a heart attack?
        Answer: The symptoms of a heart attack can include chest pain, shortness of breath, and fatigue...

        Previous Conversations:
        {previous_conversations}
    '''

    previous_conversations = ""
    for conversation in memory.conversation_history:
        previous_conversations += f"User: {conversation['user_question']}\nAnswer: {conversation['response']}\n\n"

    prompt = prompt.format(previous_conversations=previous_conversations)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_question},
    ]

    prompt += "\n\n" + user_question


    try:
        resp = llm.generate([prompt])
        response = resp.generations[0][0].text
        memory.add_to_memory(user_question, response)
        return response
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    prompt = 'What os diabetes I'
    print(get_completion(prompt))