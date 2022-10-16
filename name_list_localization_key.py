'''
CWTools generate missing loc is great but it generates a "REPLACE_ME" for each tag
Replacing each and everyone for names is too much of a hassle

This script loads the localization (English currently) and the name list
It will then check if the name in name_list is a tag and the tag exist in localization
If not a tag then it will generate one making sure the tag corresponds to the name
There is also an option for a prefix if you want to differentiate tags for different species (1 species per file currently)

The script does not deal with sequential_name so these must be manually edited
'''


import re

def readTags(localizationFilePath):
    file_localization = open(localizationFilePath, "r")
    lines_local = file_localization.readlines()
    tag_dict = {}
    for line in lines_local:
        if line.find(':')==-1 and line.find('\"')==-1:
            continue
        tag = line[:line.find(':')]
        name = line[line.find('\"'):]
        tag_dict[tag]=name.replace('\n','')
    return tag_dict
			
def check_and_create_tags(lines, tags = [], prefix = ''):
    local_lines = []
    for line in lines:
        quotedWords = re.findall('"([^"]*)"', line)
        line_noquotes = line
        for word in quotedWords:
            line_noquotes = line_noquotes.replace(word,'').replace('\"','')
            if word in tags:
                continue
            tag = (prefix + '_' if not prefix == '' else '') + word.replace(' ','').replace('\'','')
            local_line = tag + ':0 ' + '\"' + word + '\"'
            local_lines.append(local_line)

        spaceWords = line_noquotes.split()
        for word in spaceWords:
            if word in tags:
                continue
            tag = (prefix + '_' if not prefix == '' else '') + word.replace('\'','').strip()
            local_line = tag + ':0 ' + '\"' + word + '\"'
            local_lines.append(local_line)
    return local_lines
	
def outputTags(section_head, tags):
    print('\n### '+section_head+' ###\n')
    for tag in tags:
        print(tag)

modPath = "D:/PREDATOR/Documents/Paradox Interactive/Stellaris/mod/fantastical_magiks"
filepath_localization = modPath + "/localisation/english/name_lists/name_list_Drakiel_l_english.yml"
filepath_namelist = modPath + "/common/name_lists/DRAKIEL.txt"

f = open(filepath_namelist, "r")
lines = f.readlines()
tags = readTags(filepath_localization)

found_section_head = False
potential_section_head = ''
potential_lines = []

for line in lines:

    index_equalsign = line.find('=')
    index_openbrace = line.find('{')
    index_closebrace = line.find('}')
    if index_equalsign>=0 and index_openbrace>=0:
        head = line[:index_equalsign].strip()
        potential_section_head = head
        potential_lines.clear()
        found_section_head = True
        continue

    if found_section_head:
        potential_line = line.replace('}','').replace('=','').replace('sequential_name','').strip()
        if not potential_line == '':
            potential_lines.append(potential_line)
		
    if index_closebrace>=0:
        if potential_lines:
            createdTags = check_and_create_tags(potential_lines, tags, 'DRA')
            if createdTags:
                outputTags(potential_section_head ,createdTags)
            potential_section_head = ''
            potential_lines = []

f.close()

    
    
