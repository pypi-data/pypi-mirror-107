import os
import torch
import json
import yaml
from dataclasses import dataclass
from torch.utils.data import Dataset
import time

def timeit(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te-ts))
        return result

    return timed

def save_json(R, path):
    """ Obj, path """
    with open(path, 'w', encoding='utf8') as f:
        json.dump(R, f, indent=2, ensure_ascii=False)
    print(f"{path} loaded with {len(R)} samples!")

def load_json(path):
    with open(path, 'r', encoding='utf8') as f:
        obj = json.load(f)
    print(f"{path} loaded with {len(obj)} samples!")
    return obj

def load_yaml(path):
    with open(path) as fin:
        return yaml.safe_load(fin)


class BaseData:    
    def cpu(self):
        for k, v in self.__dict__.items():
            if type(v) is torch.Tensor:
                setattr(self, k, v.cpu())
        return self
    
    def to(self, device):
        for k,v in self.__dict__.items():
            if type(v) is torch.Tensor:
                setattr(self, k, v.to(device))
        return self
    
    def __getitem__(self,index):
        return self.__dict__[index]
    
    def todict(self):
        return self.__dict__
    
    def tolist(self):
        return [ v for k,v in self.__dict__.items()]


@dataclass
class MRCSample(BaseData):

    qid: str = None
    title: str = None
    context: str = None
    question: str = None
    answer_texts: list = None
    answer_starts: list = None
    is_impossible: bool = None


@dataclass
class MRCBatch(BaseData):
    samples : MRCSample  = None
    input_ids: torch.Tensor =None
    attention_mask : torch.Tensor =None
    token_type_ids : torch.Tensor =None
    start_labels : torch.Tensor =None
    end_labels : torch.Tensor =None
    ans_labels : torch.Tensor =None
    offset_mappings : list = None
        
    def __len__(self):
        return self.input_ids.size(0)

def load_data(path):
    R = []
    with open(path, 'r', encoding='utf8') as f:
        obj = json.load(f)
        for entry in obj['data']:
            for sample in entry['paragraphs']:
                context = sample['context'].strip()
                title = sample.get("title", "")
                for qas in sample['qas']:
                    R.append(
                        MRCSample(
                            qid = qas['id'],
                            title=title,
                            context=context,
                            question=qas['question'],
                            answer_texts=[ a['text'].strip() for a in qas.get('answers', [])],
                            answer_starts=[ a['answer_start'] for a in qas.get('answers', [])],
                            is_impossible=qas.get('is_impossible', None)
                        )
                    )

    print(f"{path} loaded with {len(R)} MRCSamples!")
    return R

class MRCDataset(Dataset):

    _max_index = 99999
    def __init__(self, datas, tokenizer):
        self.datas = datas
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.datas)
    
    def __getitem__(self, index):
        sample = self.datas[index]
        qid, title, context, question, answer_texts, answer_starts, is_impossible = sample.tolist()
        if is_impossible:
            answer_text = ""
            # answer_start, answer_end = 0, 0    # 无答案的情况下，start和end指向[CLS] token
            answer_start, answer_end = self._max_index, self._max_index
        else:
            # ans_index = random.sample(range(len(sample.answer_texts)), 1)[0]            # 存在多个候选答案，随机选择一个作为训练目标
            ans_index = 0
            answer_text, answer_start = answer_texts[ans_index], answer_starts[ans_index]
            answer_end = answer_start + len(answer_text)    # 超出模型能处理的最大长度512也没关系，BertForQuestionAnswering在处理时会将
        
        return qid, title, context, question, answer_text, answer_start, answer_end, is_impossible, sample
    
    def _find_start_end_token_index(self, char_start, char_end, input_ids, offset_mapping):
        start_labels, end_labels, ans_labels = [], [], []
        for char_s, char_e, _input_ids, mapping in zip(char_start, char_end, input_ids, offset_mapping):
            if char_start == char_end == 0:
                start_labels.append(0)
                end_labels.append(0)
                ans_labels.append(0)
                continue
            token_s, token_e = None, None
            sep_idx = _input_ids.index(self.tokenizer.sep_token_id)
            context_mapping = mapping[sep_idx:]  # 从第一个SEP Token后开始找 
            for i, (_s, _e) in  enumerate(context_mapping):
                if _s == char_s and token_s is None:
                    token_s = i + sep_idx
                if _e == char_e and token_e is None:
                    token_e = i + sep_idx
            
            if token_e is not None and token_s is not None:
                start_labels.append(token_s)
                end_labels.append(token_e)
                ans_labels.append(1)
            elif token_s is not None:
                start_labels.append(token_s)
                end_labels.append(self._max_index)
                ans_labels.append(1)
            else:
                start_labels.append(0)
                end_labels.append(0)
                ans_labels.append(0)
        return start_labels, end_labels, ans_labels


    def collate_fn(self, batch):
        """
        这里传入的batch参数，即是batch_size条上面__getitem__返回的结果
        此函数返回的结果即为输入到模型中的一个batch
        """
        qid, title, context, question, answer_text, answer_start, answer_end, is_impossible, sample = zip(*batch)
        tokenized = self.tokenizer(list(question), list(context), max_length=512, padding=True, truncation=True, return_offsets_mapping=True)
        start_labels, end_labels, ans_labels = self._find_start_end_token_index(answer_start, answer_end, tokenized.input_ids, tokenized.offset_mapping)
        R = MRCBatch(
            samples= sample,
            input_ids= torch.tensor(tokenized.input_ids),
            attention_mask=torch.tensor(tokenized.attention_mask),
            token_type_ids=torch.tensor(tokenized.token_type_ids),
            start_labels=torch.tensor(start_labels),
            end_labels=torch.tensor(end_labels),
            ans_labels=torch.tensor(ans_labels),
            offset_mappings=tokenized.offset_mapping
        )
        return R


def span_decode(start_logits, end_logits, cls_logits, max_a_len, samples, offset_mappings, use_cls=True, no_answer=""):
    """

    Args:
        start_logits  (torch.Tensor) :  (bsz,seqlen)
        end_logits (torch.Tensor) :   (bsz,seqlen)
        cls_logits (torch.Tensor) :  (bsz, num_classes)
        max_a_len ( int ): 限制答案文本的最大长度
        samples (MRCSample ): 该条数据的所有信息
        offset_mappings ([type]): tokenizer返回的
        use_cls (bool, optional): 是否使用预测的有无答案的概率，False则一定会返回预测的span文本. Defaults to True.
        no_answer (str, optional): Squad和DuReader要求的无答案形式不同，. Defaults to "".

    Returns:
        Dict : {qid: pred_text, ...}
    """
    se_sum = end_logits[:,None,:] + start_logits[:,:,None]
    # 限制值的范围是s<e, 最大长度为 max_a_len        
    mask = torch.tril(torch.triu(torch.ones_like(se_sum), 0), max_a_len)   
    r = (mask * se_sum).masked_fill_((1-mask).bool(), float('-inf'))    # score值全是负的，导致0 > score，选出来s>e了
    start_max, end_max = r.max(2)[0].max(1)[1], r.max(1)[0].max(1)[1]
    answerable = cls_logits.argmax(-1)
    R = {}
    for s, e, a, sample, mapping in zip(start_max, end_max, answerable, samples, offset_mappings):
        if a == 1 and use_cls:
            R[sample.qid] = no_answer
        else:
            s_char, e_char = mapping[s][0], mapping[e][-1]
            pred_text = sample.context[s_char:e_char]
            pred_text = no_answer if pred_text == "" else pred_text
            R[sample.qid] = pred_text
    return R

