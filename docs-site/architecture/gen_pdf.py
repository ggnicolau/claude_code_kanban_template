from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
import re
import os
import subprocess
import tempfile
import shutil

# === PALETTE ===
DEEP_PURPLE   = colors.HexColor('#4A148C')
MED_PURPLE    = colors.HexColor('#7B1FA2')
LIGHT_PURPLE  = colors.HexColor('#E1BEE7')
VERY_LIGHT    = colors.HexColor('#F3E5F5')
DARK_GREY     = colors.HexColor('#212121')
MID_GREY      = colors.HexColor('#616161')
LIGHT_GREY    = colors.HexColor('#F5F5F5')
WHITE         = colors.HexColor('#FAFAFA')
BLUE_NOTE     = colors.HexColor('#E3F2FD')
BLUE_NOTE_BDR = colors.HexColor('#1565C0')
TIP_BDR       = colors.HexColor('#6A1B9A')
QUOTE_BG      = colors.HexColor('#1A1A2E')
ACCENT_LINE   = colors.HexColor('#CE93D8')

PAGE_W, PAGE_H = A4
LEFT_M  = 2.2 * cm
RIGHT_M = 2.2 * cm
TOP_M   = 2.0 * cm
BOT_M   = 2.2 * cm


class DecorativeLine(Flowable):
    def __init__(self, width, color=ACCENT_LINE, thickness=1.5, spaceAbove=6, spaceBelow=6):
        Flowable.__init__(self)
        self.line_width = width
        self.color = color
        self.thickness = thickness
        self.spaceAbove = spaceAbove
        self.spaceBelow = spaceBelow
        self.height = thickness + spaceAbove + spaceBelow

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.spaceBelow, self.line_width, self.spaceBelow)


class ColorBox(Flowable):
    def __init__(self, content_para, bg_color, border_color, width, padding=10):
        Flowable.__init__(self)
        self.content = content_para
        self.bg = bg_color
        self.border = border_color
        self.box_width = width
        self.padding = padding
        self.box_h = 0

    def wrap(self, availW, availH):
        inner_w = self.box_width - 2 * self.padding - 4
        w, h = self.content.wrap(inner_w, availH)
        self.box_h = h + 2 * self.padding + 4
        self.width = self.box_width
        self.height = self.box_h
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.setStrokeColor(self.border)
        c.setLineWidth(2)
        c.roundRect(0, 0, self.box_width, self.box_h, 6, fill=1, stroke=1)
        self.content.drawOn(c, self.padding + 2, self.padding)


def make_styles():
    s = {}
    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=10, leading=16,
        textColor=DARK_GREY, alignment=TA_JUSTIFY,
        spaceAfter=8, spaceBefore=2)
    s['h1'] = ParagraphStyle('h1',
        fontName='Helvetica-Bold', fontSize=22, leading=28,
        textColor=DEEP_PURPLE, spaceBefore=20, spaceAfter=4)
    s['h2'] = ParagraphStyle('h2',
        fontName='Helvetica-Bold', fontSize=13, leading=19,
        textColor=DEEP_PURPLE, spaceBefore=18, spaceAfter=4)
    s['subtitle'] = ParagraphStyle('subtitle',
        fontName='Helvetica-Oblique', fontSize=11.5, leading=18,
        textColor=MID_GREY, alignment=TA_CENTER, spaceAfter=6)
    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=30, leading=38,
        textColor=WHITE, alignment=TA_CENTER)
    s['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='Helvetica-Oblique', fontSize=13, leading=20,
        textColor=LIGHT_PURPLE, alignment=TA_CENTER)
    s['note_text'] = ParagraphStyle('note_text',
        fontName='Helvetica', fontSize=9.5, leading=15,
        textColor=DARK_GREY)
    s['quote_text'] = ParagraphStyle('quote_text',
        fontName='Helvetica-Oblique', fontSize=10, leading=16,
        textColor=WHITE)
    s['tip_text'] = ParagraphStyle('tip_text',
        fontName='Helvetica', fontSize=9.5, leading=15,
        textColor=colors.HexColor('#1A0033'))
    s['table_header'] = ParagraphStyle('table_header',
        fontName='Helvetica-Bold', fontSize=9, leading=13,
        textColor=WHITE, alignment=TA_CENTER)
    s['table_cell'] = ParagraphStyle('table_cell',
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=DARK_GREY)
    s['meta_key'] = ParagraphStyle('meta_key',
        fontName='Helvetica-Bold', fontSize=9, leading=13,
        textColor=MED_PURPLE)
    s['meta_val'] = ParagraphStyle('meta_val',
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=DARK_GREY)
    return s


def process_text(text):
    # Extract backtick spans first to protect asterisks inside them
    placeholders = {}
    counter = [0]

    def protect_code(m):
        key = f'\x00CODE{counter[0]}\x00'
        inner = m.group(1).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        placeholders[key] = (
            f'<font name="Courier" color="#6A1B9A" backColor="#F3E5F5"> {inner} </font>'
        )
        counter[0] += 1
        return key

    text = re.sub(r'`([^`]+)`', protect_code, text)

    # Now safe to apply bold/italic — no asterisks inside code spans
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)

    # Restore code spans
    for key, val in placeholders.items():
        text = text.replace(key, val)

    return text


_mermaid_cache = {}

# Locate mmdc — check npm global prefix on Windows
def _find_mmdc():
    # Try PATH first
    found = shutil.which('mmdc')
    if found:
        return found
    # Windows npm global installs to AppData/Roaming/npm
    npm_path = os.path.expanduser(r'~\AppData\Roaming\npm\mmdc.cmd')
    if os.path.exists(npm_path):
        return npm_path
    return 'mmdc'

MMDC = _find_mmdc()


def render_mermaid(mermaid_code, avail_w):
    key = hash(mermaid_code)
    if key in _mermaid_cache:
        return _mermaid_cache[key]

    tmp_dir = tempfile.mkdtemp()
    src = os.path.join(tmp_dir, 'diagram.mmd')
    out = os.path.join(tmp_dir, 'diagram.png')

    # theme config for purple palette
    cfg = os.path.join(tmp_dir, 'config.json')
    with open(cfg, 'w') as f:
        f.write('{"theme":"base","themeVariables":{"primaryColor":"#E1BEE7","primaryTextColor":"#212121","primaryBorderColor":"#7B1FA2","lineColor":"#7B1FA2","secondaryColor":"#F3E5F5","tertiaryColor":"#fafafa"}}')

    with open(src, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)

    result = subprocess.run(
        [MMDC, '-i', src, '-o', out, '-c', cfg, '-b', 'white', '-w', '900'],
        capture_output=True, text=True, shell=(os.name == 'nt')
    )

    if result.returncode != 0 or not os.path.exists(out):
        print(f'mmdc error: {result.stderr[:200]}')
        _mermaid_cache[key] = None
        return None

    # scale to fit page width while keeping aspect ratio
    from PIL import Image as PILImage
    with PILImage.open(out) as im:
        img_w, img_h = im.size
    scale = avail_w / img_w
    img = Image(out, width=avail_w, height=img_h * scale)
    _mermaid_cache[key] = img
    return img


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ACCENT_LINE)
    canvas.setLineWidth(0.5)
    canvas.line(LEFT_M, BOT_M - 4, PAGE_W - RIGHT_M, BOT_M - 4)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MID_GREY)
    canvas.drawCentredString(PAGE_W / 2, BOT_M - 14,
        'Dual Multi-Agent System — Arquitetura e Origem   |   %d' % doc.page)
    canvas.restoreState()


def flush_table(table_rows, styles, avail_w):
    if not table_rows:
        return []
    items = []
    header = table_rows[0]
    data_rows = [r for r in table_rows[2:] if not all(re.match(r'^[-: ]+$', c.strip()) for c in r)]
    tdata = []
    tdata.append([Paragraph(process_text(c.strip()), styles['table_header']) for c in header])
    for row in data_rows:
        tdata.append([Paragraph(process_text(c.strip()), styles['table_cell']) for c in row])
    col_count = max(len(header), 1)
    col_w = avail_w / col_count
    t = Table(tdata, colWidths=[col_w] * col_count, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DEEP_PURPLE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, VERY_LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_PURPLE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    items.append(Spacer(1, 8))
    items.append(t)
    items.append(Spacer(1, 10))
    return items


def parse_markdown(md_text, styles, avail_w):
    story = []
    lines = md_text.split('\n')
    i = 0
    in_table = False
    table_rows = []

    def do_flush():
        nonlocal table_rows, in_table
        result = flush_table(table_rows, styles, avail_w)
        story.extend(result)
        table_rows = []
        in_table = False

    while i < len(lines):
        line = lines[i]

        # mermaid block — render with mmdc
        if line.strip().startswith('```mermaid'):
            if in_table:
                do_flush()
            i += 1
            mermaid_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                mermaid_lines.append(lines[i])
                i += 1
            mermaid_code = '\n'.join(mermaid_lines)
            story.append(Spacer(1, 10))
            img = render_mermaid(mermaid_code, avail_w)
            if img:
                story.append(img)
            else:
                # fallback to labeled box if rendering failed
                actors = []
                for ml in mermaid_lines:
                    m = re.search(r'participant \w+ as (.+)', ml)
                    if m:
                        actors.append(m.group(1).strip())
                    m2 = re.search(r'subgraph [^\[]*\["([^"]+)"', ml)
                    if m2:
                        actors.append(m2.group(1).strip())
                label = ' · '.join(actors[:5]) if actors else 'fluxo de agentes'
                p = Paragraph('<b>◆  Diagrama — </b>' + label, styles['note_text'])
                box = ColorBox(p, VERY_LIGHT, LIGHT_PURPLE, avail_w, padding=10)
                story.append(box)
            story.append(Spacer(1, 10))
            i += 1
            continue

        # generic code block — skip
        if line.strip().startswith('```'):
            if in_table:
                do_flush()
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                i += 1
            i += 1
            continue

        # table row
        if line.strip().startswith('|') and '|' in line:
            cells = [c for c in line.split('|')[1:-1]]
            if in_table:
                table_rows.append(cells)
            else:
                in_table = True
                table_rows = [cells]
            i += 1
            continue
        else:
            if in_table:
                do_flush()

        # hr
        if line.strip() == '---':
            story.append(Spacer(1, 6))
            story.append(DecorativeLine(avail_w, color=ACCENT_LINE, thickness=1))
            story.append(Spacer(1, 6))
            i += 1
            continue

        # admonitions
        if line.strip().startswith('!!!'):
            kind = 'note'
            if 'tip' in line:
                kind = 'tip'
            elif 'quote' in line:
                kind = 'quote'
            i += 1
            content_lines = []
            while i < len(lines) and (lines[i].startswith('    ') or lines[i].strip() == ''):
                content_lines.append(lines[i].strip())
                i += 1
            content = process_text(' '.join(content_lines).strip())
            if kind == 'note':
                p = Paragraph('<b>📌  Nota</b><br/>' + content, styles['note_text'])
                box = ColorBox(p, BLUE_NOTE, BLUE_NOTE_BDR, avail_w, padding=12)
            elif kind == 'tip':
                p = Paragraph('<b>💡  Dica</b><br/>' + content, styles['tip_text'])
                box = ColorBox(p, VERY_LIGHT, TIP_BDR, avail_w, padding=12)
            else:
                p = Paragraph('❝  ' + content, styles['quote_text'])
                box = ColorBox(p, QUOTE_BG, DEEP_PURPLE, avail_w, padding=16)
            story.append(Spacer(1, 8))
            story.append(box)
            story.append(Spacer(1, 8))
            continue

        # H1
        if re.match(r'^# [^#]', line):
            if in_table:
                do_flush()
            title = line[2:].strip()
            story.append(Paragraph(process_text(title), styles['h1']))
            story.append(DecorativeLine(avail_w, color=MED_PURPLE, thickness=2.5))
            story.append(Spacer(1, 4))
            i += 1
            continue

        # H2
        if re.match(r'^## ', line):
            if in_table:
                do_flush()
            title = line[3:].strip()
            story.append(Spacer(1, 6))
            story.append(Paragraph(process_text(title), styles['h2']))
            story.append(DecorativeLine(avail_w, color=LIGHT_PURPLE, thickness=1))
            story.append(Spacer(1, 2))
            i += 1
            continue

        # italic-only line (subtitle)
        if re.match(r'^\*[^*].+[^*]\*$', line.strip()):
            text = line.strip()[1:-1]
            story.append(Paragraph('<i>' + process_text(text) + '</i>', styles['subtitle']))
            story.append(Spacer(1, 4))
            i += 1
            continue

        # empty
        if line.strip() == '':
            story.append(Spacer(1, 4))
            i += 1
            continue

        # regular paragraph
        if line.strip():
            if in_table:
                do_flush()
            story.append(Paragraph(process_text(line.strip()), styles['body']))
            i += 1
            continue

        i += 1

    if in_table:
        do_flush()

    return story


def build_pdf(md_path, out_path):
    styles = make_styles()
    avail_w = PAGE_W - LEFT_M - RIGHT_M

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=LEFT_M, rightMargin=RIGHT_M,
        topMargin=TOP_M, bottomMargin=BOT_M,
        title='Dual Multi-Agent System — Arquitetura e Origem',
        author='Guilherme Giuliano Nicolau',
        subject='Arquitetura de sistemas multi-agentes duais com Claude Code',
    )

    story = []

    # ── COVER ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 2.5 * cm))

    cover_block = Table(
        [[Paragraph('Dual Multi-Agent System', styles['cover_title'])]],
        colWidths=[avail_w])
    cover_block.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DEEP_PURPLE),
        ('TOPPADDING', (0, 0), (-1, -1), 30),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 30),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(cover_block)
    story.append(Spacer(1, 14))

    story.append(Paragraph('Arquitetura e Origem', styles['subtitle']))
    story.append(Spacer(1, 8))
    story.append(DecorativeLine(avail_w, color=MED_PURPLE, thickness=2))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        '<i>Como a maturidade dos modelos de linguagem e a convergência de ferramentas '
        'tornaram possível um padrão inédito de orquestração: o mesmo time de agentes '
        'construindo e executando o produto simultaneamente.</i>',
        styles['subtitle']))
    story.append(Spacer(1, 2.5 * cm))
    story.append(DecorativeLine(avail_w, color=ACCENT_LINE, thickness=0.5))
    story.append(Spacer(1, 14))

    meta_rows = [
        ['Domínio', 'Arquitetura de sistemas multi-agentes'],
        ['Autor', 'Guilherme Giuliano Nicolau'],
        ['Ano', '2026'],
    ]
    meta_data = [
        [Paragraph(k, styles['meta_key']), Paragraph(v, styles['meta_val'])]
        for k, v in meta_rows
    ]
    meta_table = Table(meta_data, colWidths=[3.2 * cm, avail_w - 3.2 * cm])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, LIGHT_PURPLE),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # ── CONTENT ────────────────────────────────────────────────────────────
    md_text = open(md_path, encoding='utf-8').read()
    lines = md_text.split('\n')
    # skip title line and its italic subtitle (already on cover)
    start = 0
    for j, l in enumerate(lines[:6]):
        if l.strip().startswith('*') and l.strip().endswith('*'):
            start = j + 1
            break
    md_body = '\n'.join(lines[start:])

    story.extend(parse_markdown(md_body, styles, avail_w))

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print('PDF gerado:', out_path)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    build_pdf(
        os.path.join(here, 'dual-system.md'),
        os.path.join(here, 'dual-system.pdf'),
    )
