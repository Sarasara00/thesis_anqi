import re
import networkx as nx
import os
from matplotlib import pyplot as plt
import json
#extract all types and toolname
def extract_all_types(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    if tool_match:
        new_feature=f"{tool_match}-"
    list_input_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0],input_type[1])
        list_input_sort=list_input_sort+input_type
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        new_feature=new_feature+f"+{'_'.join(sorted(output_type))}"
    return new_feature
#extract only coreconcept and toolname
def extract_only_coreconcept(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    if tool_match:
        new_feature=f"{tool_match}-"
    list_input_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[0])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        new_feature=new_feature+f"+{output_type[0]}"
    return new_feature
#extract only layer and toolname
def extract_only_layer(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    if tool_match:
        new_feature=f"{tool_match}-"
    list_input_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[1])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[1])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        new_feature=new_feature+f"+{output_type[1]}"
    return new_feature
#extract only measurement and toolname
def extract_only_measurement(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    if tool_match:
        new_feature=f"{tool_match}-"
    list_input_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        list_input_sort.append(input_type[2])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        new_feature=new_feature+f"+{output_type[2]}"
    return new_feature
#extract coreconcept , layer types and toolname
def extract_coreconcept_and_layer(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    if tool_match:
        new_feature=f"{tool_match}-"
    list_input_sort = []
    list_output_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[0])
        list_input_sort.append(input_type[1])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        list_output_sort.append(output_type[0])
        list_output_sort.append(output_type[1])
        new_feature=new_feature+f"+{'_'.join(sorted(list_output_sort))}"
    return new_feature
#extract coreconcept , measurement and toolname
def extract_coreconcept_and_measurement(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    if tool_match:
        new_feature=f"{tool_match}-"
    list_input_sort = []
    list_output_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[0])
        list_input_sort.append(input_type[2])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        list_output_sort.append(output_type[0])
        list_output_sort.append(output_type[2])
        new_feature=new_feature+f"+{'_'.join(sorted(list_output_sort))}"
    return new_feature
def extract_layer_and_measurement(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    if tool_match:
        new_feature=f"{tool_match}-"
    list_input_sort = []
    list_output_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[1])
        list_input_sort.append(input_type[2])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        list_output_sort.append(output_type[1])
        list_output_sort.append(output_type[2])
        new_feature=new_feature+f"+{'_'.join(sorted(list_output_sort))}"
    return new_feature
#extract without toolname
#extract all types
def extract_all_types_without_toolname(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    list_input_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0],input_type[1])
        list_input_sort=list_input_sort+input_type
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        new_feature=new_feature+f"+{'_'.join(sorted(output_type))}"
    return new_feature
#extract only coreconcept
def extract_only_coreconcept_without_toolname(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    list_input_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[0])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        new_feature=new_feature+f"+{output_type[0]}"
    return new_feature
#extract only layer
def extract_only_layer_without_toolname(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    list_input_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[1])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[1])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        new_feature=new_feature+f"+{output_type[1]}"
    return new_feature
#extract only measurement
def extract_only_measurement_without_toolname(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''
    list_input_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        list_input_sort.append(input_type[2])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        new_feature=new_feature+f"+{output_type[2]}"
    return new_feature
#extract coreconcept , layer types
def extract_coreconcept_and_layer_without_toolname(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''

    list_input_sort = []
    list_output_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[0])
        list_input_sort.append(input_type[1])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        list_output_sort.append(output_type[0])
        list_output_sort.append(output_type[1])
        new_feature=new_feature+f"+{'_'.join(sorted(list_output_sort))}"
    return new_feature
#extract coreconcept , measurement
def extract_coreconcept_and_measurement_without_toolname(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''

    list_input_sort = []
    list_output_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[0])
        list_input_sort.append(input_type[2])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        list_output_sort.append(output_type[0])
        list_output_sort.append(output_type[2])
        new_feature=new_feature+f"+{'_'.join(sorted(list_output_sort))}"
    return new_feature
def extract_layer_and_measurement_without_toolname(features_value):
    tool_match = re.search(r"(\w+)-", features_value).group(1)
    input_matches = re.findall(r'-(\w+)', features_value)
    output_match = re.findall(r"\+(\w+)", features_value)
    new_feature=''

    list_input_sort = []
    list_output_sort = []
    for input_match in input_matches:
        input_type=input_match.split('_')
        #print(input_type[0])
        #print(input_type[0],input_type[1])
        list_input_sort.append(input_type[1])
        list_input_sort.append(input_type[2])
    new_feature=new_feature+f"{'_'.join(sorted(list_input_sort))}"
    if output_match:
        output_type=output_match[0].split('_')
        list_output_sort.append(output_type[1])
        list_output_sort.append(output_type[2])
        new_feature=new_feature+f"+{'_'.join(sorted(list_output_sort))}"
    return new_feature
# read the expert json file
current_dir = os.getcwd()
input_folder_expert = os.path.join(current_dir, "../json_file/")
output_folder_expert_full_types = os.path.join(current_dir, "../json_file_full_types/")
output_folder_expert_only_coreconcept=os.path.join(current_dir,'../json_file_only_coreconcept/')
output_folder_expert_only_layer=os.path.join(current_dir,'../json_file_only_layer/')
output_folder_expert_only_measurement=os.path.join(current_dir,'../json_file_only_measurement/')
output_folder_expert_coreconcept_and_layer=os.path.join(current_dir,'../json_file_coreconcept_and_layer/')
output_folder_expert_coreconcept_and_measurement=os.path.join(current_dir,'../json_file_coreconcept_and_measurement/')
output_folder_expert_layer_and_measurement=os.path.join(current_dir,'../json_file_layer_and_measurement/')
#output folder without tool
output_folder_expert_full_types_without_tool = os.path.join(current_dir, "../json_file_full_types_without_tool/")
output_folder_expert_only_coreconcept_without_tool=os.path.join(current_dir,'../json_file_only_coreconcept_without_tool/')
output_folder_expert_only_layer_without_tool=os.path.join(current_dir,'../json_file_only_layer_without_tool/')
output_folder_expert_only_measurement_without_tool=os.path.join(current_dir,'../json_file_only_measurement_without_tool/')
output_folder_expert_coreconcept_and_layer_without_tool=os.path.join(current_dir,'../json_file_coreconcept_and_layer_without_tool/')
output_folder_expert_coreconcept_and_measurement_without_tool=os.path.join(current_dir,'../json_file_coreconcept_and_measurement_without_tool/')
output_folder_expert_layer_and_measurement_without_tool=os.path.join(current_dir,'../json_file_layer_and_measurement_without_tool/')
for file in os.listdir(input_folder_expert):
    if file.endswith('.json'):
        file_path=os.path.join(input_folder_expert,file)
        with open(file_path,'r') as file:
            data=json.load(file)
        edges=data['edges']
        features=data['features']
        new_features={key:extract_coreconcept_and_layer_without_toolname(value) for key,value in features.items()}
        data = {
            "edges": edges,
            "features": new_features
        }

        # json file generate
        numbers = re.findall(r'(\d+)', os.path.basename(file_path))
        filename = f"expert{int(numbers[0])}.json"  # 设置文件名
        if filename=='expert14.json':
            print('features:',new_features)
        #all types
        json_file_name = os.path.join(output_folder_expert_coreconcept_and_layer_without_tool, filename)
        with open(json_file_name, "w") as file:
            json.dump(data, file)

#read the generated json file
input_folder_generated = os.path.join(current_dir, "../json_file_generated/")
output_folder_generated_full_types = os.path.join(current_dir, "../json_file_full_types/")
output_folder_generated_only_coreconcept=os.path.join(current_dir,'../json_file_only_coreconcept/')
output_folder_generated_only_layer=os.path.join(current_dir,'../json_file_only_layer/')
output_folder_generated_only_measurement=os.path.join(current_dir,'../json_file_only_measurement/')
output_folder_generated_coreconcept_and_layer=os.path.join(current_dir,'../json_file_coreconcept_and_layer/')
output_folder_generated_coreconcept_and_measurement=os.path.join(current_dir,'../json_file_coreconcept_and_measurement/')
output_folder_generated_layer_and_measurement=os.path.join(current_dir,'../json_file_layer_and_measurement/')
#output folder without tool
output_folder_generated_full_types_without_tool = os.path.join(current_dir, "../json_file_full_types_without_tool/")
output_folder_generated_only_coreconcept_without_tool=os.path.join(current_dir,'../json_file_only_coreconcept_without_tool/')
output_folder_generated_only_layer_without_tool=os.path.join(current_dir,'../json_file_only_layer_without_tool/')
output_folder_generated_only_measurement_without_tool=os.path.join(current_dir,'../json_file_only_measurement_without_tool/')
output_folder_generated_coreconcept_and_layer_without_tool=os.path.join(current_dir,'../json_file_coreconcept_and_layer_without_tool/')
output_folder_generated_coreconcept_and_measurement_without_tool=os.path.join(current_dir,'../json_file_coreconcept_and_measurement_without_tool/')
output_folder_generated_layer_and_measurement_without_tool=os.path.join(current_dir,'../json_file_layer_and_measurement_without_tool/')
for file in os.listdir(input_folder_generated):
    if file.endswith('.json'):
        file_path=os.path.join(input_folder_generated,file)
        with open(file_path,'r') as file:
            data=json.load(file)
        edges=data['edges']
        features=data['features']
        if not edges:
            continue
        new_features={key:extract_coreconcept_and_layer_without_toolname(value) for key,value in features.items()}
        data = {
            "edges": edges,
            "features": new_features
        }
        numbers = re.findall(r'solution(\d+)', os.path.basename(file_path))
        filename = f"solution{int(numbers[0])}.json"  # 设置文件名
        #all types
        json_file_name = os.path.join(output_folder_generated_coreconcept_and_layer_without_tool, filename)
        with open(json_file_name, "w") as file:
            json.dump(data, file)

print("Edges:")
for edge in edges:
    print(edge)

print("Features:")
for key, value in features.items():
    print(f"{key}: {extract_all_types(value)}")

