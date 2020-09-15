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
    report('patching missing \\t chars in lines 984, 1367, 3738, 9518 of 06.JoshB.par...')
    joshb = file2text['06.JoshB.par']
    joshb[983] = 'W/)T H/GRG$Y ^ =W/)T W/H/)MRY\t KAI\\ TO\\N AMORRAI=ON '
    joshb[1366] = 'W/H/KHNYM =W/H/)BNYM .m .kb #\t KAI\\ OI( LI/QOI '
    joshb[3737] = 'W/YC+YRW =;W/YC+YDW .rd <9.12\t E)PESITI/SANTO {d} KAI\\ H(TOIMA/SANTO '
    joshb[9517] = "--+ '' =;L/GBWLWT/YHM <19.49>\t E)N TOI=S O(RI/OIS AU)TW=N "
    report('\tdone')

    report('patching extra \\t chars in lines 2007 and 9516 of 06.JoshB.par...')
    # the following lines have one too many tab characters
    joshb[2006] = '-+ =;H/(YR/H <6.20>\tEI)S TH\\N PO/LIN '
    joshb[9515] = "--+ '' =;M/XLQ <19.49>\tDIAMERI/SAS "
    report('\tdone')
  
    # there is a corruption in the lines for Exod 35:19:
    # 
    #     16283 ^ ^^^ =L/$RT {...?H/&RD} #  {+} E)N AI(=S LEITOURGH/SOUSIN
    #     16284 
    #     16285 Exod 1:10
    #     16286     #
    #     16287 
    #     16288 Exod 35:19
    #     16289 --+ E)N AU)TAI=S 
    #
    # the interposition of blank lines and the "Exod 1:10" string are not
    # supposed to be there, and they interrupt the data-lines for Exod 35:19
    # these incorrect lines will be removed; the extra Exod 35:19 heading will
    # likewise become unnecessary
    # NB that line numbers below will be 1 less due to zero-indexing of Python
    report('patching corrupt lines 16283-16289 in 02.Exodus.par...')
    exod = file2text['02.Exodus.par']
    fixed_lines = exod[:16283] + [exod[16285]] + exod[16288:]
    file2text['02.Exodus.par'] = fixed_lines
    report('\tdone')

    # An identical corruption to the one discussed above can be found in
    # likewise in 20.Psalms.par lines 2455-2459
    report('patching corrupt lines 2455-2459 in 20.Psalms.par...')
    pss = file2text['20.Psalms.par']
    fixed_lines = pss[:2456] + [pss[2457]] + pss[2460:]
    file2text['20.Psalms.par'] = fixed_lines
    report('\tdone')

    # a search for lines without \t reveals that numerous lines are 
    # orphaned from their original line, for instance, see DanTh 6:17:
    # >>> 4132     L/DNY)L ,,a TO\N
    # >>> 4133     DANIHL
    # here DANIHL should be a part of the previous line
    # this problem is found in Sirach, Psalms, Daniel, Chronicles, Ezekiel, Neh,
    # etc. and is correlated with the book names. For instance, in the Psalms,
    # the Hebrew column is affected anywhere the characters "PS" appear (פס)
    # In Deuteronomy, the Greek column is affected where DEUT appears in the text
    # This was probably caused by a bad export and regex pattern that inserted a 
    # newline everywhere a book reference was found in the database, with the ill-effect
    # that text containing the first characters of the books were also cleft by the newline. 
    # Since most book abbreviations contain vowels, the Greek column is primarily affected,
    # meaning that orphaned lines need to be shifted up and appended to the Greek column.
    # The one exception to this is Psalms with the "PS" string that is anywhere a 
    # פס appears in the text. These cases need to be merged down to the BEGINNING of the 
    # subsequent line, in the Hebrew column.
    # This script will provide a detailed report in the log about which passages are affected,
    # as well as how these effects are corrected (either shift up or shift down).

    # TODO: This could be better patched by doing a simple search/replace in the text 
    # for all text beginning with book names and preceded by a newline
    # will need a regex pattern that can differentiate genuine booknames and text

    report('patching orphaned lines (see code for description)...')

    # Ps 68:31 is a special case with 2 orphaned lines in a row
    # to prevent need for recursive algorithm, just easier to do this
    report('\tpatching special double-orphan case in Ps 68:31')
    ps68_31 = file2text['20.Psalms.par']
    ps68_31_patch = [ps68_31[10848] + ps68_31[10849] + ps68_31[10850]]
    file2text['20.Psalms.par'] = ps68_31[:10848] + ps68_31_patch + ps68_31[10851:] 

    current_verse = None
    for file, lines in file2text.items():

        filtered_lines = []

        i = 0
        while i < len(lines):

            line = lines[i]

            # track references and keep them
            if ref_string.match(line):
                current_verse = line
                filtered_lines.append(line)
            
            # apply corrections to relevant lines
            elif line and '\t' not in line:
                
                # append to log and report which lines are involved
                show = f'\n\t\t{lines[i-1]}\n\t--> {line}\n\t\t{lines[i+1]}'
                report(f'\tpatching {file} at line {i}, {current_verse}:{show}')

                # shift line down to HB col if it's in Psalms
                if current_verse.startswith('Ps'):
                    filtered_lines.append(line+lines[i+1])
                    i += 1 # shift forward 1 extra to skip already-covered line

                # otherwise shift it up to GK col
                else:
                    filtered_lines[-1] = filtered_lines[-1] + line

            # keep everything else unchanged            
            else:
                filtered_lines.append(line) 

            # advance the position 
            i += 1

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
