from regex_patterns import *
import collections
from pathlib import Path

data = Path('source/patched')

re_sets = [
    ('common', common_tc),
    ('hebrew', heb_tc),
    ('greek', greek_tc),
]

comps = collections.defaultdict(list)

# make sure all patterns compile without error
for name, patterns in re_sets:
    print(f'compiling {name}')
    for i, pattern in enumerate(patterns):
        try:
            comps[name].append(regex.compile(pattern[0]))
        except:
            raise Exception(f'Problem in pattern {i} of {name} set: {pattern}')

# test that all patterns work as expected and
# are able to retrieve at least some matches
examples = collections.defaultdict(lambda: collections.defaultdict(list))

def add_ex(set, pattern, string):
    test = pattern.search(string)
    if test:
        examples[set][pattern.pattern].append((string, test.group(0)))

print('gathering examples...')
for set, patterns in comps.items():
    print(f'\tgathering examples in set {set}')
    for pattern in patterns:
        done = False
        for file in sorted(data.glob('*.par')):
            if done:
                break
            for line in file.read_text().split('\n'):

                # skip reference string lines
                if ref_string.match(line) or not line:
                    continue

                try:
                    heb_col, grk_col = line.split('\t')
                except:
                    raise Exception(file, line)
    
                if set == "common":
                    add_ex(set, pattern, line)
                elif set == "hebrew":
                    add_ex(set, pattern, heb_col)
                elif set == "greek":
                    add_ex(set, pattern, grk_col)

                if len(examples[set][pattern.pattern]) > 5:
                    done = True
                    break

# show all matched patterns
for set, patterns in examples.items():
    print('showing examples')
    print()
    print(f'------ {set} set -----')
    print()
    for i, pattern in enumerate(patterns):
        exs = patterns[pattern]
        print(i, pattern)
        if len(exs) == 0:
            raise Exception(f'pattern has no matches!')
        for ex in exs:
            print(f'\t{ex}')
        print()
