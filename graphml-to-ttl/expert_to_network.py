import re
import networkx as nx
import os
from matplotlib import pyplot as plt
import json
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib.term import URIRef
from rdflib.graph import Graph
from rdflib.paths import ZeroOrMore
from typing import Iterable
from collections import deque

def determine_final_output(network,nodes,numeric_dict):
    final_output = re.search(r"wf:output _:(\w+) \.", network).group(1)
    for node in nodes:
        if final_output in node:
            final_output_tool_name=re.search(r"(\w+)-",node).group(1)
    keys = [key for key, value in numeric_dict.items() if final_output_tool_name in value]
    return keys[0]

def extract_nodes_and_connections(network):
    nodes = set()
    connections = []
    str1 = '_'
    str2 = '+'
    str3 = '-'
    pattern1 = r"\[(.*?)\]"
    pattern2 = r"\[ wf:applicationOf \[ a (.*?)\],"
    matches1 = re.findall(pattern1, network)
    matches2 = re.findall(pattern2, network)
    #print(matches2)
    #matches2 = [item for item in matches2 if ']' not in item]
    all_matches = []
    all_matches.extend(matches1)
    all_matches.extend(matches2)
    #print(all_matches)
    for match in all_matches:
        tool_match = re.search(r"wf:applicationOf tools:(\w+)", match)
        if not tool_match:
            tool_match = re.search(r'rdfs:label "(\w+)"', match)
        input_matches = re.findall(r"wf:input\w+ _:(\w+)", match)
        output_match = re.search(r"wf:output _:(\w+)", match)
        if tool_match and input_matches and output_match:
            tool_node = tool_match.group(1)
            #print(tool_node)
            input_nodes = input_matches
            output_node = output_match.group(1)
            # Create a new combined node
            combined_node = f"{tool_node}-{'-'.join(input_nodes)}+{output_node}"
            nodes.add(combined_node)
            # Create the connection
            # Loop through the nodes
            for node in nodes:
                for input1 in input_nodes:
                    input_node1 = str2+input1
                    if input_node1 in node:
                        input_node2 = str2 + input1 + str1
                        if input_node2 not in node:
                            if combined_node != node:
                                connections.append((combined_node, node))
            for node in nodes:
                output_node1 = str3 + output_node + str3
                output_node2= str3 + output_node+str2
                if output_node1 in node or output_node2 in node:
                    #output_node2 = str3 + output_node + str1
                    #if output_node2 not in node:
                    if combined_node != node:
                        connections.append((combined_node, node))
    return nodes, connections

CCD = Namespace("http://geographicknowledge.de/vocab/CoreConceptData.rdf#")
ccd = Graph()
ccd.parse(CCD)
dimensions = [CCD.CoreConceptQ, CCD.LayerA, CCD.NominalA]
rdf_str="http://geographicknowledge.de/vocab/CoreConceptData.rdf#"
def complete_dict(uris: Iterable[URIRef]) -> dict[URIRef, set[URIRef]]:
    return {dim: set(uri for uri in uris if (uri, RDFS.subClassOf * ZeroOrMore, dim) in ccd) or {dim}for dim in dimensions}

def complete_set(uris: Iterable[URIRef]) -> set[URIRef]:
    return set.union(*complete_dict(uris).values())

def extract_dimensions(str_connect):
    if "CoreConceptQ" in str_connect:
        pattern=r"rdf#(\w+)'\)}$"
    if "LayerA" in str_connect:
        pattern=r"rdf#(\w+)'\)}$"
    if "NominalA" in str_connect:
        pattern=r"rdf#(\w+)'\)}$"
    matches = re.findall(pattern, str_connect)
    return matches[0]

def rdf_convert2list2(ccd_matches):
    rdf_str1=rdf_str+ccd_matches[0]
    rdf_str1=URIRef(rdf_str1)
    rdf_str2 = rdf_str + ccd_matches[1]
    rdf_str2 = URIRef(rdf_str2)
    list_rdf=[rdf_str1,rdf_str2]
    iter_dict = complete_dict(list_rdf)
    list_complete = []
    for key, value in iter_dict.items():
        str_connect = str(key) + str(value)
        list_complete.append(extract_dimensions(str_connect))
    return list_complete

def rdf_convert2list3(ccd_matches3):
    rdf_str1=rdf_str+ccd_matches3[0]
    rdf_str1=URIRef(rdf_str1)
    rdf_str2 = rdf_str + ccd_matches3[1]
    rdf_str2 = URIRef(rdf_str2)
    rdf_str3 = rdf_str + ccd_matches3[2]
    rdf_str3 = URIRef(rdf_str3)
    list_rdf=[rdf_str1,rdf_str2,rdf_str3]
    #print('list_,',list_rdf)
    iter_dict = complete_dict(list_rdf)
    #print(iter_dict)
    list_complete = []
    for key, value in iter_dict.items():
        str_connect = str(key) + str(value)
        list_complete.append(extract_dimensions(str_connect))
    return list_complete

def extract_ccd(network):
    rdf_str = "http://geographicknowledge.de/vocab/CoreConceptData.rdf#"
    data_names = []
    combined_ccds = []

    pattern = r"_:(\w+\s+.*?)\s\."
    matches = re.findall(pattern, network)
    #print('extract',matches)
    for match in matches:
        data_name_match = re.search(r"(.*?)\sa\sccd", match)
        ccd_matches = re.findall(r"ccd:(\w+)", match)
        #output_match = re.search(r"wf:output _:(\w+)", match)
        if len(ccd_matches)==2:
            ccd_matches=rdf_convert2list2(ccd_matches)
        if len(ccd_matches)==3:
            ccd_matches=rdf_convert2list3(ccd_matches)
        if data_name_match and ccd_matches:
            data_name_match_group=data_name_match.group(1)
            data_names.append(data_name_match_group)
            combined_ccd=f"{'_'.join(ccd_matches)}"
            combined_ccds.append(combined_ccd)
    return combined_ccds,data_names
def replace_data_type(node,combined_ccds,data_names):
    combined_type = ''
    tool_name = re.search(r"(\w+)-", node).group(1)
    input_names = re.findall(r'-(\w+)', node)
    output_name = re.search(r"\+(\w+)", node).group(1)
    if tool_name and input_names and output_name:
        combined_type = f"{tool_name}"
        for ccd, data_name in zip(combined_ccds, data_names):
            for input_name in input_names:
                if input_name==data_name:
                    input_type=f"-{ccd}"
                    combined_type = combined_type+input_type
        #if combined_type=='':
        #    combined_type = f"{tool_name}"
        for ccd_2, data_name_2 in zip(combined_ccds,data_names):
            if output_name==data_name_2:
                output_type=f"+{ccd_2}"
                combined_type=combined_type+output_type
    return(combined_type)
'''
file_path_1 = '../data_source/ttl_new/wfaccess.ttl'
file_path_2='../data_source/ttl_new/wfcrime_exposure.ttl'
# 打开文件进行读取
with open(file_path_1, 'r', encoding='utf-8') as file:
    # 读取整个文件内容
    content_1 = file.read()
with open(file_path_2, 'r', encoding='utf-8') as file:
    # 读取整个文件内容
    content_2 = file.read()
'''
def convert_nested_list(nested_list, dictionary):
    converted_list = [[dictionary.get(item) for item in sublist] for sublist in nested_list]
    return converted_list
def assign_numeric_keys(node_list,nested_list,dictionary):
    numeric_dict = {i+1: value for i, (_, value) in enumerate(dictionary.items())}
    convert_dict = {key: i+1 for i, (key, _) in enumerate(dictionary.items())}
    converted_nested_list = convert_nested_list(nested_list, convert_dict)
    converted_node_list=[convert_dict.get(item) for item in node_list]
    return numeric_dict,converted_nested_list,converted_node_list
def change_diagram_order(labels,dict,nested_list):
    new_numeric_dict = {}
    i=0
    for sub in labels:
        i=i+1
        for key,value in dict.items():
            if sub==key:
                new_numeric_dict.update({i:value})
    convert_dict={label:j+1 for j,label in enumerate(labels)}
    converted_nested_list=convert_nested_list(nested_list,convert_dict)
    #dict_test.update({i+1:value for i,(key,value) in enumerate(dict.items()) if sub==key})
    return converted_nested_list,new_numeric_dict
#The order of nodes in the graph is determined by a breadth traversal starting from the final output.
class Node:
    def __init__(self, label, next=None):
        self.label = label
        self.next = next

def extract_labels(connections, start):
    if not connections or not start:
        return []

    labels = []
    queue = deque([start])
    visited = set()
    while queue:
        node = queue.popleft()
        labels.append(node.label)
        visited.add(node.label)
        for connection in connections:
            if connection[0] == node.label and connection[1] not in visited:
                next_node = Node(connection[1])
                node.next = next_node
                queue.append(next_node)
                visited.add(connection[1])
            if connection[1] == node.label and connection[0] not in visited:
                next_node = Node(connection[0])
                node.next = next_node
                queue.append(next_node)
                visited.add(connection[1])
    return labels

# read the file
current_dir = os.getcwd()
input_folder = os.path.join(current_dir, "../data_source/ttl_new/")
output_folder = os.path.join(current_dir, "../data_source/json_file/")
i=0

for file in os.listdir(input_folder):
    i=i+1
    print(i)
    if file.endswith('.ttl'):
        file_name=os.path.join(input_folder,file)
        with open(file_name,'r',encoding='utf-8') as file:
            content=file.read()
        content=content.replace('\n','')
        nodes,connections=extract_nodes_and_connections(content)
        combined_ccds,data_names=extract_ccd(content)
        dict_wf = {value: replace_data_type(value, combined_ccds, data_names) for value in nodes}
        #print(dict_wf)
        numeric_dict,converted_nested_list,converted_node_list=assign_numeric_keys(nodes,connections, dict_wf)
        # Build a chain table to determine the order of the graph starting with the final output
        final_tool = determine_final_output(content, nodes, numeric_dict)
        start_node = Node(final_tool)
        labels = extract_labels(converted_nested_list, start_node)
        converted_nested_list, numeric_dict_new = change_diagram_order(labels, numeric_dict, converted_nested_list)
        # create JSON data
        data = {
            "edges": converted_nested_list,
            "features": numeric_dict_new
        }

        # generate JSON file
        filename = f"{i}.json"  # set the name of file
        json_file_name = os.path.join(output_folder, filename)
        with open(json_file_name, "w") as file:
            json.dump(data, file)

'''print("Connections:", connections)
for connection in connections:
    print(f"{connection[0]} -> {connection[1]}")'''




'''node_type = set()
for node in nodes:
    combined_type=replace_data_type(node,combined_ccds,data_names)
    #print('combined_type:',type(combined_type))
    node_type.add(combined_type)
connection_type=[]
for connection in connections:
    #connection[0]=replace_data_type(connection[0],combined_ccds,data_names)
    #connection[1]=replace_data_type(connection[1],combined_ccds,data_names)
    connection_type.append((replace_data_type(connection[0],combined_ccds,data_names),replace_data_type(connection[1],combined_ccds,data_names)))

print("new Nodes:")
for node in node_type:
    print(node)

print("new Connections:")
for connection in connection_type:
    print(f"{connection[0]} -> {connection[1]}")'''
file_path_1 = '../data_source/ttl_new/wfwaste_odour.ttl'
with open(file_path_1, 'r', encoding='utf-8') as file:
    # 读取整个文件内容
    content_1 = file.read()
content_1 = content_1.replace('\n', '')
print(content_1)
nodes_1, connections_1 = extract_nodes_and_connections(content_1)
#print("Connections:", connections)
for connection in connections_1:
    print(f"{connection[0]} -> {connection[1]}")
combined_ccds_1, data_names_1 = extract_ccd(content_1)
dict_wf_1 = {value: replace_data_type(value, combined_ccds_1, data_names_1) for value in nodes_1}
print('dict',dict_wf_1)
numeric_dict,converted_nested_list,converted_node_list=assign_numeric_keys(nodes_1,connections_1, dict_wf_1)
# Build a chain table to determine the order of the graph starting with the final output
final_tool=determine_final_output(content_1,nodes_1,numeric_dict)
start_node = Node(final_tool)
labels = extract_labels(converted_nested_list, start_node)
print(numeric_dict)

converted_nested_list_new,numeric_dict_new=change_diagram_order(labels,numeric_dict,converted_nested_list)
print('final:',final_tool)
print(labels)
print(converted_nested_list_new)
print(numeric_dict_new)
# Create a directed graph
graph = nx.Graph()

# Add nodes to the graph
#graph.add_nodes_from(converted_node_list)

# Add edges to the graph
graph.add_edges_from(converted_nested_list)

# Draw the graph
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, node_size=500, font_size=8)
plt.show()
