from PIL import Image
import pytesseract

def extract_names_from_image(image_path, namelist_file):

    with open(namelist_file, "r") as file:
        lines = file.readlines()
    all_names = set([line.strip() for line in lines])
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
        elif word[:2] in first_two_chars_to_name:
            words2.append(first_two_chars_to_name[word[:2]])

    return words2

extracted_names = extract_names_from_image(image_path="/Users/yujianzhao/Desktop/code/cs50w/try/gateway2.png", namelist_file="gateway_namelist.txt")
print(extracted_names)