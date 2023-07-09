from scipy.spatial.distance import cosine
import pandas as pd

def cosine_similarity(vector1, vector2):
    return 1 - cosine(vector1, vector2)
nci1=pd.read_csv('../features/nci_coreconcept_and_layer_without_tool.csv')
nci2=nci1.iloc[14:,]
print(nci2.columns)
print(nci2)
nci1=nci1.iloc[0:14,]
print(nci1)


out=[]
for index_1,row_nci1 in nci1.iterrows():
    for index_2,row_nci2 in nci2.iterrows():
        out.append([row_nci1.iloc[0]]+[row_nci2.iloc[0]]+[cosine_similarity(row_nci1.iloc[1:],row_nci2.iloc[1:])])
column_names=['expert_embedding','generated_embedding','similarity']
out = pd.DataFrame(out, columns=column_names)

print(out)
values=out.groupby(['expert_embedding','generated_embedding']).agg({'similarity':sum})
#largest
out_largest_similarity=values['similarity'].groupby('expert_embedding', group_keys=False).nlargest(10)
df_out_largest_similarity=out_largest_similarity.to_frame()
print('largest:',df_out_largest_similarity)
#smallest
out_smallest_similarity=values['similarity'].groupby('expert_embedding', group_keys=False).nsmallest(1)
df_out_smallest_similarity=out_smallest_similarity.to_frame()
print('smallest:',df_out_smallest_similarity)
output_path='../features/similarity_full_types.csv'
out.to_csv(output_path, index=None)
#values_median
values_median=out.groupby('expert_embedding')['similarity'].median()
print('values_median:',values_median)
#values_mean
values_mean=out.groupby('expert_embedding')['similarity'].mean()
print('values_mean:',values_mean)