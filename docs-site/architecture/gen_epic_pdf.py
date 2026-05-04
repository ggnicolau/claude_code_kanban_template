import html
import os
import re
import textwrap
import unicodedata

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable

from gen_pdf import (
    A4,
    ACCENT_LINE,
    BLUE_NOTE,
    BLUE_NOTE_BDR,
    BOT_M,
    ColorBox,
    DARK_GREY,
    DecorativeLine,
    DEEP_PURPLE,
    LEFT_M,
    LIGHT_GREY,
    LIGHT_PURPLE,
    MED_PURPLE,
    MID_GREY,
    PAGE_W,
    QUOTE_BG,
    RIGHT_M,
    TIP_BDR,
    TOP_M,
    VERY_LIGHT,
    WHITE,
    flush_table,
    make_styles,
    process_text,
    render_mermaid,
)


DOC_TITLE = 'Dual Agent SaaS Beta'
DOC_SUBTITLE = 'Encapsulamento comercial do Dual Multi-Agent System'
DOC_DESCRIPTION = (
    'Service-as-a-Product entregue como plataforma gerenciada: '
    'sistema privado, UI controlada, GitHub do cliente e agentes governados.'
)
AUTHOR = 'Guilherme Giuliano Nicolau'
YEAR = '2026'

INDEX_ITEMS = [
    ('Contexto e tese de produto', 'Contexto'),
    ('Diferenciação e hipótese de mercado', 'Diferenciação e hipótese de mercado'),
    ('Template atual e capacidades existentes', 'O que o template atual já entrega'),
    ('Objetivo e arquitetura alvo', 'Objetivo'),
    ('Separação system/platform/project', 'Separação de domínios'),
    ('Dual-plane: construção e execução', 'Dual-plane support: construção e execução'),
    ('UI, executor e ferramentas avaliadas', 'Avaliação de opções reais de UI e executor'),
    ('API, fluxos, isolamento e GitHub', 'Backend/API própria'),
    ('Infraestrutura beta', 'Infraestrutura beta'),
    ('Modelo comercial e posicionamento', 'Modelo comercial beta'),
    ('Cronograma, riscos e critérios de aceite', 'Estimativa de prazo'),
    ('Resultado esperado', 'Resultado esperado'),
]


def slugify(text):
    normalized = unicodedata.normalize('NFKD', text)
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', ascii_text).strip('-').lower()
    return slug or 'section'


class Bookmark(Flowable):
    def __init__(self, name, title=None, level=0):
        super().__init__()
        self.name = name
        self.title = title
        self.level = level

    def wrap(self, avail_width, avail_height):
        return 0, 0

    def draw(self):
        self.canv.bookmarkPage(self.name)
        if self.title:
            self.canv.addOutlineEntry(self.title, self.name, level=self.level, closed=False)


def make_epic_styles():
    styles = make_styles()
    styles['code_block'] = ParagraphStyle(
        'code_block',
        fontName='Courier',
        fontSize=7.6,
        leading=10,
        textColor=DARK_GREY,
        alignment=TA_LEFT,
        spaceBefore=0,
        spaceAfter=0,
    )
    styles['h3'] = ParagraphStyle(
        'h3',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=15,
        textColor=MED_PURPLE,
        spaceBefore=10,
        spaceAfter=3,
    )
    styles['bullet_text'] = ParagraphStyle(
        'bullet_text',
        fontName='Helvetica',
        fontSize=9.6,
        leading=14,
        textColor=DARK_GREY,
        alignment=TA_LEFT,
        spaceAfter=0,
        spaceBefore=0,
    )
    styles['ordered_num'] = ParagraphStyle(
        'ordered_num',
        fontName='Helvetica-Bold',
        fontSize=9.2,
        leading=13,
        textColor=MED_PURPLE,
        alignment=TA_CENTER,
    )
    styles['index_item'] = ParagraphStyle(
        'index_item',
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=DARK_GREY,
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    styles['flow_node'] = ParagraphStyle(
        'flow_node',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=DARK_GREY,
        alignment=TA_CENTER,
    )
    styles['flow_arrow'] = ParagraphStyle(
        'flow_arrow',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=MED_PURPLE,
        alignment=TA_CENTER,
    )
    styles['caption'] = ParagraphStyle(
        'caption',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=MED_PURPLE,
        alignment=TA_LEFT,
    )
    styles['mono_small'] = ParagraphStyle(
        'mono_small',
        fontName='Courier',
        fontSize=7.4,
        leading=9.5,
        textColor=DARK_GREY,
        alignment=TA_LEFT,
    )
    styles['chip'] = ParagraphStyle(
        'chip',
        fontName='Courier-Bold',
        fontSize=8.2,
        leading=10,
        textColor=DEEP_PURPLE,
        alignment=TA_CENTER,
    )
    return styles


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(ACCENT_LINE)
    canvas.setLineWidth(0.5)
    canvas.line(LEFT_M, BOT_M - 4, PAGE_W - RIGHT_M, BOT_M - 4)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MID_GREY)
    canvas.drawCentredString(PAGE_W / 2, BOT_M - 14, '%s   |   %d' % (DOC_TITLE, doc.page))
    canvas.restoreState()


def build_linked_index(styles, avail_w):
    story = [
        Bookmark('indice', 'Índice', 0),
        Paragraph('Índice', styles['h1']),
        DecorativeLine(avail_w, color=MED_PURPLE, thickness=2.5),
        Spacer(1, 8),
    ]
    for idx, (label, target_title) in enumerate(INDEX_ITEMS, 1):
        target = slugify(target_title)
        text = '<a href="#%s"><font color="#4A148C">%d. %s</font></a>' % (
            html.escape(target),
            idx,
            html.escape(label),
        )
        story.append(Paragraph(text, styles['index_item']))
    story.append(PageBreak())
    return story


def strip_markdown_index(md_text):
    lines = md_text.split('\n')
    start = 0
    while start < len(lines) and lines[start].strip() == '':
        start += 1

    if start >= len(lines) or lines[start].strip() != '## Índice':
        return md_text
    i = start + 1
    while i < len(lines):
        if lines[i].strip() == '---':
            return '\n'.join(lines[:start] + lines[i + 1:])
        i += 1
    return md_text


def render_code_block(code, styles, avail_w, language=''):
    label = language.strip() or 'text'
    lines = []
    for raw_line in code.splitlines() or ['']:
        if raw_line == '':
            lines.append('')
            continue
        lines.extend(textwrap.wrap(
            raw_line,
            width=86,
            replace_whitespace=False,
            drop_whitespace=False,
            break_long_words=True,
            break_on_hyphens=False,
        ))

    escaped = '<br/>'.join(html.escape(line).replace(' ', '&nbsp;') for line in lines)
    label_para = Paragraph('<b>%s</b>' % html.escape(label), styles['meta_key'])
    code_para = Paragraph(escaped, styles['code_block'])
    table = Table(
        [[label_para], [code_para]],
        colWidths=[avail_w],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), VERY_LIGHT),
            ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GREY),
            ('BOX', (0, 0), (-1, -1), 0.6, LIGHT_PURPLE),
            ('LINEBELOW', (0, 0), (-1, 0), 0.6, LIGHT_PURPLE),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 9),
            ('RIGHTPADDING', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]),
    )
    return table


def _paragraph_cell(text, style):
    return Paragraph(process_text(text.strip()), style)


def _looks_like_flow(lines):
    clean = [l.strip() for l in lines if l.strip()]
    return len(clean) >= 3 and any(l in ('↓', '->', '+') for l in clean)


def _looks_like_tree(lines):
    joined = '\n'.join(lines)
    return any(token in joined for token in ['├', '└', '│', '/opt/', 'Repo privado', 'system/', 'platform/'])


def _looks_like_commands(lines):
    clean = [l.strip() for l in lines if l.strip()]
    return clean and all(l.startswith('/') and ' ' not in l for l in clean)


def _looks_like_http(lines):
    return any(re.match(r'^(GET|POST|PUT|PATCH|DELETE)\s+/', l.strip()) for l in lines)


def _looks_like_checklist(lines):
    clean = [l.strip() for l in lines if l.strip()]
    return len(clean) >= 3 and all(l.startswith('- [ ] ') for l in clean)


def render_flow_block(lines, styles, avail_w):
    nodes = []
    connectors = {'↓', '->', '+'}
    for line in lines:
        clean = line.strip()
        if not clean or clean in connectors:
            continue
        nodes.append(clean)

    rows = []
    for idx, node in enumerate(nodes):
        rows.append([Paragraph(process_text(node), styles['flow_node'])])
        if idx < len(nodes) - 1:
            rows.append([Paragraph('↓', styles['flow_arrow'])])

    table = Table(rows, colWidths=[avail_w * 0.74], hAlign='CENTER')
    style_cmds = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    for idx in range(0, len(rows), 2):
        style_cmds.extend([
            ('BACKGROUND', (0, idx), (0, idx), VERY_LIGHT),
            ('BOX', (0, idx), (0, idx), 0.8, LIGHT_PURPLE),
            ('LEFTPADDING', (0, idx), (0, idx), 10),
            ('RIGHTPADDING', (0, idx), (0, idx), 10),
        ])
    table.setStyle(TableStyle(style_cmds))
    return KeepTogether([Spacer(1, 6), table, Spacer(1, 8)])


def render_tree_block(lines, styles, avail_w, language='text'):
    caption = Paragraph('<b>%s</b>' % html.escape(language or 'estrutura'), styles['caption'])
    body = '<br/>'.join(
        html.escape(line).replace(' ', '&nbsp;')
        for line in lines
    )
    table = Table(
        [[caption], [Paragraph(body, styles['mono_small'])]],
        colWidths=[avail_w],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), VERY_LIGHT),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#FBF8FC')),
            ('BOX', (0, 0), (-1, -1), 0.6, LIGHT_PURPLE),
            ('LINEBELOW', (0, 0), (-1, 0), 0.6, LIGHT_PURPLE),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]),
    )
    return KeepTogether([Spacer(1, 6), table, Spacer(1, 8)])


def render_chip_block(lines, styles, avail_w, label):
    items = [l.strip() for l in lines if l.strip()]
    cols = 2 if len(items) > 5 else 1
    rows = []
    for i in range(0, len(items), cols):
        row = []
        for item in items[i:i + cols]:
            row.append(Paragraph(html.escape(item), styles['chip']))
        while len(row) < cols:
            row.append('')
        rows.append(row)
    col_widths = [avail_w / cols] * cols
    table = Table(rows, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), VERY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.6, LIGHT_PURPLE),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, LIGHT_PURPLE),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    header = Paragraph('<b>%s</b>' % label, styles['caption'])
    return KeepTogether([Spacer(1, 6), header, Spacer(1, 3), table, Spacer(1, 8)])


def render_checklist_block(lines, styles, avail_w):
    rows = []
    for line in lines:
        item = line.strip()
        if not item:
            continue
        item = item.replace('- [ ] ', '', 1)
        rows.append([
            Paragraph('□', styles['caption']),
            Paragraph(process_text(item), styles['table_cell']),
        ])
    table = Table(rows, colWidths=[0.7 * cm, avail_w - 0.7 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), WHITE),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, VERY_LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.3, LIGHT_PURPLE),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return KeepTogether([Spacer(1, 6), table, Spacer(1, 8)])


def render_bullet_block(items, styles, avail_w):
    rows = []
    for item in items:
        rows.append([
            Paragraph('•', styles['caption']),
            Paragraph(process_text(item), styles['bullet_text']),
        ])
    table = Table(rows, colWidths=[0.45 * cm, avail_w - 0.45 * cm], hAlign='LEFT')
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    return KeepTogether([table, Spacer(1, 5)])


def render_ordered_block(items, styles, avail_w):
    rows = []
    for num, item in items:
        rows.append([
            Paragraph(num + '.', styles['ordered_num']),
            Paragraph(process_text(item), styles['bullet_text']),
        ])
    table = Table(rows, colWidths=[0.65 * cm, avail_w - 0.65 * cm], hAlign='LEFT')
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    return KeepTogether([table, Spacer(1, 6)])


def render_epic_block(code, styles, avail_w, language=''):
    lines = code.strip('\n').splitlines()
    if _looks_like_checklist(lines):
        return render_checklist_block(lines, styles, avail_w)
    if _looks_like_commands(lines):
        return render_chip_block(lines, styles, avail_w, 'Comandos')
    if language == 'http' or _looks_like_http(lines):
        return render_chip_block(lines, styles, avail_w, 'Endpoints')
    if _looks_like_flow(lines) and not _looks_like_tree(lines):
        return render_flow_block(lines, styles, avail_w)
    if _looks_like_tree(lines):
        return render_tree_block(lines, styles, avail_w, language or 'estrutura')
    if len([l for l in lines if l.strip()]) <= 2:
        text = '<br/>'.join(html.escape(l) for l in lines)
        p = Paragraph(text, styles['note_text'])
        return KeepTogether([Spacer(1, 6), ColorBox(p, VERY_LIGHT, LIGHT_PURPLE, avail_w, padding=10), Spacer(1, 8)])
    return render_code_block(code, styles, avail_w, language)


def parse_markdown(md_text, styles, avail_w):
    story = []
    lines = md_text.split('\n')
    i = 0
    in_table = False
    table_rows = []

    def do_flush():
        nonlocal table_rows, in_table
        story.extend(flush_table(table_rows, styles, avail_w))
        table_rows = []
        in_table = False

    while i < len(lines):
        line = lines[i]

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
                p = Paragraph('<b>Diagrama</b><br/>Mermaid indisponivel no build local.', styles['note_text'])
                story.append(ColorBox(p, VERY_LIGHT, LIGHT_PURPLE, avail_w, padding=10))
            story.append(Spacer(1, 10))
            i += 1
            continue

        fence_match = re.match(r'^\s*```([A-Za-z0-9_-]*)\s*$', line)
        if fence_match:
            if in_table:
                do_flush()
            language = fence_match.group(1)
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            story.append(Spacer(1, 6))
            story.append(render_epic_block('\n'.join(code_lines), styles, avail_w, language))
            story.append(Spacer(1, 8))
            i += 1
            continue

        if line.strip().startswith('|') and '|' in line:
            cells = [c for c in line.split('|')[1:-1]]
            if in_table:
                table_rows.append(cells)
            else:
                in_table = True
                table_rows = [cells]
            i += 1
            continue
        elif in_table:
            do_flush()

        if line.strip() == '---':
            story.append(Spacer(1, 6))
            story.append(DecorativeLine(avail_w, color=ACCENT_LINE, thickness=1))
            story.append(Spacer(1, 6))
            i += 1
            continue

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
                p = Paragraph('<b>Nota</b><br/>' + content, styles['note_text'])
                box = ColorBox(p, BLUE_NOTE, BLUE_NOTE_BDR, avail_w, padding=12)
            elif kind == 'tip':
                p = Paragraph('<b>Dica</b><br/>' + content, styles['tip_text'])
                box = ColorBox(p, VERY_LIGHT, TIP_BDR, avail_w, padding=12)
            else:
                p = Paragraph(content, styles['quote_text'])
                box = ColorBox(p, QUOTE_BG, DEEP_PURPLE, avail_w, padding=16)
            story.append(Spacer(1, 8))
            story.append(box)
            story.append(Spacer(1, 8))
            continue

        if re.match(r'^# [^#]', line):
            if in_table:
                do_flush()
            title = line[2:].strip()
            story.append(Paragraph(process_text(title), styles['h1']))
            story.append(DecorativeLine(avail_w, color=MED_PURPLE, thickness=2.5))
            story.append(Spacer(1, 4))
            i += 1
            continue

        if re.match(r'^## ', line):
            if in_table:
                do_flush()
            title = line[3:].strip()
            story.append(Spacer(1, 6))
            story.append(Bookmark(slugify(title), title, 0))
            story.append(Paragraph(process_text(title), styles['h2']))
            story.append(DecorativeLine(avail_w, color=LIGHT_PURPLE, thickness=1))
            story.append(Spacer(1, 2))
            i += 1
            continue

        if re.match(r'^### ', line):
            if in_table:
                do_flush()
            title = line[4:].strip()
            story.append(Spacer(1, 4))
            story.append(Bookmark(slugify(title), title, 1))
            story.append(Paragraph(process_text(title), styles['h3']))
            i += 1
            continue

        if line.strip().startswith('> '):
            if in_table:
                do_flush()
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:].strip())
                i += 1
            content = process_text(' '.join(quote_lines))
            p = Paragraph(content, styles['quote_text'])
            story.append(Spacer(1, 6))
            story.append(ColorBox(p, QUOTE_BG, DEEP_PURPLE, avail_w, padding=14))
            story.append(Spacer(1, 8))
            continue

        if re.match(r'^\s*-\s+', line):
            if in_table:
                do_flush()
            items = []
            while i < len(lines) and re.match(r'^\s*-\s+', lines[i]):
                items.append(re.sub(r'^\s*-\s+', '', lines[i]).strip())
                i += 1
            story.append(render_bullet_block(items, styles, avail_w))
            continue

        if re.match(r'^\s*\d+\.\s+', line):
            if in_table:
                do_flush()
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                m = re.match(r'^\s*(\d+)\.\s+(.+)$', lines[i])
                items.append((m.group(1), m.group(2).strip()))
                i += 1
            story.append(render_ordered_block(items, styles, avail_w))
            continue

        if re.match(r'^\*[^*].+[^*]\*$', line.strip()):
            text = line.strip()[1:-1]
            story.append(Paragraph('<i>' + process_text(text) + '</i>', styles['subtitle']))
            story.append(Spacer(1, 4))
            i += 1
            continue

        if line.strip() == '':
            story.append(Spacer(1, 4))
            i += 1
            continue

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
    styles = make_epic_styles()
    avail_w = PAGE_W - LEFT_M - RIGHT_M

    doc = SimpleDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=LEFT_M,
        rightMargin=RIGHT_M,
        topMargin=TOP_M,
        bottomMargin=BOT_M,
        title=DOC_TITLE,
        author=AUTHOR,
        subject='Epic beta para produto web B2B do Dual Multi-Agent System',
    )

    story = []
    story.append(Spacer(1, 2.5 * cm))

    cover_block = Table([[Paragraph(DOC_TITLE, styles['cover_title'])]], colWidths=[avail_w])
    cover_block.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DEEP_PURPLE),
        ('TOPPADDING', (0, 0), (-1, -1), 30),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 30),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(cover_block)
    story.append(Spacer(1, 14))
    story.append(Paragraph(DOC_SUBTITLE, styles['subtitle']))
    story.append(Spacer(1, 8))
    story.append(DecorativeLine(avail_w, color=MED_PURPLE, thickness=2))
    story.append(Spacer(1, 14))
    story.append(Paragraph('<i>%s</i>' % DOC_DESCRIPTION, styles['subtitle']))
    story.append(Spacer(1, 2.5 * cm))
    story.append(DecorativeLine(avail_w, color=ACCENT_LINE, thickness=0.5))
    story.append(Spacer(1, 14))

    meta_rows = [
        ['Dominio', 'Produto, engenharia, agentes e governanca'],
        ['Documento', 'Epic beta / Product-as-a-Service'],
        ['Autor', AUTHOR],
        ['Ano', YEAR],
    ]
    meta_data = [[Paragraph(k, styles['meta_key']), Paragraph(v, styles['meta_val'])] for k, v in meta_rows]
    meta_table = Table(meta_data, colWidths=[3.2 * cm, avail_w - 3.2 * cm])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, LIGHT_PURPLE),
    ]))
    story.append(meta_table)
    story.append(PageBreak())
    story.extend(build_linked_index(styles, avail_w))

    with open(md_path, encoding='utf-8') as f:
        md_text = f.read()
    lines = md_text.split('\n')
    md_body = '\n'.join(lines[1:]) if lines and lines[0].startswith('# ') else md_text
    md_body = strip_markdown_index(md_body)
    story.extend(parse_markdown(md_body, styles, avail_w))

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print('PDF gerado:', out_path)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    build_pdf(
        os.path.join(here, 'EPIC_dual-agent-saas-beta.md'),
        os.path.join(here, 'EPIC_dual-agent-saas-beta.pdf'),
    )
