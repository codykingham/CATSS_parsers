# compiled patterns for searching the CATSS database

import regex

# identify verse reference strings
ref_string = regex.compile(r'^[A-Za-z1-9/]+ \d+:?\d*$')

# identify Hebrew transcription characters
hchars = r')BGDHWZX+YKLMNS(PCQR&$T/'

# recognize Greek letters
gchars = r"ABGDEVZHQIKLMNCOPRSJTUFXYW()|/\\=+*'\-"

# strings to discard if all other matches fail
discard = r"\s+|="

# The following data contains patterns for capturing
# and processing text critical sigla
# the tuples contain the following content:
# (regex, kind, tag, description, indices [optional])
# kind refers to different behavior of markup:
# • con - apply the tag to all text in a given context
# • sub - a substitution which represents a missing text element
# • cap - a tag which captures text elements in its vicinity for tagging
# indices is a dict which refers to capture group indices;
# the 'txt' key is reserved as special for text elements;
# all other tags are used for formatting tag strings with .format().

# identify text-critical sigla common to all columns
common_tc = [
    (
        r"([^\s?]+)(\?+)(\s+|$)",
        "cap",
        "{tag}",
        "indicates doubt on the word or interpretation of the translation strategy",
        {'txt':0, 'tag':1},
    ),
    (
        r"({.*?})(\?+)",
        "cap",
        "{tag}",
        "indicates doubt on the word or interpretation of the translation strategy",
        {'txt':0, 'tag':1},
    ),
    (
        r"(?<= )(\?+)([^\s?]+)",
        "cap",
        "{tag}",
        "indicates doubt on the word or interpretation of the translation strategy",
        {'txt': 1, 'tag': 0},
    ),
    (
        r"(?<= )(\?+)({.*?})",
        "cap",
        "{tag}",
        "indicates doubt on the word or interpretation of the translation strategy",
        {'txt': 1, 'tag': 0},
    ),
    (
        r"(--\+\s?(''|{x})?)", 
        'con', 
        '{tag}', 
        'In column A of the Hebrew: element added in the Greek', 
        {'tag':0},
    ),
    (
        r"(---\s?(''|{x})?)", 
        'con', 
        '{tag}', 
        'apparent minus in the MT over against the Greek', 
        {'tag':0},
    ),
    (
        "{x}",
        "con",
        "app-/+",
        "apparent minus/plus",
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
        'trans',
        'transposition; equivalent reflected elsewhere in the text', 
        {'txt':0},
    ),
    (
        r"(\^\^\^ \^|\^ \^\^\^)", 
        'sub', 
        '{tag}', 
        'equivalent of the Hebrew / Greek word(s) occurs elsewhere in verse/context', 
        {'tag':0},
    ),
    (
        r"(\^\^\^)",
        'sub',
        '{tag}',
        'equivalent of the Hebrew / Greem word(s) occurs elsewhere',
        {'tag':0},
    ),
    (
        r"{\.\.p?\^(.+?)}",
        "cap",
        "^s",
        "stylistic or grammatical transposition of elements",
        {'txt': 0},
    ),
    (
        r"([^\^\s]*) +(?=\??\^)",
        "cap",
        ".^",
        "elements before a transposition",
        {'txt':0},
    ),
    (
        r"(?<!\^)\^ *({.*?}[a-z+\-]*)",
        "cap",
        "^.",
        "elements after a transposition",
        {'txt':0},
    ),
    (
        r"(?<!\^)\^ *([^\^\s{]*)",
        "cap",
        "^.",
        "elements after a transposition",
        {'txt':0},
    ),
    (
        r"<(.*?)>",
        "con",
        "{note}",
        "contains a note (?)",
        {'note': 0},
    ),
    (
        r"({.*?}|[^\s]+) *(?=\??\{d\})",
        "cap",
        ".doub",
        "elements before a doublet",
        {'txt':0},
    ),
    (
        r"=?\{d\}\??\s*({.*?}|[^\s]*)",
        "cap",
        "doub.",
        "elements after a doublet",
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
        "{t}",
        "con",
        "transl",
        "Transliterated Hebrew word",
        {},
    ),
    (
        "{p}\+?",
        "con",
        "gprev",
        "Greek preverb representing Hebrew preposition",
        {},
    ),
    (
        r"({\+})",
        "con",
        "! {{+}}",
        "UNKNOWN",
        {},
    ),
    (
        r"(\?+)",
        "con",
        "{tag}",
        "indicates doubt on the word or interpretation of the translation strategy",
        {'tag':0},
    ),
    (
        r"{\.\.d(.*?)}",
        "cap",
        "distr",
        "distributive rendering: occurring once in translation but referring to more than one Hebrew ord",
        {'txt':0},
    ),

]

# order matters: more complex patterns first
heb_tc = [
    # pattern, kind, NEW code, description, indicies (optional)
   
    (
        r",,a", 
        'con', 
        'ARA', 
        'Word included in one of the Aramaic sections', 
        {},
    ),
   (
        r"=?;(.*)", 
        'cap', 
        'cret', 
        'retroversion in Hebrew con.b based on immediate / remote context', 
        {'txt':0},
    ),
   (
        fr"\*\*([{hchars}]+)",
        'cap',
        'qere',
        'Hebrew qere reading',
        {'txt':0},
    ),
    (
        fr"\*([{hchars}]+)",
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
        fr"=?:([{hchars} ?]*)",
        'cap',
        'rprn',
        'introduces reconstructed proper noun',
        {'txt':0},
    ),
    (
        fr"=?@([{hchars} ,]*?)a",
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
        r"=?%p([-+])?",
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
        r"{\.\.r(.*?)}",
        "cap",
        "repeat",
        "elements repeated in the translation",
        {'txt':0},
    ),
    (
        r"=?{!}([a-z\-+]*)",
        "con",
        "infa.{tag}",
        "infinitive absolute with additional data",
        {'tag':0},
    ),
    (
        r"\.m(\s+|$)",
        "con",
        "metat",
        "metathesis of letters",
        {},
    ),
    (
        r"\.z(\s+|$)",
        "con",
        "abbr",
        "possible abbreviation",
        {},
    ),
    (
        r"\.s(\s+|$)",
        "con",
        "sep",
        "one word of MT separated into two or more words in vorlage of LXX",
        {},
    ),
    (
        r"\.j(\s+|$)",
        "con",
        "join",
        "two words of MT joined into one word in the vorlage of LXX",
        {},
    ),
    (
        r"\.w(\s+|$)",
        "con",
        "wordd",
        "different word division reflected in the vorlage of LXX",
        {},
    ),
    (
        r"\.([a-z+\-$&()][a-z+\-$&()]?[a-z+\-$&()])",
        "con",
        "int.{cons}",
        "interchange of cited letters",
        {'cons':0},
    ),
    (
        r"(=|^)\+(\s+|$)",
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
        r",([^,<]*)",
        "cap",
        "OR",
        "introduces a second reconstruction",
        {'txt':0},
    ),
   ( # NB: this pattern will only be selected after <.+> pattern
        ">",
        "con",
        "! >",
        "UNKNOWN",
        {},
    ),
]

# recognize Greek text-critical sigla
greek_tc = [
    (
        "{---%}",
        "con",
        "ast",
        "asterized passage in Job",
        {},
    ),
    (
        "{c(.*?)}",
        "cap",
        "corr",
        "indicates a correction to the Greek text",
        {'txt':0},
    ),
    (
        "\{s\}",
        "con",
        "hsupr",
        "Hebrew MN reflected by Greek comparative or superlative",
        {},
    ),
    (
        "\[\[(.*\d+.*)\]\]",
        "con",
        "{tag}",
        "chapter & verse difference from Hebrew",
        {'tag': 0},
    ),
    (
        "\[(.*\d+.*)\]",
        "con",
        "{tag}",
        "(chapter &) verse difference from Hebrew",
        {'tag': 0},
    ),
    (
        "{g(.*?)}",
        "cap",
        "diffg",
        "difference between Rahlfs and Göttingen edition",
        {'txt':0},
    ),
    (
        "{pm}",
        "con",
        "! {{pm}}",
        "UNKNOWN",
        {},
    ),
]

# recognize text-critical characters in extra-biblical books
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
        '! <<...>>',
        'UNKNOWN; possibly reconstructed text',
        {'txt':0},
    ),
    (
        r"<(.+?)>",
        'cap',
        '! <...>',
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
    ),
    (
        "(?<!')'(?!')",
        "con",
        "! '",
        "UNKNOWN; possibly a character aleph?",
        {},
    ),
    (
        "=s",
        "con",
        "! =s",
        "UNKNOWN",
        {},
    )
]
