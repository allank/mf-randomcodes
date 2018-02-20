import argparse
import string
import random
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("--generate", dest='generate', type=int, help="the number of unique codes to generate")
parser.add_argument("--template", dest='template', type=str, help="the template to use to build the codes")
parser.add_argument("--exclude", dest='exclusions', type=str, help="numbers and letters to exclude", default = [])
args = parser.parse_args()

numrequired = int(args.generate)

template = args.template.upper()
tlength = len(template)

if type(args.exclusions) is str:
	exclusions = args.exclusions.split()
else:
	exclusions = []

candidates_alpha = [x for x in string.ascii_uppercase if x not in [y.upper() for y in exclusions]]
candidates_numeric = [x for x in [y for y in range(0,10)] if x not in exclusions]

perms = 1

if tlength > 0:
    for c in template:
        if c == 'X':
            perms = perms * len(candidates_alpha)
        else:
            perms = perms * len(candidates_numeric)

if numrequired > perms:
	print("Sadly, you are asking for more codes than your template supports")
	print("The template {} can only provide {} random codes".format(template, perms))
	quit()

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
query = "create table codes (code char({}) not null, unique (code))".format(len(template))
cursor.execute(query)

completed = 0
codes = []
while completed < numrequired:
    generated = ''
    for c in template:
        if c == 'X':
            generated += random.choice(candidates_alpha)
        else:
            generated += str(random.choice(candidates_numeric))
    try:
        query = "insert into codes values ('{}')".format(generated)
        cursor.execute(query)
        completed += 1
        codes.append(generated)
    except:
        pass
conn.commit()
conn.close()

with open('codes.txt', 'w') as f:
    for c in codes:
        f.write("%s\n" % c)

print("{} codes generated in codes.txt".format(completed))       
