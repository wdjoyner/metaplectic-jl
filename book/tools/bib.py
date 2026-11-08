#!/usr/bin/env python3
"""Merge the five bibliographies into one, keyed by the book's citation keys.
Usage: python3 bib.py BIBS_JSON BOOK_DIR"""
import json, re, sys, os, glob
bibs = json.load(open(sys.argv[1])); BOOK = sys.argv[2]
sys.path.insert(0, os.path.dirname(__file__))
BIBMAP = {
    'I':   {'BZ': 'BZ76', 'Gao': 'Gao12', 'W': 'Wei'},
    'II':  {'BZ': 'BZ77'},
    'III': {'Kottwitz84': 'Kot84', 'MilneADT': 'MilADT', 'Adams62': 'Ada62', 'Atiyah66': 'Ati66',
            'SegalK': 'Seg68', 'FK86': 'FK', 'Zou': 'Z', 'Badulescu': 'Bad', 'Cohen': 'Coh',
            'Loeser': 'Loe', 'ArtinTate': 'AT', 'Klose86': 'Klo86a', 'PrasadRaghunathan88': 'PRa88',
            'Riehm70': 'Rie70'},
    'IV':  {'Zou24': 'Z', 'KP': 'KP1', 'Kottwitz84': 'Kot84', 'ClozelDelorme': 'CD84', 'Li14': 'Li4'},
    'W':   {'BD01': 'BD', 'Gao': 'Gao18', 'Bad08': 'Bad', 'Kub': 'Kub69', 'Zou24': 'Z'},
}
SELF = {'P1', 'P3', 'JoynerI', 'JoynerII', 'JoynerIII', 'JoynerIV', 'RankTwo0'}
# preferred source for each global key (first listed wins)
PREF = ['I', 'II', 'III', 'IV', 'W']
OVERRIDE = {'DKV': 'W', 'Coh': 'III'}   # more complete entries
entries, sources = {}, {}
for src in PREF:
    for k, v in bibs[src].items():
        if k in SELF: continue
        g = BIBMAP.get(src, {}).get(k, k)
        sources.setdefault(g, []).append('%s:%s' % (src, k))
        if g not in entries or OVERRIDE.get(g) == src:
            entries[g] = v
entries['Wei'] = entries['Wei'].replace('2nd ed., Springer, 1973.', '2nd ed., Springer, 1973; 3rd ed., 1974.')
# keys cited
cited = set()
for f in glob.glob(os.path.join(BOOK, 'chapters', '*.tex')):
    for m in re.finditer(r'\\cite(?:\[[^\]]*\])?\{([^}]*)\}', open(f).read()):
        cited.update(k.strip() for k in m.group(1).split(','))
missing = sorted(cited - set(entries))
uncited = sorted(set(entries) - cited)
keys = sorted(cited & set(entries), key=lambda k: k.lower())
out = ['\\begin{thebibliography}{Klo86b}\\small']
for k in keys:
    out.append('\\bibitem[%s]{%s} %s' % (k, k, entries[k]))
out.append('\\end{thebibliography}')
open(os.path.join(BOOK, 'chapters', 'bibliography.tex'), 'w').write('\n'.join(out) + '\n')
merged = {g: s for g, s in sources.items() if len(s) > 1}
json.dump({'missing': missing, 'uncited': uncited, 'merged': merged}, open(os.path.join(BOOK, 'bib_report.json'), 'w'), indent=1)
print('entries', len(keys), 'missing', missing, '\nuncited', uncited)
print('merged', len(merged))
