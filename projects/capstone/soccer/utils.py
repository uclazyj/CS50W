from PIL import Image
import pytesseract

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