import re
import csv


def savecsv(contacts_list, filename="phonebook.csv"):
    with open(filename, "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


def getfromline(line: str) -> list:
    fio_groups = re.compile(r'([А-Я][а-я]+)(?:\s|,{,2})([А-Я][а-я]+)(?:\s|,{,2})(?:([А-Я][а-я]+),|,)')
    org_pos = re.compile(r'[^,]*,[^,]*,[^,]*,([^,]*),([^,]*),[^,]*,[^,]*')
    tel = re.compile(
        r'((?:\+7|8))\s*\(?(\d\d\d)\)?(?:-|\s?)(\d\d\d)(?:-|\s?)(\d\d)(?:-|\s?)(\d\d)(?:\s*\(*(доб\.)\s*(\d{3,5})|)')
    email = re.compile(r',((?:\w+\.|)\w+@\w+\.\w+)')

    line_result = []
    line_result.extend(fio_groups.findall(line)[0])
    line_result.extend(org_pos.findall(line)[0])
    tel_phone = tel.search(line)
    if tel_phone:
        p = [''] * 7
        for i, v in enumerate(tel_phone.groups()):
            p[i] = v
        phone_string = f'+7({p[1]}){p[2]}-{p[3]}-{p[4]}' + ['', f' {p[5]}{p[6]}'][bool(p[5])]
    else:
        phone_string = ''
    line_result.append(phone_string)
    email_ = email.findall(line)
    line_result.extend([[''], email_][bool(email_)])
    return line_result


def start():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        title = f.readline().strip().split(',')
        result_dict = {}
        for line in f:
            line_result = getfromline(line)
            if (line_result[0], line_result[1]) in result_dict:
                result_dict[(line_result[0], line_result[1])] = [
                    i_1 if i_1 else i_2 for i_1, i_2 in zip(result_dict[(line_result[0], line_result[1])], line_result)
                ]
            else:
                result_dict[(line_result[0], line_result[1])] = line_result

    contacts_list = [title]
    for value in result_dict.values():
        contacts_list.append(value)
    savecsv(contacts_list, filename='phonebook2.csv')


if __name__ == '__main__':
   start()