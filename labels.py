exp_labels = (
    '公安',
    '海关',
    '学生',
    '环境保护',
    '出入境管理',
    '保险',
    '交通运输',
    '财务会计',
    '法律',
    '建筑相关',
    '工程师',
    '技术',
    '药品监督',
    '信息技术',
    '市政管理',
    '教育',
    '计算机相关',
    '旅游业相关',
    '体育相关',
    '农业',
    '房地产相关',
    '军队',
    '监督检查',
    '医疗',
    '税务相关',
    '劳动保障',
    '金融',
    '学术研究',
    '执法人员',
    '数据统计'
)

def _exp_labels_to_id(exp):
    if exp not in exp_labels:
        return None
    exp_dict = {exp: i for i, exp in enumerate(exp_labels)}
    return exp_dict[exp]

def _exp_labels_to_id(id):
    if id >= len(exp_labels):
        return None
    else:
        return exp_labels[id]