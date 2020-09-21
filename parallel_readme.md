# Interepreting the CATSS Parallel Database
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
https://www.academia.edu/28953727/B5_A_Computerized_Data_Base_for_Septuagint_Studies_The_Parallel_Aligned_Text_of_the_Greek_and_Hebrew_Bible_CATSS_Volume_2_JNSLSup_1_Stellenbosch_1986_xviii_144_pp . 

I'll draw from both of these sources as I try to trace out my own understanding of
this format. I'll refer to them as 1991 and 1986, respectively.

### Problems with documentation

There are numerous lacunae and typos in the two pieces of documentation. 

#### Outdated Sigla

The database dump as downloaded online has numerous incongruencies with 
the 1991 and 1986 documents.

##### transpositions (~)

In 1991, `~` and `~~~` are provided as the sigla used for transpositions. 
1986 presents these as `~` or `---` in the sigla appendix (pg. 14). 
But in the database as currently downloaded this is received as `^` and 
`^^^` respectively, with the exception of `31.Joel.par` and `32.Jonah.par` 
which confusingly still retain `~`. 

The 1986 sections dealing with transcriptions generally use `-` and `---` in the 
actual examples (see section 7.1f), but there are many typos and the text appears
to be a corrupt export of the original documentation (see especially top of pg. 45
in the PDF).

**NB that the regular sign of transpositions in the downloaded database
is one or three caret signs, i.e. ^ or ^^^**. Thus, everywhere in the documentation
that reads `~` should be interpreted as `^`.  

##### morphological separator (`\`)

According to 1991, the backslash (`\`) serves  as a morphological separator for, e.g.,
inseparable prepositions in Hebrew. But in the databse `/` is instead used for this purpose.

##### maqqeph (`-`)

1991 says that `-` is used in for maqqeph. But the online database uses whitespace instead 
to represent maqqeph.

##### shin/sin with `#`

1991 says a `#` can represent "sin/shin", but this is not used in the database. 
This character assignment conflicts with the alternative use of `#` to indicate
discontinuous lines.

#### Other changed symbols
|docs|actual| meaning |
|----| ---- |  ----   |
|`..a`|`,,a`|"word included in one of the Aramaic sections" |
|`{..}`|`[..]`|"lacuna in [manuscript]" (1991:123)" |


### Categories of Markup

The CATSS database is a kind of column-based, in-line markup. In the repo,
we want to change the markup to stand-off, which is more flexible. 

The markup patterns used implicitly modify a word or stretch of words. For 
instance, in the Greek column, words surrounded with `{..^}` are marked as 
a "stylistic or grammatical transposition". This notation can also be considered
as a "wrapper" markup, which modifies 1+ words. Another kind of markup can be 
seen in the `:=` which "introduces a reconstructed proper noun". This symbol
would thus seem to modify a string which follows it [question: can the string
have spaces? If so, where do we end this markup?]. This might be called an
"attached" markup pattern.

| category | e.g. | desc |
|  -----   |  --  | ---  |
| wrapper | `{..^}` | surrounds modified words |
| attacher | `:=` | adjacent to modified word(s) |
| columner | `''` | modifies a whole column of words | 
| place-holder | `{...}` | represents absent or transported words |  

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

# General Philosophy

The Hebrew text of BHS is the reference point for the alignments. This follows
a so-called "formal representation" (1986: 29-30) where, as far as possible,
one Greek word is juxtaposed against one Hebrew word, with the Hebrew text
considered the ground truth. So the BHS Hebrew text serves as the hypothetical 
text used for the LXX translation. Deviations from this text are specially 
indicated. (1986: 29-30).

[Comments: this strikes me as a very old-fashioned approach, and not very flexible
to handle the rich diversity of texts reflected between BHS and its witnesses and LXX
and its witnesses. What would a different approach look like?]

# Layout

## Verses
The online dump of the database consists of verses and 
their lines, delineated by a reference string, a set of 
data lines, and double newline characters `\n\n` at the
end of the verse.

Versification follows BHS, even where Rahlfs LXX disagrees
(1986:22). Where the Greek text has a different verse number,
it is indicated at the end of the Greek text in square 
brackets:

```
Gen 23:5
W/Y(NW  A)PEKRI/QHSAN ^ DE\ 
BNY OI( UI(OI\
XT  XET
)T )BRHM    PRO\S ABRAAM
L/)MR   LE/GONTES
L/W =L) .w) <sp>    MH/ [6]
```
Thus, the last line belongs to verse 6 in the LXX text.

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

The most problematic aspect of the database as received online is that some 
data-lines are split up over several document-lines, or need to be read in
conjunction with other lines. This is a bad side-effect of using in-line 
annotation instead of stand-off. I suspect it is also simply a quirk from
the older technology that was being used. For instance, the lines that are
"too long" are split up. This is not necessary with modern data storage methods.

Clustering discontinous data together into one place is a major goal of this repo.
Thus, where relevant, I will propose some things to do in order to remedy the 
discontinuities.

### long lines 

marked with # - long lines are broken up using # at end and # at beginning 
of its adjacent continuation:   

e.g. from Gen 15:11
```
H/PGRYM TA\ SW/MATA {d} TA\ DIXOTOMH/MATA #
#   AU)TW=N
```

In this example, the Greek line is continued on the second line.

The Hebrew line can also be carried to the next line:

Gen 5:26
```
{...$TYM W/$MWNYM} W/$B( #  O)KTAKO/SIA ^ DU/O
M)WT =+ #
```

Here `M)WT` should be read at the end of `W/$B(`. 

Thus, the `#` sign on the follow-up line will go into the opposite
column to whichever column is extended (1986:86).

### transpositions (marked with `^` or `^^^`)

Transpositions marked by `^` in one column are often cross-referenced
with a column in a subsequent line. The line may or may not be adjacent. But 
the documentation implies that it should at least be within the same verse.

*NB: A proper extraction of alignments should seek to maintain this link.
A better approach to the database would allow these links to be made more
naturally. For instance, given a set of indexed Hebrew words, link each index i 
to an index of Greek words j.*

#### local transpositions

Gen 1:2
```
W/H/)RC H( ^ DE\ GH=
```
The Greek words H( and DE\ should be switched to match the Hebrew.

*Remedy: There is the option here to re-arrange the Greek text to 
better match the Hebrew order. But it is not mandatory for us to do 
that. I will consider doing this.*

#### adjacent transpositions

Gen 2:4
```
)RC ^ =$MYM <sp>    TO\N OU)RANO\N
^ W/$MYM =W/)RC <sp>    KAI\ TH\N GH=N
```
The single ^ in one column followed immediately by another line
with ^ indicates a transposition of material between the two cols.

*Remedy: Hebrew col b should take precedence, provided it is contained
in col a of the adjacent line. i.e., in this case we only want $MYM rather
than W/$MYM. The second row should likewise take col. b instead.*

#### non-adjacent transpositions

Gen 1:11
```
^ L/MYN/W   ^^^   
)$R OU(=
ZR(/W   TO\ SPE/RMA AU)TOU=
B/W E)N AU)TW=|
^^^ ^ =L/MYN/W  KATA\ GE/NOS
```
The first row contains 2 columns, hebrew col a and greek col.
The single ^ before Hebrew and the triple ^^^ in the greek col
indicate that the Greek is transposed elsewhere in the text. 
The last row indicates the opposite: triple ^^^ indicate that 
the Hebrew text is elsewhere in the verse, the single ^ then seems
to serve as a placeholder. The Hebrew text is also contained in 
col b, the reconstruction.

*Remedy: When (+)Hebrew and (-)Greek with a ^ indication in the Hebrew
column and a ^^^ indication in place of the Greek, we should
go hunting for the Greek text elsewhere in the verse.*

#### non-adjacent, stylistic transpositions

Gen 1:29
```
ZR( {..^SPORI/MOU}
ZR( SPE/RMATOS
{...}   SPORI/MOU
L/KM    U(MI=N
```

The `{..^ }` brackets indicate that all of the contents are part of a 
transposition introduced for stylistic reasons. In this case, the true
parallel of the Hebrew is located two lines down, as marked by `{...}`.

*Remedy: We should keep the text contained in the brackets for the Hebrew-LXX
alignment. If we do a LXX-Hebrew alignment, the `{...}` should be replaced with 
the Hebrew text from the first row [ZR(].*

## Order of the Text

The order of the text in the database attempts to follow the printed text
where possible. However, only the Hebrew text order is reliably unaltered:

> The running text of MT thus has never been touched, while that of the LXX has been touched in the case of global differences between the two texts. (1986: 21). 

[Question: which passages in particular have been altered?]

## Unknown symbols

|  |  | 
|--|--|
| `<sp>` | e.g. Gen 2:4 `)RC ^ =$MYM <sp>    TO\N OU)RANO\N` |
