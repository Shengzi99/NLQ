import os
import json
import yaml
import argparse
import random
import numpy as np
from labels import _label_to_id, _id_to_label

resume_label_dict = yaml.load(open('labeled_data/resume_label_data.json', 'r'), Loader=yaml.FullLoader)
label_resume_dict = yaml.load(open('labeled_data/label_resume_data.json', 'r'), Loader=yaml.FullLoader)

class ResumeGenerator():
    def __init__(self, id, config):
        self.id = id
        self.config = config
        self.edu = None
        self.age = None
        self.gen = None
        self.rank = None
        self.work_exp = {}
        self.random_generate()

    def random_generate(self):
        self.edu = np.random.choice(self.config['edu']['degree'], p=self.config['edu']['prob'])
        self.age = np.random.choice(range(self.config['age']['min'], self.config['age']['max'] + 1))
        self.gen = np.random.choice(self.config['gender'])
        self.rank = np.random.choice(self.config['rank']['degree'], p=self.config['rank']['prob'])
        work_exp_num = np.random.choice(self.config['work_exp']['nums'], p=self.config['work_exp']['prob'])
        for i in range(work_exp_num):
            label_id = np.random.choice(self.config['work_exp']['label_id'], p=self.config['work_exp']['label_prob'])
            resume = np.random.choice(label_resume_dict[_id_to_label(label_id)])
            self.work_exp[resume] = {}
            self.work_exp[resume]['label'] = resume_label_dict[resume]
            self.work_exp[resume]['start_time'] = np.random.choice(self.config['work_exp']['start_time'])+np.random.choice(self.config['work_exp']['month'])
            duration = np.random.choice(self.config['work_exp']['duration'], p=self.config['work_exp']['duration_prob'])
            self.work_exp[resume]['end_time'] = self.work_exp[resume]['start_time'] + duration + np.random.choice(self.config['work_exp']['noise'])
            self.work_exp[resume]['start_time'] = str(round(self.work_exp[resume]['start_time'], 1))
            self.work_exp[resume]['end_time'] = str(round(self.work_exp[resume]['end_time'], 1))

    def load_resume(self):
        result = {'id': self.id, '教育经历': self.edu, '年龄': str(self.age), '性别': self.gen, '职级': self.rank, '工作经历': self.work_exp}
        with open(os.path.join(self.config['load_path'], str(self.id)+'.json'), 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)


class QueryGenerator():
    def __init__(self, id, config):
        self.config = config
        self.id = id
        self.raw_text = None
        self.edu = {}   # {'query_text': None, 'attribute': None}
        self.gen = {}   # {'query_text': None, 'attribute': None}
        self.rank = {}   # {'query_text': None, 'attribute': None}
        self.age = {}   # {'query_text': None, 'attribute': None, 'condition': None}
        self.work_exp = {'exp': [], 'logic': None}
        self.random_generate()

    def random_generate(self):
        # resume_label_dict = yaml.load(open(self.config['resume_label_path'], 'r'), Loader=yaml.FullLoader)
        # label_resume_dict = yaml.load(open(self.config['label_resume_path'], 'r'), Loader=yaml.FullLoader)
        raw_text_list = []
        
        template, entity = np.random.choice(self.config['edu']['template']), list(self.config['edu']['dict'].items())[np.random.choice(list(range(len(self.config['edu']['dict']))), p=self.config['edu']['prob'])]
    
        self.edu['query_text'] = template.replace("%", entity[0])
        self.edu['attribute'] = entity[1]
        raw_text_list.append(self.edu['query_text'])

        if np.random.choice([1, 0], p=self.config['rank']['generate']):
            template, entity = np.random.choice(self.config['rank']['template']), np.random.choice(self.config['rank']['dict'], p=self.config['rank']['prob'])
            self.rank['query_text'] = template.replace("%", entity)
            self.rank['attribute'] = entity
            raw_text_list.append(self.rank['query_text'])

        if np.random.choice([1, 0], p=self.config['gender']['generate']):
            template, entity = np.random.choice(self.config['gender']['template']), np.random.choice(self.config['gender']['dict'], p=self.config['gender']['prob'])
            self.gen['query_text'] = template.replace("%", entity)
            self.gen['attribute'] = entity
            raw_text_list.append(self.gen['query_text'])           

        if np.random.choice([1, 0], p=self.config['age']['generate']):
            template, entity, condition = np.random.choice(self.config['age']['template']), np.random.choice(self.config['age']['dict'], p=self.config['age']['prob']), np.random.choice(self.config['age']['condition'])
            self.age['query_text'] = template.replace("%", entity).replace("*", condition)
            self.age['attribute'] = entity
            self.age['condition'] = condition 
            raw_text_list.append(self.age['query_text'])         

        exp_num = np.random.choice(self.config['work_exp']['nums'], p=self.config['work_exp']['prob'])
        exp_raw_text = ""

        template, label_id =  np.random.choice(self.config['work_exp']['template']), np.random.choice(self.config['work_exp']['label_id'], p=self.config['work_exp']['label_prob']) 
        label = _id_to_label(label_id)
        condition = None
        if '%' in template:
            time, condition = list(self.config['work_exp']['time'].items())[np.random.choice(list(range(len(self.config['work_exp']['time']))))], np.random.choice(self.config['work_exp']['time_condition'])
            template = template.replace("#", label).replace("%", time[0]).replace("*", condition)
            condition = (time[1], condition)
        else:
            template = template.replace("#", label)
        self.work_exp['exp'].append({'query_text': template, 'attribute': label, 'condition': condition})
        exp_raw_text += template

        if exp_num == 2:
            template, label_id =  np.random.choice(self.config['work_exp']['template']), np.random.choice(self.config['work_exp']['label_id'], p=self.config['work_exp']['label_prob']) 
            label = _id_to_label(label_id)
            condition = None
            if '%' in template:
                time, condition = list(self.config['work_exp']['time'].items())[np.random.choice(list(range(len(self.config['work_exp']['time']))))], np.random.choice(self.config['work_exp']['time_condition'])
                template = template.replace("#", label).replace("%", time[0]).replace("*", condition)
                condition = (time[1], condition)
            else:
                template = template.replace("#", label)
                self.work_exp['exp'].append({'query_text': template, 'attribute': label, 'condition': condition})
            logic = np.random.choice(['和', '或'], p=[0.3, 0.7])
            self.work_exp['logic'] = logic
            exp_raw_text += logic
            exp_raw_text += template
        raw_text_list.append(exp_raw_text)
        
        random.shuffle(raw_text_list)
        
        self.raw_text = ""
        for i in range(len(raw_text_list) - 1):
            self.raw_text += raw_text_list[i]
            self.raw_text += np.random.choice([',', '，', ' '], p=[0.2, 0.7, 0.1])
        
        self.raw_text += raw_text_list[len(raw_text_list) - 1]
        self.raw_text += np.random.choice(['.', '。', ''], p=[0.2, 0.7, 0.1])

        # print(self.raw_text)

    def load_query(self):
        result = {'id': self.id, 'raw_text': self.raw_text, '教育经历': self.edu, '年龄': self.age, '性别': self.gen, '职级': self.rank, '工作经历': self.work_exp}
        with open(os.path.join(self.config['load_path'], str(self.id)+'.json'), 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)       

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, choices=['query', 'resume'], help="choice what type of data to generate", required=True)
    parser.add_argument("-n", "--nums", type=int, help="the number of data to generate", required=True)
    args = parser.parse_args()

    if args.mode == 'resume':
        resume_config = yaml.load(
            open('config/resume.yaml', "r"), Loader=yaml.FullLoader
        )
        for i in range(args.nums):
            rg = ResumeGenerator(i, resume_config)
            rg.load_resume()

    if args.mode == 'query':
        query_config = yaml.load(
            open('config/query.yaml', "r"), Loader=yaml.FullLoader
        )
        for i in range(args.nums):
            rg = QueryGenerator(i, query_config)
            rg.load_query()