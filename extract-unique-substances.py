# Extracts all the unique substances
# Gives a list of all the substances that are contained in the report corpus
# Alex Zhao
# alexzhao@seas.upenn.edu

import re

def dedup_list(input_list):
    """
    deduplicate a list, from https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    """
    return list(dict.fromkeys(input_list))

# a list of unique substances
substances_all = []
regex_and = re.compile(r"\wand\w", re.MULTILINE)

with open("substances-all", "r") as f:
    substances_list = f.readlines()
    for line in substances_list:
        # make everything lowercase
        line = line.lower().strip()
        # some substances are delimited by & rather than ,
        line = line.replace('&', ',').strip()
        line = line.replace('"', '').strip()
        line = line.replace(' and/or ', ',')
        line = line.replace(' and ', ',').strip()
        # line = regex_and.sub(',', line).strip()
        # list of substances for a particular trip report
        current_substances = line.split(",")
        for substance in current_substances:
            # strip out all the whitespaces
            substanceCurr = substance.strip()
            substances_all.append(substanceCurr)

substances_unique = dedup_list(substances_all)
substances_unique.sort()


with open("substances_unique", "w") as out:
    for substance in substances_unique:
        out.write("%s\n" % substance)
