import re
from pathlib import Path
from regex_patterns import ref_string
from datetime import datetime

def patch(data_dir='source', output_dir='source/patched', silent=False):
    """Corrects known errors in the CATSS database."""

    log = ''
    log += datetime.now().__str__() + '\n'

    def report(msg):
        # give feedback
        nonlocal log # see https://stackoverflow.com/a/8178808/8351428
        log += msg + '\n'
        if not silent:
            print(msg)
    
    data = Path(data_dir)
    file2text = {}

    for file in data.glob('*.par'):
        file2text[file.name] = file.read_text().split('\n')

    # the following lines lack a tab character between the columns
    # corrections add a tab char
    report('patching missing \\t chars in 06.JoshB.par...')
    joshb = file2text['06.JoshB.par']
    joshb[983] = 'W/)T H/GRG$Y ^ =W/)T W/H/)MRY\t KAI\\ TO\\N AMORRAI=ON '
    joshb[1366] = 'W/H/KHNYM =W/H/)BNYM .m .kb #\t KAI\\ OI( LI/QOI '
    joshb[3737] = 'W/YC+YRW =;W/YC+YDW .rd <9.12\t E)PESITI/SANTO {d} KAI\\ H(TOIMA/SANTO '
    joshb[9517] = "--+ '' =;L/GBWLWT/YHM <19.49>\t E)N TOI=S O(RI/OIS AU)TW=N "
    report('\tdone')
  
    # a search for lines without \t reveals that numerous lines are 
    # orphaned from their original line, for instance, see DanTh 6:17:
    # >>> 4132     L/DNY)L ,,a TO\N
    # >>> 4133     DANIHL
    # here DANIHL should be a part of the previous line, or it should
    # at least be marked with # to indicate the continuation of a line 
    # in the subsequent line
    # all such patched cases will be noted when running the patcher if 
    # not silent 
    report('patching orphaned lines (see code for description)...')
    report('the following lines will be joined to their previous')

    # Ps 68:31 is a special case with 2 orphaned lines in a row
    # that instead of being merged up should be merged down together
    # we handle that here
    report('\tpatching special double-orphan case in Ps 68:31')
    ps68_31 = file2text['20.Psalms.par']
    ps68_31_patch = [ps68_31[10848] + ps68_31[10849] + ps68_31[10850]]
    file2text['20.Psalms.par'] = ps68_31[:10848] + ps68_31_patch + ps68_31[10851:] 
    
    for file, lines in file2text.items():

        filtered_lines = []

        for i, line in enumerate(lines):

            # keep other lines 
            if (ref_string.match(line)) or (not line):
                filtered_lines.append(line)
            
            # apply corrections to relevant lines
            elif '\t' not in line:
                report(f'\tpatching {file} line {i}: {line}')
                filtered_lines[-1] = filtered_lines[-1] + line 

            else:
                filtered_lines.append(line) 

        # reassign to new lines
        file2text[file] = filtered_lines

    report('\tdone')

    # export the corrected files
    report(f'writing patched data to {output_dir}')
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    for file, lines in file2text.items():
        text = '\n'.join(lines)
        file_path = output_dir.joinpath(file)
        file_path.write_text(text)

    log_path = output_dir.joinpath('log.txt')
    log_path.write_text(log)

    report('DONE with all patches!')
