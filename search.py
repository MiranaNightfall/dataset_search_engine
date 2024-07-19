import os
import time
import sys
from colorama import Fore, init
import random

# feature: random font colour for every single line in list

start_time = time.time() # runtime started
total_document = 0
init(autoreset=True) # initialization colorama
section_list = ["kepala putusan", "identitas", "riwayat penahanan", "fakta", "riwayat perkara", "riwayat tuntutan", "riwayat dakwaan", "fakta_hukum", "amar putusan",  "penutup"] #section list
colour_list = ["RED", "CYAN", "GREEN", "MAGENTA", "YELLOW"] # font-colour list
operator_list = ["AND", "OR", "ANDNOT"] # operator list

# a function that showing province section in terminal
def province(file_content):
    input_string = file_content
    start_index = input_string.find('provinsi="') + len('provinsi="') 
    province = input_string[start_index:input_string.find('"', start_index)]
    return province

# a function that showing classification section in terminal
def classification(file_content):
    input_string = file_content
    start_index = input_string.find('klasifikasi="') + len('klasifikasi="') 
    classification = input_string[start_index:input_string.find('"', start_index)]
    return classification

# a function that showing sub classification section in terminal 
def sub_classification(file_content):
    input_string = file_content
    start_index = input_string.find('sub_klasifikasi="') + len('sub_klasifikasi="') 
    sub_classification = input_string[start_index:input_string.find('"', start_index)]
    return sub_classification

# a function that showing judicial institution section in terminal           
def judicial_institution(file_content):
    input_string = file_content
    start_index = input_string.find('lembaga_peradilan="') + len('lembaga_peradilan="') 
    judicial_institution = input_string[start_index:input_string.find('"', start_index)]
    return judicial_institution

# a feature(&function); colorizing each line in terminal
def search_output(file, file_content, font_colour):
    font_colour = font_colour.upper()
    if font_colour == "CYAN":
        output = Fore.CYAN + file + " {: >15} {: >15} {: >30} {: >20}".format(province(file_content)[:15], classification(file_content)[:15], sub_classification(file_content)[:30], judicial_institution(file_content)[:20])
    elif font_colour == "RED":
        output = Fore.RED + file + " {: >15} {: >15} {: >30} {: >20}".format(province(file_content)[:15], classification(file_content)[:15], sub_classification(file_content)[:30], judicial_institution(file_content)[:20])
    elif font_colour == "GREEN":
        output = Fore.GREEN + file + " {: >15} {: >15} {: >30} {: >20}".format(province(file_content)[:15], classification(file_content)[:15], sub_classification(file_content)[:30], judicial_institution(file_content)[:20])
    elif font_colour == "MAGENTA":
        output = Fore.MAGENTA + file + " {: >15} {: >15} {: >30} {: >20}".format(province(file_content)[:15], classification(file_content)[:15], sub_classification(file_content)[:30], judicial_institution(file_content)[:20])
    elif font_colour == "YELLOW":
        output = Fore.YELLOW + file + " {: >15} {: >15} {: >30} {: >20}".format(province(file_content)[:15], classification(file_content)[:15], sub_classification(file_content)[:30], judicial_institution(file_content)[:20])
    return output

# a function; search keywords with operator
def search_keyword_with_operator(file_content, first_keyword, second_keyword, section, operator, file):
    operator = operator.lower()
    global total_document # can be returned outside the function (for total document)

    if section.lower() == "all":
        if operator == 'and' and first_keyword in file_content and second_keyword in file_content:
            output_list = search_output(file, file_content, font_colour)
            print(output_list) # showing an output line
            total_document += 1
        elif operator == 'or' and (first_keyword in file_content or second_keyword in file_content):
            output_list = search_output(file, file_content, font_colour)
            print(output_list) # showing an output line
            total_document += 1
        elif operator == 'andnot' and first_keyword in file_content and second_keyword not in file_content:
            output_list = search_output(file, file_content, font_colour)
            print(output_list) # showing an output line
            total_document += 1
    elif section.lower() in section_list:
        # find a section and slice for the content (<section> content </section>)
        content_section = file_content[file_content.find(f"<{section}>"):file_content.find(f"</{section}>")]
        if operator == 'and' and first_keyword in content_section and second_keyword in content_section:
            output_list = search_output(file, file_content, font_colour)
            print(output_list) # showing an output line
            total_document += 1
        elif operator == 'or' and (first_keyword in content_section or second_keyword in content_section):
            output_list = search_output(file, file_content, font_colour)
            print(output_list) # showing an output line
            total_document += 1
        elif operator == 'andnot' and first_keyword in content_section and second_keyword not in content_section:
            output_list = search_output(file, file_content, font_colour)
            print(output_list) # showing an output line
            total_document += 1

# a function; search keyword without operator
def search_keyword_without_operator(file_content, keyword, section, file):
    global total_document # can be declared outside the function (for total document)
    if section.lower() == "all":
        if keyword.lower() in file_content:
            output_list = search_output(file, file_content, font_colour)
            print(output_list) # showing an output line
            total_document += 1
    elif section.lower() in section_list:
        # find a section and slice for the content (<section> content </section>)
        content_section = file_content[file_content.find(f"<{section}>"):file_content.find(f"</{section}>")]
        if keyword.lower() in content_section:
            output_list = search_output(file, file_content, font_colour)
            print(output_list) # showing an output line
            total_document += 1 

# main program
if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) == 4 or len(sys.argv) > 5:
        print()
        print("Argumen tidak benar")
        exit(1) # exit the program while length of arguments not eligible
    # arguments condition; without operator
    elif len(sys.argv) == 3:
        keyword = sys.argv[2]
        section = sys.argv[1]
        folder_name = '\dataset'
        folder_path = os.getcwd() + folder_name # file path
        list_file = os.listdir(folder_path)
        change_dir = os.chdir(folder_path) # change directory
        for file in list_file:
            with open(file, "r") as f: # open the file
                file_content = f.read()
                font_colour = random.choice(colour_list) # random colour for each line
                search_output(file, file_content, font_colour) # determine the font-colour
                search_keyword_without_operator(file_content, keyword, section, file) # output for every line
    # arguments condition; with operator  
    elif len(sys.argv) == 5:
        first_keyword = sys.argv[2]
        second_keyword = sys.argv[4]
        operator = sys.argv[3]
        section = sys.argv[1]

        if operator.upper() not in operator_list:
            print()
            print("Operator harus berupa AND, OR atau ANDNOT.")
            exit(1)
        folder_name = '\dataset'
        folder_path = os.getcwd() + folder_name # file path
        list_file = os.listdir(folder_path)
        change_dir = os.chdir(folder_path) # change directory
        for file in list_file:
            with open(file, "r") as f: # open the file
                file_content = f.read()
                font_colour = random.choice(colour_list) # random colour for each line
                search_output(file, file_content, font_colour) # determine the font-colour
                search_keyword_with_operator(file_content, first_keyword, second_keyword, section, operator, file) # output for every line

end_time = time.time() # runtime stopped
print()
print("Banyaknya dokumen yang ditemukan =", total_document) # showing total document
print("Total waktu pencarian =", end_time - start_time, "detik") # showing runtime