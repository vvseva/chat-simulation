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


def simulate_group_chat(chat_history, agents, client, num_turns=5, isprint = True):
    # Initialize the chat with a starting message
    current_message = "What is the best landing location?"
    chat_history.append(("System", current_message))

    for i in range(num_turns):
        for agent, system_content in agents.items():
            prompt = "\n".join([f"{role}: {content}" for role, content in chat_history])
            prompt += f"\n{agent}:"
            response = generate_response(prompt, system_content, client)
            chat_history.append((agent, response))
            isprint: (
                print(f"{agent}: {response}"))

    return chat_history


def reply_to_survey(
          chat_history,
          agents,
          client,
          current_message = 'Rate Life Scientist, Geology Scientist, Climate Scientist, and AI agent on a scale from 1 to 7, answering questions "How confident are you in each teammate`s ability to effectively complete tasks?" 1 being not confident at all and 7 being absolutely confident. REPLY ONLY IN THE FOLLOWING FORMAT: {"rankings":{"ranking":[{"your_role":"your role","teammate":"Life Scientist","value":"value from 1 to 7","explanation":"One sentance with an explanation of the value"},{"your_role":"your role","teammate":"Geology Scientist","value":"value from 1 to 7","explanation":"One sentance with an explanation of the value"},{"your_role":"your role","teammate":"Climate Scientist","value":"value from 1 to 7","explanation":"One sentance with an explanation of the value"},{"your_role":"your role","teammate":"AI agent","value":"value from 1 to 7","explanation":"One sentance with an explanation of the value"}]}}',
          isprint = True):
                                # agents = {
    #     "Life Scientist": "As a Life Scientist, your mission is to help select the best landing site for a 6-member international crew (3 US, 3 Russian) traveling 140 million miles from the Moon to Mars to establish the first human scientific outpost. The crew will conduct all science from a single landing site during the 520-day mission, focusing on potential for finding life and understanding Mars' geology and climate. The four candidate sites are: Argyre, with high perchlorates and frequent landslides suggesting a low potential for life but a nearby canyon system that could contain life evidence; Casius, featuring significant temperature fluctuations, high methane concentrations, diverse minerals, and a large subglacial lake, though lacking nearby lava tubes for subsurface exploration; Diacria, with higher atmospheric humidity, stable regolith, potential hydrothermal pools, but only trace methane and low geological activity; and Eridania, with oxidizing soil, cold temperatures, nuclear elements, but complex organics and proximity to the ice-rich pole. YOUR TASK IS TO REPLY TO A SURVEY QUESTION, BASED ON THE PREVIOUS CONVERSATION. Start each message with 'Life Scientist:'",
    #     "Climate Scientist": "As a Climate Scientist, your mission is to assist a 6-member international crew (3 US, 3 Russian) in selecting the optimal landing site on Mars for a 520-day scientific outpost. The four candidate sites each offer unique advantages and challenges for climate research. Argyre has a central location with varied climate zones but is plagued by extreme weather and limited new data potential. Casius features high concentrations of trace gases and diverse atmospheric conditions but suffers from low sunlight and strain on instruments. Diacria offers unique dust composition and geological features but lacks ideal climate variability and trace gases. Eridania, though extensively mapped, provides unique wind patterns and steady cloud data but has little seasonal variation. YOUR TASK IS TO REPLY TO A SURVEY QUESTION, BASED ON THE PREVIOUS CONVERSATION. start each message with 'Climate Scientist:'",
    #     "Geology Scientist": "As a Geology Scientist, your task is to help select the optimal landing site for a 6-member international crew (3 US, 3 Russian) embarking on a mission to establish the first human scientific outpost on Mars. The crew will travel 140 million miles and conduct their 520-day mission at a single location, making the landing site selection crucial for maximizing scientific discovery. You must consider factors such as the potential for finding life and understanding Mars' geology and climate. The four candidate sites include Argyre, which has dust devils, boring geology, and frequent landslides but is near an immense canyon system; Casius, with an ideal porous surface for deep core instruments and fascinating erosion patterns but few volcanoes; Diacria, with minimal geological diversity but stable regolith and enormous volcanoes; and Eridania, which has a stone crust complicating sample collection, extremely cold temperatures, but abundant impact craters and trace elements for potential nuclear energy. YOUR TASK IS TO REPLY TO A SURVEY QUESTION, BASED ON THE PREVIOUS CONVERSATION. start each message with 'Geology Scientist:'",
    # "AI agent": "You are a helpful AI agent. You task is to help you team to select the best landing location. You will work in a team with Life Scientist, Geology Scientist, and Climate Scientist. Keep your replies short. Start by introducing yourself and help your human team members. YOUR TASK IS TO REPLY TO A SURVEY QUESTION, BASED ON THE PREVIOUS CONVERSATION.  start each message with 'AI Agent:'"
    # }

    # system_content = agents[agent]
    # new_chat_history = chat_history
    # # Initialize the chat with a starting message
    # new_chat_history.append(("System", current_message))
    #
    # prompt = "\n".join([f"{role}: {content}" for role, content in chat_history])
    # prompt += f"\n{agent}:"
    # response = generate_response(prompt, system_content, chat_history, agent)
    # # chat_history.append((agent, response))

    responses = []
    for agent, system_content in agents.items():
        prompt = "\n".join([f"{role}: {content}" for role, content in chat_history])
        prompt += f"\n{agent}:"
        response = generate_response(prompt, system_content+current_message, client)
        responses.append((agent, response))
        isprint: (
            print(f"{agent}: {response}"))

    return responses
