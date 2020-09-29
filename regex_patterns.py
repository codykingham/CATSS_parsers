# compiled patterns for searching the CATSS database

import regex

ref_string = regex.compile(r'^[A-Za-z1-9/]+ \d+:?\d*$')

# Hebrew characters
hchars = r')BGDHWZX+YKLMNS(PCQR&$T/'

extra_bib_tc = [
    (
        r"(.*)\s*(\d)+\s*", 
        'att', 
        'MNS.{tag}', 
        'manuscript containing Hebrew text of extrabiblical passages',
        {'txt': 0, 'tag': 1},
    ),
    (
        r"\[\.\.\]", 
        'sub', 
        'lac', 
        'lacuna reflected in manuscript of extrabiblical passage', 
        {},
    ),
    (
        r"{([\d?]+)}",
        'sub',
        'lac.{tag}',
        'reports lacuna in listed manuscript of extrabiblical passage',
        {'tag':0},
    ),
    (
        r"\[.*?\]",
        'cap',
        'recst',
        'reconstruction of text from an extrabiblical passage',
        {'txt':0},
    ),
    (
        r"<<(.+?)>>",
        'cap',
        '?',
        'UNKNOWN; possibly reconstructed text',
        {'txt':0},
    ),
    (
        r"<(.+?)>",
        'cap',
        '?',
        'UNKNOWN; possibly reconstructed text',
        {'txt':0},
    ),
    (
        r">(\d+)",
        "con",
        "om.{manu}",
        "reading is omitted in cited manuscript",
        {'manu':0},
    ),
    (
        fr"([{hchars}])\*",
        "cap",
        "doubt",
        "uncertain or fragmentary letter",
        {'txt':0},
    ),
    (
        fr"(\*-[{hchars}])\*",
        "cap",
        "doubt",
        "reading of the character is in doubt",
        {'txt':0},
    )
]

# order matters: more complex patterns first
hb_tc = [
    # pattern, kind, NEW code, description, indicies (optional)
    (
        r"--\+\s?(''|{x})?", 
        'con', 
        'LXX+', 
        'In column A of the Hebrew: element added in the Greek', 
        {},
    ),
    (
        r"---\s?(''|{x})?", 
        'con', 
        'MT-', 
        'apparent minus in the MT over against the Greek', 
        {},
    ),
    (
        r",,a", 
        'con', 
        'ARA', 
        'Word included in one of the Aramaic sections', 
        {},
    ),
    (
        r"{\.\.\.}", 
        'sub', 
        'trans', 
        'transposition; equivalent reflected elsewhere in the text', 
        {},
    ),
    (
        r"{\.\.\.(.+?)}", 
        'cap', 
        'transposition; equivalent reflected elsewhere in the text', 
        {'txt':0},
    ),
    (
        r"=?;", 
        'con', 
        'cret', 
        'retroversion in Hebrew con.b based on immediate / remote context', 
        {},
    ),
    (
        r"\^\^\^ \^|\^ \^\^\^", 
        'con', 
        'trans', 
        'equivalent of the Hebrew / Greek word(s) occurrs elsewhere in verse/context', 
        {},
    ),
    (
        r"{\.\.\^(.+?)}",
        "cap",
        "strans",
        "stylistic or grammatical transposition of elements",
        {'txt': 0},
    ),
    (
        r"([^\^]+?) (?=\^)",
        "cap",
        "<trans",
        "elements before a transposition",
        {'txt':0},
    ),
    (
        r" \^ ([^\^]+?)",
        "cap",
        ">trans",
        "elements after a transposition",
        {'txt':0},
    ),
    (
        fr"(\*\*([{hchars}]+)",
        'cap',
        'qere',
        'Hebrew qere reading',
        {'txt':0},
    ),
    (
        fr"(\\*([{hchars}]+)",
        'cap',
        'ketiv', 
        'Hebrew ketiv reading', 
        {'txt':0},
    ),
    (
        r"{\*}",
        "con",
        "gketiv",
        "Greek agrees with the ketiv reading",
        {},
    ),
    (
        r"{\*\*}",
        "con",
        "gqere",
        "Greek agrees with the qere reading",
        {},
    ),
    (
        fr"=?:([{hchars} ?]+)",
        'cap',
        'rprn',
        'introduces reconstructed proper noun',
        {'txt':0},
    ),
    (
        fr"=?@([{hchars} ?,]*?)a",
        'cap', 
        'eea',
        'introduces etymological exegesis based on Aramaic',
        {'txt': 0},
    ),
    (
        fr"=?@([{hchars} ?,]*)",
        'cap', 
        'eex',
        'introduces etymological exegesis',
        {'txt': 0},
    ),
    (
        r"<.*?>",
        "cap",
        "note",
        "contains a note (?)",
        {'txt': 0},
    ),
    (
        r"=?%p([-+])",
        "con",
        "prep{tag}",
        "difference (±) of a preposition or particle",
        {'tag': 0},
    ),
    (
        r"=?%vap",
        "con",
        "vap",
        "change from active to passive verb form",
        {},
    ),
    (
        r"=?%vpa",
        "con",
        "vpa",
        "change from passive to active verb form",
        {},
    ),
    (
        r"(.*?)(?==?\{d\})",
        "cap",
        "<doub",
        "elements before a doublet",
        {'txt':0},
    ),
    (
        r"=?\{d\}(.*)",
        "cap",
        ">doub",
        "elements after a doublet",
        {'txt':0},
    ),
    (
        r"{\.\.r(.*?)}",
        "cap",
        "repeat",
        "elements repeated in the translation",
        {'txt':0},
    ),
    (
        r"{\.\.p(.*?)}",
        "cap",
        "prept+",
        "preposition added in LXX in accordance with Greek rules/translational habits",
        {'txt':0},
    ),
    (
        r"{\.\.d(.*?)}",
        "cap",
        "distr",
        "distributive rendering: occurring once in translation but referring to more than one Hebrew ord",
        {'txt':0},
    ),
    (
        r"=?{!}[a-z-+]*",
        "con",
        "infa",
        "infinitive absolute with additional data",
        {},
    ),
    (
        r"\.m(?=\s|$)",
        "con",
        "metat",
        "metathesis of letters",
        {},
    ),
    (
        r"\.z(?=\s|$)",
        "con",
        "abbr",
        "possible abbreviation",
        {},
    ),
    (
        r"\.s(?=\s|$)",
        "con",
        "sep",
        "one word of MT separated into two or more words in vorlage of LXX",
        {},
    ),
    (
        r"\.j(?=\s|$)",
        "con",
        "join",
        "two words of MT joined into one word in the vorlage of LXX",
        {},
    ),
    (
        r"\.w(?=\s|$)",
        "con",
        "wordd",
        "different word division reflected in the vorlage of LXX",
        {},
    ),
    (
        r"\.([a-z+\-$&][a-z+\-$&]?[a-z+\-$&])",
        "con",
        "int.{cons}",
        "interchange of cited letters",
        {'cons':0},
    ),
    (
        r"(=|^)\+(\s|$)",
        "con",
        "dnumb",
        "difference in numbers between MT and LXX",
        {},
    ),
    (
        r"=?vs",
        "con", 
        "voc",
        "indicates difference in vocalization (reading) regarding shin/sin",
        {},
    ),
    (
        r"=?v",
        "con", 
        "voc",
        "indicates difference in vocalization (reading)",
        {},
    ),
    (
        r"=?r",
        "con",
        "iretro",
        "incomplete retroversion",
        {},
    ),
    (
        r",([^,]*)",
        "cap",
        "",
        "",
        {'txt':0},
    ),
    (
        "{t}",
        "con",
        "transl",
        "Transliterated Hebrew word",
        {},
    )
    
]

# devise technique to handle question marks

gk_tc = [

]
