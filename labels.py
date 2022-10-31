exp_labels = (
    '劳动保障',
    '保险',
    '学生',
    '交通运输',
    '技术',
    '建筑相关',
    '工程师',
    '房地产相关',
    '军队',
    '公安',
    '财务会计',
    '金融',
    '税务相关',
    '监督检查',
    '海关',
    '法律',
    '农业',
    '出入境管理',
    '市政管理',
    '执法人员',
    '数据统计',
    '医疗',
    '信息技术',
    '计算机相关',
    '教育',
    '环境保护',
    '旅游业相关',
    '学术研究',
    '体育相关'
)

def _label_to_id(exp):
    if exp not in exp_labels:
        return None
    exp_dict = {exp: i for i, exp in enumerate(exp_labels)}
    return exp_dict[exp]

def _id_to_label(id):
    if id >= len(exp_labels):
        return None
    else:
        return exp_labels[id]