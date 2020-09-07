# Interepreting the Parallel Database
*Cody Kingham, University of Cambridge*

It doesn't appear to me that the CATSS parallel database has ever been
processed in the open. The programs used to parse the database are not
provided online. It appears that Eliran Wong had the goal of linking the
CATSS dataset with the ETCBC database: https://github.com/eliranwong/LXX-Rahlfs-1935/blob/master/README.md#lxx-rahlfs-1935-biblebentocom 
But it doesn't appear as if he's done that yet. The Open Scriptures' Septuagint project
has only published scripts to handle the morphological text: https://github.com/openscriptures/GreekResources 

After having my own hand at parsing these files, the reason for the oversight
seems to be that the format is complicated and difficult to understand. 
So this readme is my attempt to reconstruct a method by which
the parallel files might be parsed. 

The parallel dataset has its own readme file (1991), which can be accessed here:
http://ccat.sas.upenn.edu/gopher/text/religion/biblical/parallel/00.ReadReParallel.txt

I won't reiterate the transcriptions and sigla discussed there, except to point out cases
where the documentation is either outdated or falls short. 

There is a fuller form of documentation published in 1986 as Emanuel Tov, *A Computerized Data Base for Septuagint Studies:  The Parallel Aligned Text of the Greek and Hebrew Bible*, Computer
Assisted Tools for Septuagint Studies (CATSS) Volume 2, Stellenbosch: Journal of Northwest Semitic Languages, 1986). Emanuel Tov has provided this publication as a PDF on academia.edu:
https://www.academia.edu/28953727/B5_A_Computerized_Data_Base_for_Septuagint_Studies_The_Parallel_Aligned_Text_of_the_Greek_and_Hebrew_Bible_CATSS_Volume_2_JNSLSup_1_Stellenbosch_1986_xviii_144_pp

I'll draw from both of these sources as I try to trace out my own understanding of
this format. I'll refer to them as 1991 and 1986, respectively.

## Sample of `01.Genesis.par`: 

```
Gen 1:1
B/R)$YT E)N A)RXH=|
BR) E)POI/HSEN
)LHYM   O( QEO\S 
)T H/$MYM   TO\N OU)RANO\N
W/)T H/)RC  KAI\ TH\N GH=N

Gen 1:2
W/H/)RC H( ^ DE\ GH=
HYTH    H)=N  
THW A)O/RATOS
W/BHW   KAI\ A)KATASKEU/ASTOS
W/X$K   KAI\ SKO/TOS
(L PNY  E)PA/NW
THWM    TH=S A)BU/SSOU
W/RWX   KAI\ PNEU=MA
)LHYM   QEOU= 
MRXPT   E)PEFE/RETO
(L PNY  E)PA/NW
H/MYM   TOU= U(/DATOS

Gen 1:3
W/Y)MR  KAI\ EI)=PEN
)LHYM   O( QEO/S 
YHY GENHQH/TW
)WR FW=S
W/YHY   KAI\ E)GE/NETO
)WR FW=S
``` 

# General Layout

## Verses
The online dump of the database consists of verses and 
their lines, delineated by a reference string, a set of 
data lines, and double newline characters `\n\n` at the
end of the verse.

## Lines
Each individual line breaks down into 2-3 columns:
> Each line of the parallel files shows equivalent elements of the MT
> and the LXX. Occasionally, the Hebrew column splits into two columns:
> column a and column b. (1991)

On columns a and b for the Hebrew text:
> Column a of the Hebrew records all elements of MT as formal
> equivalents of the LXX ... Column b contains a selection of retroverted readings, 
> presumably found in the parent text of the LXX. (1991)

The line itself contains either 1) original language text for both the Hebrew
and the Greek text, written in an ASCII transcription format (see 1991), 
2) or text critical notes / sigla (1991). In most cases, the original text 
can be retrieved from the verse by stripping out the text critical symbols (1986: 21). 

*Useful generalization: It appears that UPPERCASE is reserved for original language text and all
text-critical sigla are either lowercase or other symbols.*

## Discontinuous Lines
There is some significant complexity added by the fact that some lines are discontinuous:

1) marked with # - long lines are broken up using # at end and # at beginning 
of its adjacent continuation:   

e.g. from Gen 15:11
```
H/PGRYM TA\ SW/MATA {d} TA\ DIXOTOMH/MATA #
#   AU)TW=N
```

[unclear: not all # symbol]


## Order of the Text

The order of the text in the database attempts to follow the printed text
where possible. However, only the Hebrew text order is reliably unaltered:

> The running text of MT thus has never been touched, while that of the LXX has been touched in the case of global differences between the two texts. (1986: 21). 

[Question: which passages in particular have been altered?]


