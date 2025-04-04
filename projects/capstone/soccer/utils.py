from PIL import Image
import pytesseract
import re

all_names = set(['柴堰尤', '赵家伟', 'zwb', 'lyx', '赵泽宇', 'szk', 'Congee', 'ruilin', '谢鑫喆', 'Ziyan', 'Alex', '青木堂', '严智勇', 'Ye xie', 'David', '师宇豪', '费昊然', '嘉兴', '余永豪', 'Argentina', 'Steven', 'dyk', '陶', 'Louis', 'Fabien', '陈诗玮', '周裕人', '王宇煊', 'Alan', '郭希', 'lkl', '飓风先生', '钟潏晨', '管住嘴迈开腿', '励天一', 'yucheng', '黄泽宇', '杨冠群', '赵宇健', '朱总', '李翼展', 'Tiger', '谢天石', '月下柠檬树', '伍琨', 'Frank'])

def extract_names_from_image(image_path):

    first_two_chars_to_name = {name[:2]: name for name in all_names}

    # Open the image
    img = Image.open(image_path)

    # Extract text from the image with Chinese language support
    text = pytesseract.image_to_string(img, lang='chi_sim').strip()

    words = text.split()
    if '随机分配' in words:
        index = words.index('随机分配')
        words = words[index+1:]
    if '关注' in words:
        index = words.index('关注')
        words = words[:index]

    words1 = []
    for word in words:
        if word[0] == "”":
            word = word[1:]
        if "." in word:
            words1.extend(word.split("."))
        else:
            words1.append(word)

    words2 = []
    for word in words1:
        if len(word) == 3 and word[0] == "谢" and word[:2] not in first_two_chars_to_name:
            words2.append("谢鑫喆")
        elif len(word) == 3 and word[0] == "李" and word[2] == "展":
            words2.append("李翼展")
        elif word[:2] == "管住":
            words2.append("瓜瓜")
        elif len(word) > 0 and word[-1] == "总":
            words2.append("朱总")
        elif len(word) == 3 and word[0] == "赵" and word[2] == "健":
            words2.append("赵宇健")
        elif len(word) > 0 and word[0] == "月":
            words2.append("月下柠檬树")
        elif len(word) > 0 and word[0] == "黄":
            words2.append("黄泽宇")
        elif "励" in word:
            words2.append("励天一")
        elif "lk" in word or "kl" in word:
            words2.append("lkl")
        elif word[:2] in first_two_chars_to_name:
            words2.append(first_two_chars_to_name[word[:2]])

    return words2

def get_attendance_list(raw_text):
    season_pass_names = ["曹彬","xiaosong","伍琨","风","昊天","赵宇健","王宇煊","郭希","怀博群","魔术猪","小苏","Du","子恒","Di","李翼展","泽辉","梁育诚","残风","猛哥","Shawn","邹明昊","GRH","瓜瓜","qgx"]

    if "甩坑" not in raw_text:
        return []
    withdraw_and_signup_names_text = raw_text.split("甩坑")[1].strip()
    if "抢坑" not in withdraw_and_signup_names_text:
        return []
    withdraw_names_text, signup_names_text = withdraw_and_signup_names_text.split("抢坑")
    withdraw_names = [name.strip() for name in re.split(r'[:：.123456789]', withdraw_names_text)]
    withdraw_names = set([name for name in withdraw_names if name != ""])
    
    attendance_names = [name for name in season_pass_names if name not in withdraw_names]
    
    signup_names = signup_names_text.split("paid")
    excluded_chars = set([' ', '(', ')', '（', '）', ':', '：','.','1','2','3','4','5','6','7','8','9','0'])
    for raw_name in signup_names:
        chars = [c for c in raw_name if c not in excluded_chars]
        name = "".join(chars)
        if name != "":
            attendance_names.append(name)

    return attendance_names

