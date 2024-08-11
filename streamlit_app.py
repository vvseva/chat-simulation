from openai import OpenAI
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pyvis.network import Network

from chat_agents import generate_response
from chat_agents import simulate_group_chat
from networks import get_simple
from networks import get_star
st.set_page_config(layout="wide")

option = st.selectbox(
    "Select network configuration",
    ("Complete", "Star", "Ring"),
)


# net.add_node(4, label="Agent 1")



if option == "Complete":
    get_simple()
    HtmlFile = open("simple.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=400)
    # net.add_edge(1, 2)
    # net.add_edge(2, 3)
    # net.add_edge(3, 1)
elif option == "Star":
    get_star()
    HtmlFile = open("star.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=400)
    # net.add_edge(1, 2)
    # net.add_edge(2, 3)
elif option == "Ring":
    print("start")
    # net.add_edge(1, 2)
    # net.add_edge(2, 3)

get_simple()

col1, col2, col3 = st.columns(3)

goal = st.text_area('Goal for agents:', 'Your mission is to help select the best landing site for a 6-member international crew (3 US, 3 Russian) traveling 140 million miles from the Moon to Mars to establish the first human scientific outpost. The crew will conduct all science from a single landing site during the 520-day mission. KEEP YOUR REPLIES SHORT LIKE AN ACTUAL HUMAN IN A GROUP CHAT.', key = "goal")
API_key = st.text_input("Enter you OPENAI api key")

with col1:
    agent_1_description = st.text_area('Your prompt 1:', "Your role is Life Scientist. Focus on potential for finding life and understanding Mars' geology and climate. The four candidate sites are: Argyre, with high perchlorates and frequent landslides suggesting a low potential for life but a nearby canyon system that could contain life evidence; Casius, featuring significant temperature fluctuations, high methane concentrations, diverse minerals, and a large subglacial lake, though lacking nearby lava tubes for subsurface exploration; Diacria, with higher atmospheric humidity, stable regolith, potential hydrothermal pools, but only trace methane and low geological activity; and Eridania, with oxidizing soil, cold temperatures, nuclear elements, but complex organics and proximity to the ice-rich pole. Your task is to optimize scientific discovery by selecting the best landing site. Start each message with 'Life Scientist': ", key = "agent_1_description")
    # st.write(agent_1_description)

with col2:
    agent_2_description = st.text_area('Your prompt 2:', "Your role is Climate Scientist. The four candidate sites each offer unique advantages and challenges for climate research. Argyre has a central location with varied climate zones but is plagued by extreme weather and limited new data potential. Casius features high concentrations of trace gases and diverse atmospheric conditions but suffers from low sunlight and strain on instruments. Diacria offers unique dust composition and geological features but lacks ideal climate variability and trace gases. Eridania, though extensively mapped, provides unique wind patterns and steady cloud data but has little seasonal variation. Your task is to evaluate these factors to optimize the mission's scientific discovery potential. Start each message with 'Climate Scientist':" , key = "agent_2_description")
    # st.write(agent_2_description)

with col3:
    agent_3_description = st.text_area('Your prompt 3:', "Your role is Geology Scientist. Maximizing the scientific discovery. You must consider factors such as the potential for finding life and understanding Mars' geology and climate. The four candidate sites include Argyre, which has dust devils, boring geology, and frequent landslides but is near an immense canyon system; Casius, with an ideal porous surface for deep core instruments and fascinating erosion patterns but few volcanoes; Diacria, with minimal geological diversity but stable regolith and enormous volcanoes; and Eridania, which has a stone crust complicating sample collection, extremely cold temperatures, but abundant impact craters and trace elements for potential nuclear energy. Start each message with 'Geology Scientist':" , key = "agent_3_description")
    # st.write(agent_3_description)

n_turns = st.slider("How many turns", min_value = 1, max_value= 5)
reset_btn = st.button("Reset", type="primary")
start_btn = st.button("Start")

my_agents = {
"Life Scientist": f' {agent_1_description}, {goal}',
"Climate Scientist": f'{agent_2_description}, {goal}',
"Geology Scientist": f'{agent_3_description}, {goal}'
}

# st.write(my_agents)
my_chat_history = []

if reset_btn:
    my_chat_history = []

if start_btn:
    myclient = OpenAI(api_key=API_key)

    my_chat_history = simulate_group_chat(
        num_turns = n_turns,
        chat_history = my_chat_history,
        agents = my_agents,
        client=myclient
    )
    df = pd.DataFrame(my_chat_history, columns=['Agent', 'Message'])
    st.dataframe(df, width = 2000)

