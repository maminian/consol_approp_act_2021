# requires pypdf2
# pip install pypdf2

import PyPDF2 as pdf
import re
from matplotlib import pyplot
import numpy as np

def dollars2int( matchin ):
    '''
    converts a single or many strings matching a pattern
    [0-9\,]{1,} into associated integers, assuming commas 
    only represent thousands separators, or possibly 
    trailing commas in a sentence.
    
    Ex: dollars2int("123,456") => 123456 (integer)
        dollars2int([ "1,234", "56,789" ]) => [1234,56789]
    '''
    import numpy as np
    
    if isinstance(matchin, list):
        return [dollars2int(mi) for mi in matchin]
    else:
        try:
            return int( matchin.replace(',', '') )
        except:
            return np.nan
#

######

FILENAME = "BILLS-116HR133SA-RCP-116-68.pdf"
PAGENUM = 8 # automate later
DOLLAR_REGEX = "\$([0-9\,]{1,})\,?"



# don't close this for the love of god
f = open(FILENAME, 'rb')

pf = pdf.PdfFileReader(f)


page = pf.getPage(PAGENUM)
page_text = page.extractText()

matches = re.findall(DOLLAR_REGEX, page_text)
dollars2int(matches)

# 
dollars_by_page = np.nan*np.zeros( pf.numPages )

for i in range( pf.numPages ):
    page = pf.getPage(i)
    page_text = page.extractText()
    matches = re.findall(DOLLAR_REGEX, page_text)
    # if there is a match, record the largest dollar 
    # value by page.
    if len(matches) > 0: 
        all_dollars = dollars2int(matches)
        dollars_by_page[i] = np.nanmax(all_dollars)
    #
    if np.mod(i,100)==0:
        print("%i of %i" % (i+1,pf.numPages))
#

ALL_TEXT_EVER = ""
page_checkpoints = np.zeros(pf.numPages, dtype=int)
for i in range( pf.numPages ):
    page = pf.getPage(i)
    page_text = page.extractText()
    poo = page_text.split("\n")
    poo = poo[1:]   #skip header
    for pp in poo:
        ALL_TEXT_EVER += pp # yolo
        page_checkpoints[i] += len(pp)  # ha ha
    #
    

    if np.mod(i,100)==0:
        print("%i of %i" % (i+1,pf.numPages))
#

# identify all pages associated with some pattern.
#tomatch = ["[cC]opyright", "[fF]elony", "[sS]tream"]
tomatch = [
"Egypt",
"Sudan",
"Ukraine",
"Isr[ae]{,2}l",
"Nepal",
"Burma",
"Cambodia",
"Pakistan",
"Asia"
]

hit_positions = np.zeros( (len(tomatch), len(ALL_TEXT_EVER)) )

for (i,desired) in enumerate(tomatch):
    pattern = re.compile(desired)
    for match in pattern.finditer(ALL_TEXT_EVER):
        hit_positions[i,match.start()] = 1
#
#for j,(tm,hp) in enumerate( zip(tomatch, hit_positions) ):
#    nzl = np.where( hp > 0)[0]
#    ax.scatter(nzl, j*np.ones(len(nzl)), alpha=0.5, s=200, label=tm)
#

fig,ax = pyplot.subplots(1,1, figsize=(10,5), constrained_layout=True)
window = np.ones(1000)
occurrences = []
for j,hi in enumerate(hit_positions):
    occurrences.append( np.convolve(hi,window) )
    if j%10==0:
        print(j)
#
#occurrences = [np.convolve(hi, window) for hi in hit_positions]
for j,(tm,oc) in enumerate(zip(tomatch, oc)):
    if max(oc) < 3:
        continue    # don't bother with shitter countries.
    #
    idx = np.argmax(oc)
    ax.plot(range(len(oc)), oc, lw=1, alpha=0.5)
    ax.text(idx, odx[idx], tm, fontsize=10, rotation=45, ha='left', va='bottom')
#

