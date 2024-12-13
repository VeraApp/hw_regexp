import csv
import re

def read_file():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

def write_file(contact_list_result):
    with open("phonebook_resul.csv", "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(contact_list_result)

def correct_name(contacts_list):
    lastname= []
    firstname = []
    sourname = []
    for id, contact in enumerate(contacts_list):
        if contact[0].isalpha():
          lastname.append(contact[0])
          if contact[1].isalpha():
              firstname.append(contact[1])
              sourname.append(contact[2])
          else:
              fullname = contact[1].split()
              firstname.append(fullname[0])
              sourname.append(fullname[1])
        else:
          fullname = contact[0].split()
          if len(fullname) == 3:
              lastname.append(fullname[0])
              firstname.append(fullname[1])
              sourname.append(fullname[2])
          else:
              lastname.append(fullname[0])
              firstname.append(fullname[1])
              sourname.append(contact[2])
    return lastname, firstname, sourname

def sort_phone(contacts_list):
    phone = []
    reg_pattern_phone = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d+)"
    reg_pattern_extension = r"\(?(доб.)\s*(\d*)\)?"
    sub_phone = r"+7(\2)\3-\4-\5"
    sub_ext = r"\1\2"
    pattern_phone = re.compile(reg_pattern_phone)
    pattern_ext = re.compile(reg_pattern_extension)
    for id, contact in enumerate(contacts_list):
        if len(contact[5]) == 0:
            phone.append("")
        else:
            if "доб." in contact[5]:
                res_phone = pattern_phone.sub(sub_phone, contact[5])
                res_phone = pattern_ext.sub(sub_ext, res_phone)
                phone.append(res_phone)
            else:
                res_phone = pattern_phone.sub(sub_phone, contact[5])
                phone.append(res_phone)
    return phone

def sort_contact(contacts_list):
    organization = []
    position = []
    email = []
    for id, contact in enumerate(contacts_list):
        organization.append(contact[3])
        position.append(contact[4])
        email.append(contact[6])
    return organization, position, email

def gen_list(lastname, firstname, sourname, organization, position, phone, email):
    list_file = []
    add_set = set()
    add_dict = dict()
    for id, contact in enumerate(lastname):
        # print(f"Id: {id}")
        # #print(f"Contact: {contact}")
        fio = f"{lastname[id]} {firstname[id]}"
        if fio not in add_set:
            add_set.add(fio)
            add_dict[fio] = [lastname[id], firstname[id], sourname[id], organization[id], position[id], phone[id], email[id]]
        else:
            value_contact = add_dict[fio]
            if value_contact[3] == "":
                value_contact[3] = organization[id]
            if value_contact[4] == "":
                value_contact[4] = position[id]
            if value_contact[5] == "":
                value_contact[5] = phone[id]
            if value_contact[6] == "":
                value_contact[6] = email[id]
            add_dict.update(fio = value_contact)
    add_dict.pop("fio")
    values = list(add_dict.values())
    return values

def main():
    contact_list = read_file()
    lastname, firstname, sourname = correct_name(contact_list)
    phone = sort_phone(contact_list)
    organization, position, email = sort_contact(contact_list)
    contact_list_result = gen_list(lastname, firstname, sourname, organization, position, phone, email)
    write_file(contact_list_result)

main()