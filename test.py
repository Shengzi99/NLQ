# import json

# with open('labeled_data/stats.json', 'r', encoding='utf-8') as f:
#     stats_dict = json.load(f)

# for label in stats_dict:
#     if label != 'total':
#         print(str(round(stats_dict[label] / stats_dict['total'], 2)) + ',', end=" ")
#         # print('\'' + label+'\''+',')

print(len([0.02, 0.03, 0.08, 0.03, 0.05, 0.03, 0.02, 0.02, 0.02, 0.09, 0.04, 0.02, 0.02, 0.08, 0.02, 0.02, 0.02, 0.02, 0.12, 0.03, 0.02, 0.03, 0.02, 0.02, 0.04, 0.03, 0.02, 0.02, 0.02]), sum([0.02, 0.03, 0.08, 0.03, 0.05, 0.03, 0.02, 0.02, 0.02, 0.09, 0.04, 0.02, 0.02, 0.08, 0.02, 0.02, 0.02, 0.02, 0.12, 0.03, 0.02, 0.03, 0.02, 0.02, 0.04, 0.03, 0.02, 0.02, 0.02]))