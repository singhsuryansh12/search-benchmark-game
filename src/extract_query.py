import json
import sys

# ./program
# wikimedium.1M.nostopwords.tasks OrHighMed,OrHighLow,OrHighHigh,MedTerm,LowTerm,AndHighMed,AndHighLow,AndHighHigh,HighTerm,MedSloppyPhrase,MedPhrase,LowSloppyPhrase,LowPhrase,HighSloppyPhrase,HighPhrase
#

def parse_line(l: str):
    p = l.find('#')
    if p != -1:
        l = l[:p]
    (tag, query) = l.split(':', 1)
    query = query.strip()
    if query.find(':') != -1:
        return None
    return {'query': query, 'tags':[tag]}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Invalid input. Usage: extract_query task_file tag1,tag2,...")

    f = sys.argv[1]
    selectors = set(sys.argv[2].split(','))
    # print("{} {}".format(f,selectors))

    with open(f) as file:
        for line in file:
            record = parse_line(line)
            if record is not None and record['tags'][0] in selectors:
                print(json.dumps(record))


