import Levenshtein
import os
import json
import re
import pandas as pd
def extract_features_serialization(input_folder):
    df_features = pd.DataFrame(columns=['workflow_name', 'features_string'])
    for file in os.listdir(input_folder):
        if file.endswith('.json'):
            file_path=os.path.join(input_folder,file)
            with open(file_path,'r') as file:
                data=json.load(file)
            features=data['features']
            new_features=[]
            new_features=[value for key,value in features.items()]
            features_string = ''.join(new_features)
            features_string = features_string.replace("+", "").replace("-", "").replace("_", "")
            # generate column name
            numbers = re.findall(r'expert(\d+)', os.path.basename(file_path))
            if numbers:
                filename = f"expert{int(numbers[0])}"  # 设置文件名
            else:
                numbers = re.findall(r'solution(\d+)', os.path.basename(file_path))
                filename=f"solution{int(numbers[0])}"
            if filename=='expert14':
                print('features:',features_string)
            #create a dataframe including the features_string
            new_data = {'workflow_name': filename, 'features_string': features_string}
            df_features = df_features.append(new_data,ignore_index=True)
    return df_features
current_dir = os.getcwd()

input_folder_full_types = os.path.join(current_dir, "../json_file_full_types/")
input_folder_only_coreconcept=os.path.join(current_dir,'../json_file_only_coreconcept/')
input_folder_only_layer=os.path.join(current_dir,'../json_file_only_layer/')
input_folder_only_measurement=os.path.join(current_dir,'../json_file_only_measurement/')
input_folder_coreconcept_and_layer=os.path.join(current_dir,'../json_file_coreconcept_and_layer/')
input_folder_coreconcept_and_measurement=os.path.join(current_dir,'../json_file_coreconcept_and_measurement/')
input_folder_layer_and_measurement=os.path.join(current_dir,'../json_file_layer_and_measurement/')
#input folder without tool
input_folder_full_types_without_tool = os.path.join(current_dir, "../json_file_full_types_without_tool/")
input_folder_only_coreconcept_without_tool=os.path.join(current_dir,'../json_file_only_coreconcept_without_tool/')
input_folder_only_layer_without_tool=os.path.join(current_dir,'../json_file_only_layer_without_tool/')
input_folder_only_measurement_without_tool=os.path.join(current_dir,'../json_file_only_measurement_without_tool/')
input_folder_coreconcept_and_layer_without_tool=os.path.join(current_dir,'../json_file_coreconcept_and_layer_without_tool/')
input_folder_coreconcept_and_measurement_without_tool=os.path.join(current_dir,'../json_file_coreconcept_and_measurement_without_tool/')
input_folder_layer_and_measurement_without_tool=os.path.join(current_dir,'../json_file_layer_and_measurement_without_tool/')
def generate_all_features_string(input_folder):
    df=extract_features_serialization(input_folder)
    df = df.sort_values(["workflow_name"])
    filename = input_folder.split(os.sep)[-1]
    file_name= re.findall(r"(\w+)", filename)
    file_name=f"{file_name[0]}.csv"
    output_path=os.path.join(current_dir,f"../features_string/{file_name}")
    df.to_csv(output_path, index=None)
generate_all_features_string(input_folder_full_types)
generate_all_features_string(input_folder_only_coreconcept)
generate_all_features_string(input_folder_only_layer)
generate_all_features_string(input_folder_only_measurement)
generate_all_features_string(input_folder_coreconcept_and_layer)
generate_all_features_string(input_folder_coreconcept_and_measurement)
generate_all_features_string(input_folder_layer_and_measurement)
generate_all_features_string(input_folder_full_types_without_tool)
generate_all_features_string(input_folder_only_coreconcept_without_tool)
generate_all_features_string(input_folder_only_layer_without_tool)
generate_all_features_string(input_folder_only_measurement_without_tool)
generate_all_features_string(input_folder_coreconcept_and_layer_without_tool)
generate_all_features_string(input_folder_layer_and_measurement_without_tool)
generate_all_features_string(input_folder_coreconcept_and_measurement_without_tool)

nci1=pd.read_csv('../features_string/json_file_only_measurement_without_tool.csv')
nci2=nci1.iloc[14:,]
nci1=nci1.iloc[0:14,]
#distance = Levenshtein.distance(string1, string2)
#print("Levenshtein distance:", distance)
out=[]
for index_1,row_nci1 in nci1.iterrows():
    for index_2,row_nci2 in nci2.iterrows():
        out.append([row_nci1.iloc[0]]+[row_nci2.iloc[0]]+[Levenshtein.distance(row_nci1.iloc[1],row_nci2.iloc[1])])
column_names=['expert_workflow','generated_workflow','similarity']
out = pd.DataFrame(out, columns=column_names)

values=out.groupby(['expert_workflow','generated_workflow']).agg({'similarity':sum})
#smallest
out_smallest_similarity=values['similarity'].groupby('expert_workflow', group_keys=False).nsmallest(1)
df_out_smallest_similarity=out_smallest_similarity.to_frame()
print('smallest:',df_out_smallest_similarity)
#largest
out_largest_similarity=values['similarity'].groupby('expert_workflow', group_keys=False).nlargest(1)
df_out_largest_similarity=out_largest_similarity.to_frame()
print('largest:',df_out_largest_similarity)

#values_median
values_median=out.groupby('expert_workflow')['similarity'].median()
print('values_median:',values_median)
#values_mean
values_mean=out.groupby('expert_workflow')['similarity'].mean()
print('values_mean:',values_mean)
