#!/usr/bin/env python3
"""Convert the five frozen papers of the metaplectic Jacquet--Langlands
series into chapter files of one book.

Usage: python3 convert.py REPO_DIR AUX_DIR OUT_DIR

AUX_DIR holds compiled copies of the frozen drafts (x.aux in
subdirectories I10, I, II, III, IV, W) so that typed numbers such as
"Part~I, Lemma~2.2" can be mapped to labels.

The script prints every reference it could not resolve and writes a
report (conversion_report.txt) to OUT_DIR.
"""
import re, sys, os, json

REPO, AUX, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
report = []

SRC = {
    'I':   'part-I/mjl_part1_draft11.tex',
    'II':  'part-II/mjl_part2_draft10.tex',
    'III': 'part-III/mjl_part3_draft10.tex',
    'IV':  'part-IV/mjl_part4_draft6.tex',
    'W':   'part-IV/mjl_rank2_wild_draft8.tex',
}
ROMAN = ['IV', 'III', 'II', 'I']

# ---------------------------------------------------------------- maps
def read_aux(tag):
    """number -> list of labels, split into theorem-like, sections, equations."""
    s = open(os.path.join(AUX, tag, 'x.aux')).read()
    thm, sec, eq = {}, {}, {}
    for m in re.finditer(r'\\newlabel\{([^}]*)\}\{\{([^}]*)\}', s):
        lab, num = m.group(1), m.group(2)
        if 'cref' in lab or lab.startswith('gl:'):
            continue
        pre = lab.split(':')[0]
        if pre in ('sec', 'subsec', 'app'):
            sec.setdefault(num, lab)
        elif pre == 'eq':
            eq.setdefault(num, lab)
        else:
            thm.setdefault(num, lab)
    return thm, sec, eq

MAPS = {t: read_aux(t) for t in ['I10', 'I', 'II', 'III', 'IV', 'W']}
# headings that had no label in the frozen drafts; labels are added below
EXTRA_SEC = {'I': {'1.1': 'subsec:setting', '1.4': 'subsec:conventions'},
             'I10': {'1.1': 'subsec:setting', '1.4': 'subsec:conventions'},
             'III': {'2': 'sec:setting'}, 'IV': {'2.1': 'subsec:restriction'}}
for t, d in EXTRA_SEC.items():
    MAPS[t][1].update(d)
ADD_LABELS = {
    'I': [('\\subsection{Setting and aim}', '\\subsection{Setting and aim}\\label{subsec:setting}'),
          ('\\subsection{Conventions}', '\\subsection{Conventions}\\label{subsec:conventions}')],
    'III': [('\\section{Local setting and good elements}', '\\section{Local setting and good elements}\\label{sec:setting}')],
    'IV': [('\\subsection{Restriction and relabeling}', '\\subsection{Restriction and relabeling}\\label{subsec:restriction}')],
}

def partmap(target, source):
    """Which numbering a source paper uses when it cites `target`."""
    if target == 'I':
        return 'I' if source in ('II', 'III', 'GL') else 'I10'
    return target

NAME_PREFIX = {
    'lemma': 'lem', 'lemmas': 'lem', 'theorem': 'thm', 'theorems': 'thm',
    'proposition': 'prop', 'propositions': 'prop', 'definition': 'def',
    'corollary': 'cor', 'corollaries': 'cor', 'remark': 'rem',
    'example': 'ex', 'assumption': 'ass',
}

def resolve(target, source, name, num, ctx):
    """Return LaTeX for one cross-chapter item, or None."""
    m = MAPS[partmap(target, source)]
    nm = name.lower().rstrip('.')
    if nm in ('\\s', '\\s\\s', 'section', 'sections', 'appendix'):
        lab = m[1].get(num)
        if lab is None:
            return None
        return ('\\S' if nm.startswith('\\s') else
                ('Section~' if nm.startswith('section') else
                 ('Appendix~' if nm == 'appendix' else ''))) + '\\ref{%s:%s}' % (target, lab)
    if nm in ('equation',):
        lab = m[2].get(num)
        return None if lab is None else '\\eqref{%s:%s}' % (target, lab)
    lab = m[0].get(num)
    if lab is None:
        return None
    want = NAME_PREFIX.get(nm)
    have = lab.split(':')[0]
    if want and want != have:
        report.append('NAME MISMATCH in %s: "%s %s" of Part %s is %s (rendered by \\cref)  ctx: %s'
                      % (source, name, num, target, lab, ctx))
    return '\\cref{%s:%s}' % (target, lab)

# ------------------------------------------------- cross-part references
ITEM_NAMES = (r'(?:Lemmas|Lemma|Theorems|Theorem|Propositions|Proposition|Definition|'
              r'Corollaries|Corollary|Remark|Example|Assumption|Sections|Section|Appendix|'
              r'\\S\\S|\\S|equation)')
NUM = r'(?:\d+(?:\.\d+)*|[AB](?:\.\d+)?)'
SUFFIX = r'(?:\([a-z0-9]+\)(?:,\([a-z0-9]+\))*)?'

def convert_part_refs(s, source):
    def chain_repl(m):
        target = m.group('part')
        body = m.group('body')
        ctx = m.group(0)[:90].replace('\n', ' ')
        out = []
        pos = 0
        cur_name = None
        tokens = re.finditer(r'(?P<name>' + ITEM_NAMES + r')?[~ ]?(?P<num>' + NUM + r')(?P<suf>' + SUFFIX + r')'
                             r'|(?P<sep>,\s|\s+and\s+|~and~|--|;\s)', body)
        res = ''
        for t in tokens:
            if t.start() != pos:
                return None
            pos = t.end()
            if t.group('sep'):
                res += t.group('sep')
                continue
            if t.group('name'):
                cur_name = t.group('name')
            if cur_name is None:
                return None
            r = resolve(target, source, cur_name, t.group('num'), ctx)
            if r is None:
                report.append('UNRESOLVED in %s: Part %s, %s %s  ctx: %s'
                              % (source, target, cur_name, t.group('num'), ctx))
                return None
            if cur_name.startswith('\\S\\S') and res.endswith(('--', ' and ', '~and~', ', ')):
                r = r.replace('\\S', '', 1)
            if cur_name.startswith('\\S\\S') and not res:
                r = '\\S' + r
            res += r + (t.group('suf') or '')
        if pos != len(body):
            return None
        return res

    pat = re.compile(r"Part[~ ](?P<part>IV|III|II|I)\b(?:,\s*|'s\s+|\s+)(?P<body>(?:" + ITEM_NAMES + r")[~ ]?" + NUM + SUFFIX +
                     r"(?:(?:,\s|\s+and\s+|~and~|--|;\s)(?:" + ITEM_NAMES + r")?[~ ]?" + NUM + SUFFIX + r")*)")
    def repl(m):
        r = chain_repl(m)
        if r is None:
            return m.group(0)
        return r
    s = pat.sub(repl, s)
    # postfix form "Theorem~4.3 and Corollary~5.1 of Part~III"
    pat2 = re.compile(r'(?P<body>(?:' + ITEM_NAMES + r')[~ ]' + NUM + r'(?:\s+and\s+(?:' + ITEM_NAMES + r')[~ ]' + NUM + r')*) of Part[~ ](?P<part>IV|III|II|I)\b')
    def repl2(m):
        target = m.group('part')
        def one(t):
            r = resolve(target, source, t.group(1), t.group(2), m.group(0))
            return r if r else t.group(0)
        return re.sub(r'(' + ITEM_NAMES + r')[~ ](' + NUM + r')', one, m.group('body'))
    s = pat2.sub(repl2, s)
    # drafts
    s = re.sub(r'Part[~ ](IV|III|II|I),?\s+Draft[~ ]\d+', lambda m: 'Chapter~\\ref{ch:%s}' % m.group(1), s)
    s = re.sub(r'Part[~ ](IV|III|II|I)\s+as\s+Draft[~ ]\d+', lambda m: 'Chapter~\\ref{ch:%s}' % m.group(1), s)
    # plural and remaining
    s = re.sub(r'Parts[~ ](IV|III|II|I)(--|\u2013)(IV|III|II|I)\b',
               lambda m: 'Chapters~\\ref{ch:%s}--\\ref{ch:%s}' % (m.group(1), m.group(3)), s)
    s = re.sub(r'Parts[~ ](IV|III|II|I)(,?\s+and~?\s*|~and~)(IV|III|II|I)\b',
               lambda m: 'Chapters~\\ref{ch:%s} and~\\ref{ch:%s}' % (m.group(1), m.group(3)), s)
    s = re.sub(r"Part[~ ](IV|III|II|I)\b", lambda m: 'Chapter~\\ref{ch:%s}' % m.group(1), s)
    return s

# ------------------------------------------------------- bibliography
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
SELF = {'P1': 'I', 'P3': 'III', 'JoynerI': 'I', 'JoynerII': 'II', 'JoynerIII': 'III',
        'JoynerIV': 'IV', 'RankTwo0': 'W'}

def bibkeys(s):
    i = s.index('\\begin{thebibliography}'); j = s.index('\\end{thebibliography}')
    return re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}', s[i:j])

def gkey(src, k):
    return BIBMAP.get(src, {}).get(k, k)

def convert_cites(s, src, keys):
    keyset = set(keys)
    # \cite[opt]{a,b}
    def c1(m):
        opt, ks = m.group(1), [k.strip() for k in m.group(2).split(',')]
        if len(ks) == 1 and ks[0] in SELF:
            ch = SELF[ks[0]]
            return 'Chapter~\\ref{ch:%s}' % ch + (', ' + opt[1:-1] if opt else '')
        ks = [gkey(src, k) for k in ks]
        return '\\cite%s{%s}' % (opt or '', ','.join(ks))
    s = re.sub(r'\\cite(\[[^\]]*\])?\{([^}]*)\}', c1, s)
    # manual brackets [KEY], [KEY, opt], [K1; K2, opt]
    def c2(m):
        inner = m.group(1)
        parts = [p.strip() for p in inner.split(';')]
        outs = []
        for p in parts:
            mm = re.match(r'^([A-Za-z][A-Za-z0-9]*)(?:,\s*(.*))?$', p, re.S)
            if not mm or mm.group(1) not in keyset:
                return m.group(0)
            k, opt = mm.group(1), mm.group(2)
            if k in SELF:
                outs.append('Chapter~\\ref{ch:%s}' % SELF[k] + (', ' + opt if opt else ''))
            else:
                outs.append('\\cite%s{%s}' % ('[' + opt + ']' if opt else '', gkey(src, k)))
        return '; '.join(outs)
    s = re.sub(r'(?<![\\\w])\[([A-Za-z][^\[\]]{0,120}?)\]', c2, s)
    return s

# ---------------------------------------------------------- labels
def prefix_labels(s, tag):
    def fix(lab):
        lab = lab.strip()
        if lab.startswith(('gl:', 'ch:')) or re.match(r'^(I|II|III|IV|W):', lab):
            return lab
        return tag + ':' + lab
    s = re.sub(r'\\(label|ref|eqref|pageref|cref|Cref)\{([^}]*)\}',
               lambda m: '\\%s{%s}' % (m.group(1), ','.join(fix(x) for x in m.group(2).split(','))), s)
    s = re.sub(r'\\hyperref\[([^\]]*)\]', lambda m: '\\hyperref[%s]' % fix(m.group(1)), s)
    s = re.sub(r'\\tag\{([^}]*)\}\\label', r'\\tag{\1}\\label', s)
    return s

# ---------------------------------------------------------- macros
def scoped_macros(pre):
    """Turn every \\newcommand of a preamble into \\providecommand+\\renewcommand
    (balanced-brace parsing, any nesting depth)."""
    out = []
    pos = 0
    while True:
        k = pre.find('\\newcommand{', pos)
        if k < 0:
            break
        j = pre.index('}', k + 12)
        name = pre[k + 12:j]
        rest = pre[j + 1:]
        m = re.match(r'(\[\d\])?', rest)
        args = m.group(1) or ''
        q = j + 1 + len(args)
        assert pre[q] == '{', (name, pre[q:q + 20])
        depth, t = 0, q
        while True:
            c = pre[t]
            if c == '\\':
                t += 2; continue
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: break
            t += 1
        body = pre[q + 1:t]
        out.append('\\providecommand{%s}{}\\renewcommand{%s}%s{%s}' % (name, name, args, body))
        pos = t + 1
    return '\n'.join(out)

def split_doc(s):
    pre = s[:s.index('\\begin{document}')]
    body = s[s.index('\\begin{document}') + len('\\begin{document}'):s.index('\\begin{thebibliography}')]
    return pre, body

def extract_abstract(body):
    m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', body, re.S)
    return m.group(1).strip() if m else ''

def strip_front(body):
    body = re.sub(r'\\maketitle', '', body)
    body = re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}', '', body, flags=re.S)
    body = re.sub(r'\\tableofcontents', '', body)
    body = re.sub(r'\\emergencystretch=3em', '', body)
    return body

def cut_section(body, start_pat, end_pats):
    """Remove and return the block starting at regex start_pat up to the first end_pat."""
    m = re.search(start_pat, body)
    if not m:
        report.append('BLOCK NOT FOUND: ' + start_pat)
        return body, ''
    i = m.start()
    j = len(body)
    for e in end_pats:
        mm = re.compile(e).search(body, m.end())
        if mm and mm.start() < j:
            j = mm.start()
    return body[:i] + body[j:], body[i:j]

def demote(block):
    """section -> subsection etc. for blocks moved into a book chapter as sections."""
    block = re.sub(r'\\subsection(\*?)\{', r'\\subsubsection\1{', block)
    block = re.sub(r'\\section(\*?)\{', r'\\section\1{', block)
    return block

# ---------------------------------------------------------- main
chapters = {}
moved = {'lit': {}, 'gloss': {}, 'summary': {}, 'appendix': ''}
macros = {}
abstracts = {}

for tag, f in SRC.items():
    s = open(os.path.join(REPO, f)).read()
    keys = bibkeys(s)
    pre, body = split_doc(s)
    macros[tag] = scoped_macros(pre)
    abstracts[tag] = extract_abstract(body)
    body = strip_front(body)
    body = body.replace('\\input{../glossary}\n', '').replace('\\input{../glossary}', '')
    for a, b in ADD_LABELS.get(tag, []):
        assert body.count(a) == 1, (tag, a)
        body = body.replace(a, b)
    # acknowledgments go to the preface
    m = re.search(r'\\section\*\{Acknowledgments[^}]*\}(.*)$', body, flags=re.S)
    moved.setdefault('ack', {})[tag] = m.group(1).strip() if m else ''
    body = body[:m.start()] if m else body
    body = re.sub(r'\\appendix\s*', '', body)
    # move blocks
    SEC = r'(?:%\s*=+\s*\n)?\\section'
    nxt = [r'(?:%\s*=+\s*\n)?\\section[\*\{]', r'$']
    if tag == 'I':
        body, moved['lit']['I'] = cut_section(body, SEC + r'\{Literature\}', nxt)
        body, moved['gloss']['I'] = cut_section(body, SEC + r'\{Notation and glossary\}', nxt)
        body, moved['summary']['I'] = cut_section(body, SEC + r'\{Summary of results\}', nxt)
    if tag == 'II':
        body, moved['summary']['II'] = cut_section(body, SEC + r'\*\{Summary of results\}', nxt)
        body, moved['gloss']['II'] = cut_section(body, SEC + r'\{Notation and glossary\}', nxt)
        body, moved['lit']['II'] = cut_section(body, SEC + r'\{Related work\}', nxt)
    if tag == 'III':
        body, moved['summary']['III'] = cut_section(body, SEC + r'\*\{Summary of results\}', nxt)
        body, moved['gloss']['III'] = cut_section(body, SEC + r'\{Notation and glossary\}', nxt)
        body, moved['lit']['III'] = cut_section(body, SEC + r'\{Related work\}', nxt)
    if tag == 'IV':
        body, moved['gloss']['IV'] = cut_section(body, SEC + r'\{Selected glossary\}', nxt)
    if tag == 'W':
        body, moved['summary']['W'] = cut_section(body, SEC + r'\{Summary of results\}', nxt)
        body, moved['lit']['W'] = cut_section(body, SEC + r'\{Related literature\}', nxt)
        body, moved['appendix'] = cut_section(body, SEC + r'\{Tables\}', [r'$'])
    chapters[tag] = (body, keys)

def full_convert(text, tag, keys):
    text = prefix_labels(text, tag)
    text = convert_part_refs(text, tag)
    text = convert_cites(text, tag, keys)
    return text

out = {}
for tag, (body, keys) in chapters.items():
    out[tag] = full_convert(body, tag, keys)
for kind in ('lit', 'gloss', 'summary', 'ack'):
    for tag, blk in list(moved[kind].items()):
        moved[kind][tag] = full_convert(blk, tag, chapters[tag][1])
moved['appendix'] = full_convert(moved['appendix'], 'W', chapters['W'][1])
for tag in abstracts:
    abstracts[tag] = full_convert(abstracts[tag], tag, chapters[tag][1])

# glossary
g = open(os.path.join(REPO, 'glossary.tex')).read()
g = convert_part_refs(g, 'GL')
g = g.replace('the companion paper on the rank-two wild place', 'Chapter~\\ref{ch:W}')
g = g.replace('(companion paper,\n\\S1)', '(Chapter~\\ref{ch:W}, \\S\\ref{W:sec:intro})')
g = g.replace('(Part~IV; companion paper)', '(Chapters~\\ref{ch:IV} and~\\ref{ch:W})')

json.dump({'chapters': out, 'moved': moved, 'macros': macros, 'abstracts': abstracts, 'glossary': g},
          open(os.path.join(OUT, 'converted.json'), 'w'))
open(os.path.join(OUT, 'conversion_report.txt'), 'w').write('\n'.join(report) + '\n')
print('\n'.join(report))
print('DONE')
