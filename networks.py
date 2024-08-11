import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st

def get_simple():
    nx_graph = nx.cycle_graph(3)
    nx_graph.nodes[0]['label'] = 'Agent 1'
    nx_graph.nodes[1]['label'] = 'Agent 2'
    nx_graph.nodes[2]['label'] = 'Agent 3'

    nt = Network("500px", "500px", notebook=True, heading='', cdn_resources='in_line')
    nt.from_nx(nx_graph)
    # physics=st.sidebar.checkbox('add physics interactivity?')
    # if physics:
    #     nt.show_buttons(filter_=['physics'])
    nt.show('simple.html')


def get_star():
    nx_graph = nx.path_graph(3)
    nx_graph.nodes[0]['label'] = 'Agent 1'
    nx_graph.nodes[1]['label'] = 'Agent 2'
    nx_graph.nodes[2]['label'] = 'Agent 3'
    # nx_graph.remove_edge(0, 2)

    nt = Network("500px", "500px", notebook=True, heading='', cdn_resources='in_line')
    nt.from_nx(nx_graph)
    # physics=st.sidebar.checkbox('add physics interactivity?')
    # if physics:
    #     nt.show_buttons(filter_=['physics'])
    nt.show('star.html')