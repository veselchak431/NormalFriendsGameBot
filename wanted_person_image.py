from PIL import Image, ImageDraw, ImageFont


def w_wrap(word: str) -> str:
    def is_vow(let: str) -> bool:
        _vowels = ['а', 'о', 'и', 'е', 'ё', 'э', 'ы', 'у', 'ю', 'я', 'А', 'О', 'И', 'Е', 'Ё', 'Э', 'Ы', 'У', 'Ю', 'Я']
        return let in _vowels

    def is_cons(let: str) -> bool:
        _consonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'щ',
                       'ш', 'Б', 'В', 'Г', 'Д', 'Ж', 'З', 'К', 'Л', 'М', 'Н', 'П', 'Р', 'С', 'Т', 'Ф', 'Х', 'Ц', 'Ч',
                       'Ш', 'Щ']
        return let in _consonants

    def vow_inds(wrd: str):
        return [i for i in range(len(wrd) - 2) if is_vow(wrd[i])]

    vow_indices = vow_inds(word)
    if vow_indices and vow_indices[0] + 2 < len(word):
        for ind in vow_indices:
            sep = '-'
            ind += 1

            if (is_cons(word[ind]) or word[ind] in 'йЙ') and not is_vow(word[ind + 1]):
                ind += 1
            if len(word[:ind]) == 1:  # не даем отделять единичные гласные
                sep = ''
            if len(word) > 3 and word[ind] in 'ьЬЪъ':
                if word[-1] in 'ьЬЪъ':
                    sep = ''
                ind += 1

            return word[:ind] + sep + w_wrap(word[ind:])
    return word


def create_foto_of_wanted(height, word):
    print("###create_foto_of_wanted  вызвана")
    im = Image.open('foto.jpg')
    print("###foto.jpg открыт")
    font = ImageFont.truetype("arial.ttf", size=50)
    draw_text = ImageDraw.Draw(im)

    draw_text.text((780, 285), str(height), font=font, fill='#000000')

    word = w_wrap(word)
    word = word.split("-")
    text = []

    for i in range(0, 5):
        text.append("-".join(word[i * 7:(i + 1) * 7]))
        if i == 4:
            text.append("-".join(word[28:]))
        text[i] = text[i].replace("-", "")

        if i > 0 and len(text[i]) > 0:
            if (text[i - 1][-1:1] != " ") and (text[i][0:1] != " "):
                print(text[i - 1])
                text[i - 1] = text[i - 1] + "-"

    draw_text.text((600, 445), text[0], font=font, fill='#000000')
    draw_text.text((600, 525), text[1], font=font, fill='#000000')
    draw_text.text((600, 600), text[2], font=font, fill='#000000')
    draw_text.text((600, 680), text[3], font=font, fill='#000000')
    draw_text.text((100, 760), text[4], font=font, fill='#000000')
    print("###foto.jpg изменен")
    im.save('wanted.jpg')
    print("###wanted.jpg сохранен")
    return im


if __name__ == "__main__":
    pass
     #create_foto_of_wanted(str(135), ('бщественное существо, обладающее разумом и сознанием, а также субъект '
     #                              'общественно-исторической деятельности и культуры'))

