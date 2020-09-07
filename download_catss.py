"""
Use the download_catss function to download all of the 
text files for the CATSS database to disk.
"""

import requests
import time
from pathlib import Path

# Before writing the download function, we compile a series of 
# urls and filenames which will be used to download and output 
# the data. The culmination of these variables is stored under
# all_urls (further down), which is a dictionary of URL keys mapped
# to filenames for the download function

# base URL, which is formatted for each book that is retrieved
morph_url = 'http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/{}'
paral_url = 'http://ccat.sas.upenn.edu/gopher/text/religion/biblical/parallel/{}'

# names of the morphology book files; for formatting the URLs
# pasted from http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph
morph_books = '''
[   ]	01.Gen.1.mlxx	12-Jul-1994 15:10	711K
[   ]	02.Gen.2.mlxx	12-Jul-1994 15:11	673K
[   ]	03.Exod.mlxx	12-Jul-1994 15:05	1.0M
[   ]	04.Lev.mlxx	03-Aug-2015 15:13	812K
[   ]	05.Num.mlxx	10-Aug-2015 16:07	1.0M
[   ]	06.Deut.mlxx	06-Aug-2015 15:45	1.0M
[   ]	07.JoshB.mlxx	12-Jul-1994 15:55	638K
[   ]	08.JoshA.mlxx	12-Jul-1994 16:09	46K
[   ]	09.JudgesB.mlxx	12-Jul-1994 16:10	667K
[   ]	10.JudgesA.mlxx	12-Jul-1994 16:11	683K
[   ]	11.Ruth.mlxx	12-Jul-1994 16:12	88K
[   ]	12.1Sam.mlxx	04-Aug-2015 16:39	862K
[   ]	13.2Sam.mlxx	04-Aug-2015 16:43	766K
[   ]	14.1Kings.mlxx	06-Aug-2015 15:30	888K
[   ]	15.2Kings.mlxx	12-Jul-1994 16:41	807K
[   ]	16.1Chron.mlxx	12-Jul-1994 16:41	692K
[   ]	17.2Chron.mlxx	03-Aug-2015 16:30	910K
[   ]	18.1Esdras.mlxx	12-Jul-1994 16:58	387K
[   ]	19.2Esdras.mlxx	19-Jul-1994 12:45	568K
[   ]	20.Esther.mlxx	12-Jul-1994 16:59	251K
[   ]	21.Judith.mlxx	12-Jul-1994 16:59	392K
[   ]	22.TobitBA.mlxx	13-Jul-1994 09:41	236K
[   ]	23.TobitS.mlxx	13-Jul-1994 09:41	308K
[   ]	24.1Macc.mlxx	13-Jul-1994 09:42	791K
[   ]	25.2Macc.mlxx	03-Aug-2015 16:50	519K
[   ]	26.3Macc.mlxx	13-Jul-1994 09:55	223K
[   ]	27.4Macc.mlxx	19-Jul-1994 12:46	341K
[   ]	28.Psalms1.mlxx	13-Jul-1994 11:21	752K
[   ]	29.Psalms2.mlxx	06-Aug-2015 16:10	750K
[   ]	30.Odes.mlxx	13-Jul-1994 11:53	180K
[   ]	31.Proverbs.mlxx	31-Mar-2015 09:11	490K
[   ]	32.Qoheleth.mlxx	13-Jul-1994 11:54	193K
[   ]	33.Canticles.mlxx	13-Jul-1994 11:54	87K
[   ]	34.Job.mlxx	13-Jul-1994 11:54	589K
[   ]	35.Wisdom.mlxx	13-Jul-1994 12:53	301K
[   ]	36.Sirach.mlxx	10-Aug-2015 16:04	815K
[   ]	37.PsSol.mlxx	13-Jul-1994 13:36	212K
[   ]	38.Hosea.mlxx	13-Jul-1994 13:37	170K
[   ]	39.Micah.mlxx	13-Jul-1994 13:37	102K
[   ]	40.Amos.mlxx	13-Jul-1994 13:38	138K
[   ]	41.Joel.mlxx	13-Jul-1994 13:38	68K
[   ]	42.Jonah.mlxx	13-Jul-1994 13:38	47K
[   ]	43.Obadiah.mlxx	13-Jul-1994 13:40	20K
[   ]	44.Nahum.mlxx	06-Aug-2015 15:41	40K
[   ]	45.Habakkuk.mlxx	13-Jul-1994 13:41	48K
[   ]	46.Zeph.mlxx	13-Jul-1994 13:41	53K
[   ]	47.Haggai.mlxx	13-Jul-1994 13:41	40K
[   ]	48.Zech.mlxx	13-Jul-1994 13:42	213K
[   ]	49.Malachi.mlxx	13-Jul-1994 13:42	61K
[   ]	50.Isaiah1.mlxx	04-Aug-2015 16:33	672K
[   ]	51.Isaiah2.mlxx	03-Aug-2015 15:22	485K
[   ]	52.Jer1.mlxx	03-Aug-2015 15:51	639K
[   ]	53.Jer2.mlxx	06-Aug-2015 15:56	600K
[   ]	54.Baruch.mlxx	13-Jul-1994 14:27	111K
[   ]	55.EpJer.mlxx	13-Jul-1994 14:29	56K
[   ]	56.Lam.mlxx	04-Aug-2015 16:30	105K
[   ]	57.Ezek1.mlxx	13-Jul-1994 15:04	601K
[   ]	58.Ezek2.mlxx	13-Jul-1994 15:04	663K
[   ]	59.BelOG.mlxx	19-Jul-1994 12:46	38K
[   ]	60.BelTh.mlxx	19-Jul-1994 12:46	37K
[   ]	61.DanielOG.mlxx	10-Aug-2015 16:14	460K
[   ]	62.DanielTh.mlxx	19-Jul-1994 12:46	446K
[   ]	63.SusOG.mlxx	19-Jul-1994 12:46	34K
[   ]	64.SusTh.mlxx	19-Jul-1994 12:47	49K
'''

# names of parellel book files
# pasted from http://ccat.sas.upenn.edu/gopher/text/religion/biblical/parallel
paral_books = '''
[   ]	01.Genesis.par	08-Dec-1999 10:27	379K
[   ]	02.Exodus.par	05-Apr-1994 17:36	318K
[   ]	03.Lev.par	05-Apr-1994 17:36	225K
[   ]	04.Num.par	05-Apr-1994 17:36	299K
[   ]	05.Deut.par	05-Apr-1994 17:36	265K
[   ]	06.JoshB.par	05-Apr-1994 17:36	198K
[   ]	07.JoshA.par	05-Apr-1994 17:36	13K
[   ]	08.JudgesB.par	05-Apr-1994 17:36	178K
[   ]	09.JudgesA.par	02-Sep-1994 16:53	183K
[   ]	10.Ruth.par	05-Apr-1994 17:36	23K
[   ]	11.1Sam.par	05-Apr-1994 17:36	244K
[   ]	12.2Sam.par	05-Apr-1994 17:36	209K
[   ]	13.1Kings.par	05-Apr-1994 17:36	302K
[   ]	14.2Kings.par	05-Apr-1994 17:36	220K
[   ]	15.1Chron.par	05-Apr-1994 17:36	191K
[   ]	16.2Chron.par	18-Feb-2005 15:18	242K
[   ]	17.1Esdras.par	05-Apr-1994 17:36	161K
[   ]	18.Esther.par	05-Apr-1994 17:36	84K
[   ]	18.Ezra.par	05-Apr-1994 17:36	70K
[   ]	19.Neh.par	05-Apr-1994 17:36	94K
[   ]	20.Psalms.par	05-Apr-1994 17:36	533K
[   ]	22.Ps151.par	05-Apr-1994 17:36	1.8K
[   ]	23.Prov.par	05-Apr-1994 17:36	158K
[   ]	24.Qoh.par	05-Apr-1994 17:36	48K
[   ]	25.Cant.par	25-Mar-2015 11:34	24K
[   ]	26.Job.par	05-Apr-1994 17:36	183K
[   ]	27.Sirach.par	05-Apr-1994 17:36	289K
[   ]	28.Hosea.par	05-Apr-1994 17:36	46K
[   ]	29.Micah.par	05-Apr-1994 17:36	27K
[   ]	30.Amos.par	05-Apr-1994 17:36	37K
[   ]	31.Joel.par	05-Apr-1994 17:36	18K
[   ]	32.Jonah.par	05-Apr-1994 17:36	13K
[   ]	33.Obadiah.par	05-Apr-1994 17:36	5.4K
[   ]	34.Nahum.par	05-Apr-1994 17:36	11K
[   ]	35.Hab.par	05-Apr-1994 17:36	13K
[   ]	36.Zeph.par	05-Apr-1994 17:36	14K
[   ]	37.Haggai.par	05-Apr-1994 17:36	11K
[   ]	38.Zech.par	05-Apr-1994 17:36	57K
[   ]	39.Malachi.par	05-Apr-1994 17:36	17K
[   ]	40.Isaiah.par	05-Apr-1994 17:36	334K
[   ]	41.Jer.par	05-Apr-1994 17:36	461K
[   ]	42.Baruch.par	05-Apr-1994 17:36	16K
[   ]	43.Lam.par	05-Apr-1994 17:36	30K
[   ]	44.Ezekiel.par	05-Apr-1994 17:36	359K
[   ]	45.DanielOG.par	05-Apr-1994 17:36	177K
[   ]	46.DanielTh.par	05-Apr-1994 17:36	143K
'''

# clean the book names
morph_books = [book.split('\t')[1] for book in morph_books.split('\n')
                  if book]
paral_books = [book.split('\t')[1] for book in paral_books.split('\n')
                  if book]

# assemble URLs for both morph and parallel data
all_urls = {}
for dataset, base_url in [(morph_books, morph_url), (paral_books, paral_url)]:
    for book in dataset:
        all_urls[base_url.format(book)] = book

def download_catss(urls=all_urls, output_dir='source', silent=False, sleeptime=1):
    """Download all of CATSS morphology and parallels as plain text files

    Args:
        urls: a dict where each key is a url address and each value is a 
            corresponding file name (e.g. the book name) to output the page's
            data to.
        output_dir: the directory where the files should be output to
        silent: boolean, False if you want to print status updates
        sleeptime: number of seconds to wait between each download
    
    Returns:
        True if task finishes. Files are output to output_dir.
    """

    # check for output directory and create if necessary
    out_dir = Path(output_dir)
    if not out_dir.exists():
        out_dir.mkdir()

    # walk the URLs, download each one, and output as a file
    for url, filename in urls.items():

        if not silent:
            print(f'retrieving {url}...')

        # path to output data
        out_path = out_dir.joinpath(filename)

        # download the data
        download_data = requests.get(url).text
        
        # write to disk
        with open(out_path, 'w') as outfile:
            outfile.write(download_data) # output here
        
        if not silent:
            print(f'\t|data written to {out_path}')

        # pause between each download to be nice to server
        time.sleep(sleeptime)

    return True
