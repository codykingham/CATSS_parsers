import re
from pathlib import Path
from regex_patterns import ref_string, hchars, gchars
from datetime import datetime

def patch_morpho(data_dir='source', output_dir='source/patched', silent=False, debug=False):
    log = ''
    log += datetime.now().__str__() + '\n'

    n_edits = 0

    def report(msg):
        # give feedback
        nonlocal log # see https://stackoverflow.com/a/8178808/8351428
        log += msg + '\n'
        if not silent:
            print(msg)
    
    data = Path(data_dir)
    file2lines = {}

    for file in data.glob('*.mlxx'):
        file2lines[file.name] = file.read_text().split('\n')

    # apply select changes 
    edits = [
        ('01.Gen.1.mlxx', 12540, 'ADI2P', "KAQI/SATE                VA  AAD2P  I(/ZW            KATA"),
        ('05.Num.mlxx', 24859, 'SONTAIVC', "SUGKATAKLHRONOMHQH/SONTAI VC  APS2S  KLHRONOME/W      SUN   KATA"),
    ]
    report('\napplying bulk manual edits...\n')

    file = ''
    for edit in edits:

        # unpack data
        file = edit[0] or file
        ln, re_confirm, redaction = edit[1:]
        old_line = file2lines[file][ln]

        # confirm and apply changes, give reports throughout
        if re.findall(re_confirm, old_line):
            file2lines[file][ln] = redaction
            report(f'correction for {file} line {ln}:')
            report(f'\tOLD: {old_line}')
            report(f'\tNEW: {redaction}')
            n_edits += 1
        else:
            if debug:
                raise Exception(f'FOLLOWING EDIT UNCONFIRMED: {edit} at {old_line}')
            report(f'**WARNING: THE FOLLOWING EDIT WAS NOT CONFIRMED**:')
            report(f'\tTARGET: {old_line}')
            report(f'\tEDIT: {edit}')

    # export the corrected files
    report(f'\nwriting patched data to {output_dir}')
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    for file, lines in file2lines.items():
        text = '\n'.join(lines)
        file_path = output_dir.joinpath(file)
        file_path.write_text(text)

    # write changes to a log file
    log_path = output_dir.joinpath('log.txt')
    log_path.write_text(log)

    report('\nDONE with all patches!')
    report(f'\ttotal edits: {n_edits}')


def patch_parallel(data_dir='source', output_dir='source/patched', silent=False, debug=False):
    """Corrects known errors in the CATSS database."""

    log = ''
    log += datetime.now().__str__() + '\n'

    n_edits = 0

    def report(msg):
        # give feedback
        nonlocal log # see https://stackoverflow.com/a/8178808/8351428
        log += msg + '\n'
        if not silent:
            print(msg)
    
    data = Path(data_dir)
    file2lines = {}

    for file in data.glob('*.par'):
        file2lines[file.name] = file.read_text().split('\n')

    # -- Manual Edits --

    # manual corrections loaded into tuples consisting of:
    # (file, line_number, regex condition, new line)
    # where line numbers refer to the original line numbers in the docs,
    # the regex condition is a pattern to search all in the line to confirm the 
    # change (a safeguard for erroneous changes or for when the underlying data
    # changes). All of the changes are enacted in a large loop.
    # If filename is left empty, the previous filename is used
    # NB: linenumbers are given as 0-indexed
    edits = [
        ('06.JoshB.par', 983, 'MRY KAI', 'W/)T H/GRG$Y ^ =W/)T W/H/)MRY\t KAI\\ TO\\N AMORRAI=ON '),
        ('', 1366, '\.kb # KAI', 'W/H/KHNYM =W/H/)BNYM .m .kb #\t KAI\\ OI( LI/QOI '),
        ('', 3737, '12 E', 'W/YC+YRW =;W/YC+YDW .rd <9.12>\t E)PESITI/SANTO {d} KAI\\ H(TOIMA/SANTO'), 
        ('', 9517, '<19.49> E', "--+ '' =;L/GBWLWT/YHM <19.49>\t E)N TOI=S O(RI/OIS AU)TW=N "),
        ('', 2006, '\t<6.20>\t', '-+ =;H/(YR/H <6.20>\tEI)S TH\\N PO/LIN '),
        ('', 9515, '\t<19\.49>\t', "--+ '' =;M/XLQ <19.49>\tDIAMERI/SAS "),
        ('', 7104, 'RNA.*\t', 'W/DNH =:W/RNH .dr\tKAI\ RENNA'),
        ('', 1659, '----', "M/MCRYM\t--- ''"),
        ('', 4673, '{=51}', "W/YMYT/M\t--- <=51>"), # Normalize this to a note
        ('', 10235, '{TOU', "--+\tSALAMIN {d} {...TOU= SWTHRI/OU}"),
        ('', 11304, 'A\)PO\|', "M/CPWN\tA)PO\ BORRA= [31] "),
        ('07.JoshA.par', 645, ' \)PO', "M/&M)L\tA)PO\ A)RISTERW=N"),
        ('01.Genesis.par', 9550, "--\+ ' ", "--+ '' =;W/BH <24.14>\tKAI\ E)N TOU/TW|"),
        ('', 9552, "--\+ ' ", "--+ '' =;KY <24.14>\tO(/TI"),
        ('', 9557, '=:ABRHM', "--+ =:)BRHM\tABRAAM"),
        ('', 2316, '--= ', "--+ '' =H/BHMH\tTW=N KTHNW=N"),
        ('', 12939, '\.a', "B/GLL/K =?B/RGL/YK .s <^30.30\tTH=| SH=| ^ EI)SO/DW|"), # typo: .a for .s
        ('', 10822, '}}', "NG(NW/K\t{...H(MEI=S} {...SE} ^ E)BDELUCA/MEQA"),
        ('17.1Esdras.par', 477, 'CC35\.24', 'W/Y(BYR/HW\tKAI\\ {..^A)PE/STHSAN AU)TO\\N} [cc35.24]'),
        ('', 6514, 'LI.*\t', ")L(ZR =:)LYW(NY\tE)LIWNA=S [e10.31]"),
        ('', 2857, '\[e2 10', "$$ M)WT )RB(YM W/$NYM =+\tE(CAKO/SIOI TESSARA/KONTA O)KTW/ [e2.10]"),
        ('', 772, 'SAS 3', ")$R H$BY(/W\t{...O(RKISQEI\S}{d} E)PIORKH/SAS #"),
        ('', 4525, 'O.I\(', "BNY GLWT/)\tOI( E)K TH=S AI)XMALWSI/AS [e6.16]"), # remove unknown char
        ('27.Sirach.par', 4843, '{\.\.}', '[..]\tA)PO\\'),
        ('', 3697, '\s\s\s\s\s', "#\tA(MARTWLOU=} [7]}"), 
        ('', 16898, ' no id\.', "NSH[..] 4\t--- ''<c - no id.>"), # put weird note in brackets
        ('', 14099, '{\.\.\.\)', "<<KY>> 12\t{...}"),
        ('11.1Sam.par', 2096, 'O\t', "--+ '' =KPWT\tOI( KARPOI\\"),
        ('', 2097, 'T\t', "--+ '' =;YD/YW\tTW=N XEIRW=N AU)TOU="),
        ('12.2Sam.par', 8592, 'EI\)S\)', "H/&DH =;H/Y(R\t{..pEI)S} TO\\N DRUMO\\N"),
        ('13.1Kings.par', 15936, 'EI\)S}\t', "W/YBW)\tKAI\ EI)SH=LQEN {...EI)S}"),
        ('', 2987, 'GY', "MCRYM\tAI)GU/PTOU [2.46k,10.26a]"),
        ('14.2Kings.par', 4735, '{c}\? ', "YNHG\tE)GE/NETO {c?H)=GEN}"),
        ('40.Isaiah.par', 1855, 'E\t', "B/$LKT =;M$LKT <q1a>\tE)KPE/SH|"),
        ('', 11657, '_', "B/M(LWT\t--- ?"),
        ('', 18586, '\.\.\.TO', "W/L/QDW$\tTO\ A(/GION {d} {..^KAI\ DIA\}{..^TO|N"),
        ('', 11769, '=XWHa,XYY', "YXYW =@XWHa =@XYY\tA)NHGGE/LH {d} {...KAI\ E)CHGEIRA/S}"),
        ('26.Job.par', 2245, 'OU\)}\t', "W/L)\t{..^OU)}DE\\"),
        ('', 2063, '=a', "$DY =@$/DYa\tO( TA\ PA/NTA POIH/SAS"),
        ('', 7441, '{#}', "YMYN\tDECIW=N {---%}"),
        ('', 7927, 'S\.\.\^', "W/T$Q\tEI) DE\ KAI\ {..^EPIQEI\S}{..^E)FI/LHSA}"),
        ('', 7615, '{c\?}', "XMH =?@XSM,@ZMMa [[30:11]]\tFIMOU= {c?QUMOU=}"),
        ('', 7535, 'KRATAI', "B/(CM\t{..^KRATAIA=|}"),
        ('44.Ezekiel.par', 471, 'OU=} MDBR', "MDBR =v\t{...?AU)TOU=} LALOU=NTOS"),
        ('', 18162, '<42\.9\)', "--+ =;L/HNH <42.9>\tDI' AU)TW=N"),
        ('', 20424, '\s\s\s\s\s', "NTNW #\tDE/DONTAI #"),
        ('', 16686, r'XEIR\\', "^^^ ^ =W/B/YD/W\tKAI\ E)N TH=| XEI\R AU)TOU="),
        ('', 8218, '\+RAUS\+', "L/MWG =%vap\tQRAUSQH=|"),
        ('16.2Chron.par', 10095, '\t---$', "MLK\t--- ''"),
        ('', 10096, '\t---$', "B/YRW$LM\t--- ''"),
        ('', 1522, 'W:', "L/YHWH\tTW=| KURI/W|"),
        ('', 3575, '-\.-', ''), # erase redundant line
        ('', 4093, '{TOU', "W/B/BNYMN\tKAI\ {cTOU=} BENIAMIN"),
        ('02.Exodus.par', 18838, '<40\.9}', '--+ '' {x} =;B/W <40.9>\tAU)TH=S'), 
        ('', 3197, '\s\s\s\s\s', "--+ =HW) <sp>\tAU)TO\S"), 
        ('04.Num.par', 7479, '<de1\.39\)', "--+ '' =;)$R <de1.39>\tO(/SOI"),
        ('20.Psalms.par', 21382, '{\.1\.d', "W/M/PZ\tKAI\ {..dU(PE\R} TOPA/ZION [118.127]"),
        ('', 8991, '\*YCPYNW\*', "**YCPYNW *YCPWNW\tKAI\ KATAKRU/YOUSIN [55.7]"),
        ('', 21484, 'Y\*', "CR/Y\tOI( E)XQROI/ MOU [118.139]"),
        ('', 7997, 'PROS/', "W/)L\tKAI\ {..dPRO/S} [49.4]"),
        ('', 8968, r'TOUS\\', "DBR/W\tTOU\S LO/GOUS MOU [55.5]"),
        ('23.Prov.par', 89, 'c18\.7\s', 'W/(NQYM <ju8.26 ge41.42 c18.7>\tKAI\ KLOIO\\N XRU/SEON'),
        ('', 3274, 'ER\t', "{...}\tW(/SPER"),
        ('', 3317, '{c} ', "YQB/HW =?@$BQa\tU(POLI/POITO {cU(POLH/NION} AU)TO\\N"),
        ('', 3482, '\^EN\)', "MCWD =MCWR .dr\t{..^E)N} O)XURW/MASIN}"),
        ('', 7090, r'G\\AR', "KY\tGA\R"),
        ('', 8517, r'A\|\(', "$)WL\tA(/|DHS"),
        ('03.Lev.par', 6866, '<sp\^\s', "--+ '' =;B/W <nu19.13> <sp^> #\tE)N AU)TW=|"),
        ('', 12382, '{\.\.\.L\)\t', "W/PSL {...L)}\tOU)DE\ GLUPTA\\"),
        ('41.Jer.par', 4751, '--\t', "H(D {!}-\t--- ''"),
        ('', 4752, '--\t', "H(DTY {!}-\t--- ''"),
        ('05.Deut.par', 11173, 'KI.*\t', "--+ '' =;KY <24.22>\tO(/TI"),
        ('', 13270, 'Deut 28:65', 'Deut 28:64'), 
        ('', 13293, '\s\*', "^ W/)BN\t^^^\n\nDeut 28:65"),
        ('', 2297, 'Deut 4:26', 'Deut 4:25'),
        ('', 2316, '\(YD', "\nDeut 4:26\nH(YDTY\tDIAMARTU/ROMAI"),
        ('08.JudgesB.par', 8041, r'N\.\.\.\)T', 'W/TY$N/HW =W/TY$N {...)T $M$WN}\tKAI\ E)KOI/MISEN {...TO\\N SAMYWN}'),
        ('', 7568, '=@a\+', "=@+R)a\tE)KRERIMME/NHN"),
        ('', 8151, ' %vpa', "W/YCXQ =%vpa {d}\tKAI\ E)/PAIZEN {d} {...KAI\ E)RRA/PIZON}"),
        ('30.Amos.par', 603, '\[c', "B/)RC\tTH=S ---  {cGH=S}"),
        ('', 751, '\[c', ")$H\tGUMNAI\ {cGUNAI=KES}"),
        ('18.Esther.par', 4779, 'TH=!', "--+ ''\tTH=| TESSARESKAIDEKA/TH|"),
        ('19.Neh.par', 1663, 'MEneN', "K/H/YWM\tW(S SH/MERON"),
        ('', 3198, '{c\?}', "$(R =?(YR\tTH=S PO/LEWS {c?PU/LHS}"),
        ('', 166, '{\*\*\t', "*W/HBW)TY/M **W/HBY)WTY/M {**}\tKAI\ EI)SA/CW AU)TOU\S"),
        ('45.DanielOG.par', 7333, '{\?}', "YMYM\t--- <?>"),
        ('', 2883, 'Q/Q', "(L M$KB/Y ,,a\tE)KA/QEUDON [10]"),
        ('43.Lam.par', 1587, 'A \)', "+M)\tA)KAQA/RTWN"),
    ]

    report('\napplying bulk manual edits...\n')

    file = ''
    for edit in edits:

        # unpack data
        file = edit[0] or file
        ln, re_confirm, redaction = edit[1:]
        old_line = file2lines[file][ln]

        # confirm and apply changes, give reports throughout
        if re.findall(re_confirm, old_line):
            file2lines[file][ln] = redaction
            report(f'correction for {file} line {ln}:')
            report(f'\tOLD: {old_line}')
            report(f'\tNEW: {redaction}')
            n_edits += 1
        else:
            if debug:
                raise Exception(f'FOLLOWING EDIT UNCONFIRMED: {edit} at {old_line}')
            report(f'**WARNING: THE FOLLOWING EDIT WAS NOT CONFIRMED**:')
            report(f'\tTARGET: {old_line}')
            report(f'\tEDIT: {edit}')

    # -- Other Edits --

    report('\nApplying corrections to orphaned / corrupt lines...\n')

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
    
    # first check that the edit still applies to current file
    exod = file2lines['02.Exodus.par']
    if exod[16284] == 'Exod 1:10':
        report('patching corrupt lines 16283-16289 in 02.Exodus.par...')
        fixed_lines = exod[:16283] + [exod[16285]] + exod[16288:]
        file2lines['02.Exodus.par'] = fixed_lines
        report('\tdone')
        n_edits += 1
    else:
        if debug:
            raise Exception('EXODUS CORRUPTION REPAIR SKIPPED!')
        report('**WARNING: SKIPPING EXODUS CORRUPTION REPAIR DUE TO CHANGED LINE NUMBERS; see code')

    # orphaned lines are cases where parts of a line are inexplicably broken off
    # these are handled in bulk in a loop further below; but Ps 68:31 contains a 
    # special case with 2 orphaned lines in a row
    # to prevent need for recursive algorith, we just fix it manually
    # we do it here to avoid needed to adjust indices after the correction
    # listed subsequent to this one
    pss = file2lines['20.Psalms.par']
    if pss[10848] == 'MTR':
        report('patching double-orphaned lines in lines 10849-10851 of 20.Psalms.par (Ps 68:31)')
        ps68_31_patch = [pss[10848] + pss[10849] + pss[10850]]
        file2lines['20.Psalms.par'] = pss[:10848] + ps68_31_patch + pss[10851:] 
        report('\tdone')
        n_edits += 1
    else:
        if debug:
            raise Exception('PSALMS ORPHAN REPAIR SKIPPED!')
        report('**WARNING: SKIPPING PSALMS ORPHAN REPAIR DUE TO CHANGED LINE NUMBERS; see code')

    # An identical corruption to the one discussed above in Exodus 35:15
    # likewise in 20.Psalms.par lines 2455-2459
    pss = file2lines['20.Psalms.par'] # rename to resume corrected data
    if pss[2459] == 'Ps 18:40':
        report('patching corrupt lines 2457-2461 in 20.Psalms.par...')
        fixed_lines = pss[:2456] + [pss[2457]] + pss[2460:]
        file2lines['20.Psalms.par'] = fixed_lines
        report('\tdone')
        n_edits += 1
    else:
        if debug:
            raise Exception('PSALMS ORPHAN REPAIR 2 SKIPPED!')
        report('**WARNING: SKIPPING PSALMS ORPHAN REPAIR #2 DUE TO CHANGED LINE NUMBERS; see code')

    # There is repeated material in Ezek, lines 20600-20607 (Ezek 47:20)
    # We repair that here
    ezek = file2lines['44.Ezekiel.par']
    if '     ' in ezek[20599]:
        ezek[20599] = "--+ =:XMT\tHMAQ"
        fix = ezek[:20600] + ezek[20607:]
        file2lines['44.Ezekiel.par'] = fix
        n_edits += 1
    else:
        if debug:
            raise Exception('EZEKIEL DUPLICATE CONTENT REPAIR SKIPPED!')
        report('**WARNING: EZEKIEL DUPLICATE CONTENT REPAIR SKIPPED; see code') 

    # -- Repair Orphaned Lines --

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

    current_verse = None
    for file, lines in file2lines.items():

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
                n_edits += 1

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
        file2lines[file] = filtered_lines

    report('\tdone')

    # -- Bulk Normalizations -- 
    
    # changes which need to be effected systematically are loaded into tuples:
    # (regex, replace)
    # the changes are enacted with regex substitutions
    # not all of these are stricly errors (though they may be), there 
    # are numerous cases of normalizations applied to bring idiosyncratic
    # patterns in line with the majority

    # NB that the order of some changes matters, since some patterns are 
    # dependent on other idiosyncracies being fixed already
    normalizations = [
        ('~', '^'),
        ('----\+---', "--- ''"), # see 2 Chr 27:8
        ("---\+", "--+"),
        ("<([^\s>]*)(\s)(?!.*[>#])", '<\g<1>>\g<2>'), # numerous unclosed brackets

        # NB: on below, cases of `{..`; some cases may be ambiguous whether they should be 
        # {... or {..^ However, it is the stated preference of the docs that 
        # during encoding {... is to be preferred (1986:7.6)
        # and it also seems that several of the examples have a majority 
        # preference of {... over {..^; thus we go with the former
        ('{\.\.(?![.^a-z])', '{...'),
        ('\.\.\.\.', '...'),
        ('\(!\)', '{!}'), # (!) to {i}, inf. abs.
        ('(?<![-*])\-\+', '--+'), # -+ to --+
        ('A(?=.*\t)', ''), # vowels in the Hebrew column, replace with nothing
        ('=&p', '=%p'), # =&p typo for =%p, preposition differences
        ('(?<!-)--(?![-+])', '---'), # -- to ---
        ('=a', '=@a'),

        # NB order of this block matters, to ensure space to left of =
        ('=%p=', '=%p-'),
        ('([:;])=', '=\g<1>'), # e.g. := to =:
        ('([^A-Z\/()\s|{}])=', '\g<1> ='), # ensure space to left of = (col.B marker)
    
        # this is case of ellision with interruption
        # it would be more consistent to code it as a separate {...} remark
        # so we close the previous brace and adda second
        ('(?<![{\[])\.\.\.(?![}\]])', '}{...'),
        
        ('=%pa', '=%vpa'),
        ('-%vap', '=%vap'),
        ('{\.\.\.r', '{..r'),
        ('=p(?=[\s-])', '=%p'),
        ('<Sp>', '<sp>'),
        ('=vpa', '=%vpa'),
        ('{d}%p(\+?)', '%p\g<1> {d}'),
        ('\+;', '=;'),
        
        ('=\?:', '=:?'),
        ('={d};', '=;{d}'),

        ('=p%([-+\s])', '=%p\g<1>'),
        ('{d\t', '{d}\t'),
        ('{15{', '{15}'),
        ('\(\?5\)', '{?5}'), 
        ('\[\.\.\.\]', '[..]'),
        ('{(\d+)(\s)', '{\g<1>}\g<2>'),
        ('(\s)(\d+)}', '\g<1>{\g<2>}'),
        ('=%\?p(-?)', '=%p\g<1>?'),
        (' ([a-z][a-z]) (?=.*\t)', ' .\g<1> '),
        ('\(\.\.', '{..'),
        (r'\\(?=.*\t)', '/'),

        # order of block matters here
        ('\[([a-zA-Z])}', '{\g<1>}'),
        ('\[([\d.a-z]+)(?!.*\])', '[\g<1>]'),
          
        ('\s\s\s\s+', ' '),
        ('{\.\.\.\^', '{..^'),
        ('{\.\.\^\.', '{..^'),
        ('{\.\.\.([a-z]+)', '{..\g<1>'),
        ('{t\.}', '{t}'),
        ('<t\?>', '{t?}'),
        ('(\s)\?--\+(\s)', '\g<1>--+?\g<2>'),

        # move question marks contained in brackets
        # to the end of the brackets; this normalizes the `?`
        # and allows us to treat them as external decorators
        # rather than allowing them to interrupt a symbol
        (r"{([^}]*)(\?\??)(.*?)}", "{\g<1>\g<3>}\g<2>"),

        # normalize verse cross references in Hebrew portion
        #('\[\[(.*[a-zA-Z]+.*\d\..*)\]\](?=.*\t)', '<\g<1>>'),
        (r"\[\[(.+?)\]\](?=.*\t)", "<\g<1>>"),
        (r"{dt}", "{d}{t}"),
    
        # move `?` to end of etymological exegesis symbol
        (r"=@\?(\S*)a", "=@\g<1>a?"),

        # close up unclosed curly brackets
        (r"{([^\[}#]+)( +|$)(?!.*[}#])", "{\g<1>}\g<2>"),

        (r"\^\^\^ \^ ''", "^^^ ^"),
        (r"=([A-Z()/&$+]+)a", "=@\g<1>a"),
    
        # change brackets of cross references in Hebrew portion to <>
        # where <...> represents a 'note'
        ("\[([^\]]*?\d[\]]*?)\](?=.*\t)", "<\g<1>>"),

        # patch misplaced accents
        (r"(\t.*)(\s)([()])(.)", "\g<1>\g<2>\g<4>\g<3>"),
        (r"(\t.*)=\)", "\g<1>)="),
        (r"\|=", "=|"),
        (r"\|\)", ")|"),
        (r"TO\|N", r"TO\\N"),
        (r"KAI\|", r"KAI\\"),
        (r"I\(MAT/TIA", "I(MA/TIA"),
        (r"ZN=\|", "ZH=|"),
        (r"H\)R=TAI", "H)=RTAI"),
        (r"OY\)K", "OU)K"),
        (r"EC/NOIS", "CE/NOIS"),
        (r"TH=/S", "TH=S"),
    ]

    report('\nMaking various bulk regex normalizations...\n')

    for search, replace in normalizations:

        report(f'---- applying pattern `{search}` with replace `{replace}` ----')
        search = re.compile(search) # compile for efficiency
        pattern_successful = False

        for file, lines in file2lines.items():
        
            new_lines = []
            curr_verse = ''

            for i,line in enumerate(lines):
                
                # track passages for reporting since line numbers have already changed
                if ref_string.match(line):
                    curr_verse = line

                # apply substitutions
                if search.findall(line):
                    redaction = search.sub(replace, line)
                    new_lines.append(redaction)
                    report(f'  in {file} in {curr_verse}:')
                    report(f'\tOLD: {line}')
                    report(f'\tNEW: {redaction}')
                    pattern_successful = True   
                    n_edits += 1    
                
                # else keep line the same
                else:
                    new_lines.append(line)

            file2lines[file] = new_lines

        if not pattern_successful:
            if debug:
                raise Exception(f'PATTERN NOT FOUND: {search}')
            else:
                report(f'WARNING, PATTERN NOT FOUND: {search}')

    # export the corrected files
    report(f'\nwriting patched data to {output_dir}')
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    for file, lines in file2lines.items():
        text = '\n'.join(lines)
        file_path = output_dir.joinpath(file)
        file_path.write_text(text)

    # write changes to a log file
    log_path = output_dir.joinpath('log.txt')
    log_path.write_text(log)

    report('\nDONE with all patches!')
    report(f'\ttotal edits: {n_edits}')
