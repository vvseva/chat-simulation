# from config import OPENAI_API_KEY

# from openai import OpenAI

# myclient = OpenAI(api_key=OPENAI_API_KEY)

# Function to generate a response from a GPT model
def generate_response(prompt, system_content, client):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def simulate_group_chat(chat_history, agents, client, num_turns=5):
    # Initialize the chat with a starting message
    current_message = "What is the best landing location?"
    chat_history.append(("System", current_message))

    for i in range(num_turns):
        for agent, system_content in agents.items():
            prompt = "\n".join([f"{role}: {content}" for role, content in chat_history])
            prompt += f"\n{agent}:"
            response = generate_response(prompt, system_content, client)
            chat_history.append((agent, response))
            print(f"{agent}: {response}")

    return chat_history