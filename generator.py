import os
import json
import yaml
import numpy as np
from labels import _label_to_id, _id_to_label

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
        resume_label_dict = yaml.load(open(self.config['resume_label_path'], 'r'), Loader=yaml.FullLoader)
        label_resume_dict = yaml.load(open(self.config['label_resume_path'], 'r'), Loader=yaml.FullLoader)
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
        self.raw_text = None
        self.edu = {}   # {'query_text': None, 'attribute': None}
        self.age = {}   # {'query_text': None, 'attribute': None, 'condition': None}
        self.rank = {}   # {'query_text': None, 'attribute': None, 'condition': None}
        self.work_exp = []
    def random_generate(self):
        ...
    def load_query(self):
        ...

resume_config = yaml.load(
    open('config/resume.yaml', "r"), Loader=yaml.FullLoader
)

for i in range(10):
    qg = ResumeGenerator(i, resume_config)
    qg.load_resume()