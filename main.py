import re
import csv


edit_contacts = []
edited_contacts_list = []


# редактируем Ф.И.О., форматируем телефоны
def correct_contacts():
    pattern = r"(\+7|8)?[\s\(]*(\d{3})[\)\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s\(]*(\w+\.|\w+\.)?[\s]*(\d+)?\)*"
    subst = r"+7(\2)\3-\4-\5 \6\7"
    for el in contacts_list[1:]:
        names = ' '.join(el[:3]).split(' ')
        names = [x for x in names if x]
        edit_phone = re.sub(pattern, subst, el[5])
        edit_phone = edit_phone.strip(' ')
        if len(names) == 3:
            a = [names[0], names[1], names[2], el[3], el[4], edit_phone, el[6]]
        else:
            a = [names[0], names[1], '', el[3], el[4], edit_phone, el[6]]
        edit_contacts.append(a)

    return edit_contacts


# объединяем записи, проверяем на уникальность
def check_contacts():
    headers = contacts_list[0]
    edited_contacts_list.append(headers)
    contact_dict = {}
    for item in edit_contacts:
        name = item[0], item[1]
        if name not in contact_dict:
            contact_dict[name] = item
        else:
            for i, part in enumerate(contact_dict[name]):
                if part == '':
                    contact_dict[name][i] = item[i]

    for name, person in contact_dict.items():
        for item in person:
            if person not in edited_contacts_list:
                edited_contacts_list.append(person)

    return edited_contacts_list

# записываем файл в формат CSV
def write_file(file):
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(edited_contacts_list)



if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    correct_contacts()
    check_contacts()
    write_file("phonebook.csv")
