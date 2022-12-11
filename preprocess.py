import string 
import re
from typing import List, Optional, Union, Callable
from pyvi import ViTokenizer
import pandas as pd

def to_lower(text: str):
    text = text.lower()
    return text

def remove_punctuation(text: str):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    text = text.translate(translator)
    return text

# đã test trên https://regex101.com/
def handle_price_value(text: str):
    text = re.sub(r'\d+k', 'pricev', text)
    return text

# đã test trên https://regex101.com/ phải xử lý sau khi xử price value (nếu có)
def handle_number(text: str):
    text = re.sub(r'\d+', 'numberv', text)
    return text

# đã test trên https://regex101.com/
def handle_duplicate_character(text: str):
    text = re.sub(r'([a-z])\1+', lambda m: m.group(1), text, flags=re.IGNORECASE)
    return text

# đã test trên https://regex101.com/
def handle_score_value(text: str):
    text = re.sub(r'\d+[đd]', 'scorev', text)
    return text

# đã test trên https://regex101.com/
def handle_time_value(text: str):
    text = re.sub(r'\d+[phs\']\d+', 'timev', text)
    text = re.sub(r'\d+[phs\']', 'timev', text)
    return text

# đã test trên https://regex101.com/
def handle_percent_value(text: str):
    text = re.sub(r'\d+%', 'percentv', text)
    return text

def remove_emojis(text: str):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', text)


def handle_acronym(text: str):
    lookup_dict = {
        ' k ': ' không ',
        'ko': ' không ',
        ' kh ': ' không ',
        'mn': 'mọi người',
        'vs': 'với',
        'dc': 'được',
        'đc': 'được',
        'yc': 'yêu cầu',
        'nhg': 'nhưng',
        'ak': 'à',
        'hqa': 'hôm qua',
        'hl': 'hài lòng',
        ' a ': 'anh',
        ' e ': 'em',
        ' j ': 'gì',
        'okie': 'ok',
    }
    for key, value in lookup_dict.items():
        text = text.replace(key, value)
    return text

def remove_noise(text: str):
    # single character word
    text = ' '.join([w for w in text.split() if len(w) > 1])
    return text

def handle_vietnamese(text: str):
    lookup_dict = {
        'òa': 'oà', 'óa': 'oá', 'ỏa': 'oả', 'õa': 'oã', 'ọa': 'oạ', 'òe': 'oè', 'óe': 'oé', 'ỏe': 'oẻ',
        'õe': 'oẽ', 'ọe': 'oẹ', 'ùy': 'uỳ', 'úy': 'uý', 'ủy': 'uỷ', 'ũy': 'uỹ', 'ụy': 'uỵ', 'uả': 'ủa',
        'ả': 'ả', 'ố': 'ố', 'u´': 'ố', 'ỗ': 'ỗ', 'ồ': 'ồ', 'ổ': 'ổ', 'ấ': 'ấ', 'ẫ': 'ẫ', 'ẩ': 'ẩ',
        'ầ': 'ầ', 'ỏ': 'ỏ', 'ề': 'ề', 'ễ': 'ễ', 'ắ': 'ắ', 'ủ': 'ủ', 'ế': 'ế', 'ở': 'ở', 'ỉ': 'ỉ',
        'ẻ': 'ẻ', 'àk': u' à ', 'aˋ': 'à', 'iˋ': 'ì', 'ă´': 'ắ', 'ử': 'ử', 'e˜': 'ẽ', 'y˜': 'ỹ', 'a´': 'á',
    }
    for key, value in lookup_dict.items():
        text = text.replace(key, value)
    return text
    
def word_tokenize(text: str):
    text = ViTokenizer.tokenize(text)
    return text


def preprocessing(text, processing_function_list: Optional[List[Callable]] = None):
    if processing_function_list is None:
        processing_function_list = [to_lower,
                                    handle_price_value,
                                    handle_score_value,
                                    handle_time_value,
                                    handle_percent_value,
                                    handle_number,
                                    remove_punctuation,
                                    remove_emojis,
                                    handle_duplicate_character,
                                    handle_acronym,
                                    handle_vietnamese,
                                    word_tokenize,
                                    remove_noise,
                                    ]
    for func in processing_function_list:
        text = func(text)
    return text

# df = pd.read_csv('dataset/loship/raw.txt')
# df['pre_content'] = df['content'].apply(preprocessing)
# df = df[['pre_content', 'content']]
# df.to_csv('test_clean.txt', sep='\n',header=None, index=None)