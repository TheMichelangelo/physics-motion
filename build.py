"""Generate the static interactive page directly from the reviewed LaTeX source."""
from pathlib import Path
import re, html
ROOT=Path(__file__).resolve().parent
tex=(ROOT/'exercises.tex').read_text()
def group(s,i):
 assert s[i]=='{'
 depth=1;j=i+1
 while depth:
  if s[j]=='{' and s[j-1]!='\\':depth+=1
  elif s[j]=='}' and s[j-1]!='\\':depth-=1
  j+=1
 return s[i+1:j-1],j

def convert(raw):
 math=[]
 def save(m):
  value=m.group(0)
  if value.startswith('$'):value=r'\('+value[1:-1]+r'\)'
  math.append(html.escape(value));return f'@@M{len(math)-1}@@'
 raw=re.sub(r'\$[^$]*\$|\\\[.*?\\\]',save,raw,flags=re.S)
 raw=re.sub(r'\\setlength\{[^}]*\}\{[^}]*\}','',raw)
 raw=html.escape(raw)
 # Text macros are parsed with balanced braces rather than a greedy regex.
 for cmd,tag in [('why','h4'),('textbf','strong'),('textit','em')]:
  needle='\\'+cmd+'{'
  while needle in raw:
   a=raw.index(needle);content,z=group(raw,a+len(needle)-1)
   raw=raw[:a]+f'<{tag}>'+content+f'</{tag}>'+raw[z:]
 # Targets contain nested braces.
 while '\\target{' in raw:
  a=raw.index('\\target{');content,z=group(raw,a+7)
  raw=raw[:a]+'<hr>'+html.escape(r'\('+html.unescape(content)+r'-?\)')+raw[z:]
 raw=raw.replace(r'\par','<br>').replace('---','—').replace('--','–')
 raw=re.sub(r'\n\s*\n','<div class="paragraph-gap"></div>',raw)
 for i,m in enumerate(math):raw=raw.replace(f'@@M{i}@@',m)
 return raw.strip()

body=tex.split('\\begin{document}',1)[1]
rule=body.split('\\begingroup\\color{red!80!black}',1)[1].split('\\endgroup',1)[0]
rule=re.sub(r'\\subsection\*\{[^}]+\}','',rule,count=1)
items=[]
for match in re.finditer(r'\\subsection\*\{',body):
 title,end=group(body,match.end()-1)
 if title.startswith('Правило'):continue
 nextpos=body.find('\\subsection*{',end)
 section=body[end:nextpos if nextpos!=-1 else len(body)]
 table=re.search(r'\\begin\{(solutiontwo|solutiontable|solutionwide)\}',section)
 assert table,title
 env=table.group(1); condition=section[:table.start()].strip()
 tablebody=section[table.end():section.index('\\end{'+env+'}')]
 cells=re.split(r'^&$',tablebody,flags=re.M)
 assert len(cells)==(2 if env=='solutiontwo' else 3),(title,len(cells))
 topic='river' if len(items)>=12 else 'straight'
 slug='exercise-'+str(len(items)+1)
 labels=['Дано','Розв’язання'] if len(cells)==2 else ['Дано','СІ','Розв’язання']
 tablehtml='<div class="table-scroll"><table><thead><tr>'+''.join('<th scope="col">'+v+'</th>' for v in labels)+'</tr></thead><tbody><tr>'+''.join('<td class="'+('reasoning' if i==len(cells)-1 else 'given')+'">'+convert(v)+'</td>' for i,v in enumerate(cells))+'</tr></tbody></table></div>'
 items.append(f'''<article class="exercise" id="{slug}" data-topic="{topic}"><header class="exercise-header"><span class="topic-label">{'За течією та проти течії' if topic=='river' else 'Прямолінійний рух'}</span><a class="permalink" href="#{slug}" aria-label="Посилання на задачу">#</a><h2>{html.escape(title)}</h2></header><div class="condition">{convert(condition)}</div><details class="solution"><summary>Показати розв’язання</summary>{tablehtml}</details></article>''')
assert len(items)==16,len(items)
template=(ROOT/'template.html').read_text()
page=template.replace('<!--RULE-->',convert(rule)).replace('<!--EXERCISES-->','\n'.join(items))
(ROOT/'index.html').write_text(page)
print(f'Generated {len(items)} exercises from the reviewed LaTeX source.')
