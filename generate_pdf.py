"""
TrustGuard – PROJECT_DOCUMENTATION.md → PDF
Uses: fpdf2 (pure Python, no GTK/Pango required)
"""

import os
import re
from fpdf import FPDF, XPos, YPos

MD_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PROJECT_DOCUMENTATION.md")
PDF_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TrustGuard_Project_Documentation.pdf")

# ── Colour palette ──────────────────────────────────────────────────────────
C_BRAND      = (79,  70,  229)   # indigo-600
C_BRAND_DARK = (49,  46, 129)   # indigo-900
C_SLATE_900  = (15,  23,  42)
C_SLATE_800  = (30,  41,  59)
C_SLATE_700  = (51,  65,  85)
C_SLATE_500  = (100, 116, 139)
C_SLATE_200  = (226, 232, 240)
C_SLATE_100  = (241, 245, 249)
C_SLATE_50   = (248, 250, 252)
C_WHITE      = (255, 255, 255)
C_EMERALD    = (16,  185, 129)
C_ROSE       = (244,  63,  94)
C_CODE_BG    = (15,  23,  42)
C_CODE_FG    = (226, 232, 240)
C_AMBER_BG   = (254, 249, 195)
C_AMBER_FG   = (113,  63,  18)

# ── PDF class ────────────────────────────────────────────────────────────────
class TrustGuardPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 18, 20)
        self.page_num   = 0
        self.in_code    = False
        self.in_table   = False
        self.table_rows = []
        self.col_widths = []

    # ── Header & Footer ─────────────────────────────────────────────────────
    def header(self):
        if self.page_no() <= 1:
            return
        self.set_font('Helvetica', 'B', 7)
        self.set_text_color(*C_SLATE_500)
        self.cell(0, 6, 'TrustGuard - Smarter Shopping, Fewer Fakes', align='L')
        self.ln(0.5)
        self.set_draw_color(*C_SLATE_200)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

    def footer(self):
        if self.page_no() <= 1:
            return
        self.set_y(-14)
        self.set_draw_color(*C_SLATE_200)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(1)
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*C_SLATE_500)
        self.cell(0, 5, f'IEEE Technosphere Ideathon 2026  ·  Page {self.page_no()}', align='C')

    # ── Cover page ──────────────────────────────────────────────────────────
    def cover(self):
        self.add_page()

        # Dark header band
        self.set_fill_color(*C_BRAND_DARK)
        self.rect(0, 0, 210, 70, 'F')

        # IEEE badge
        self.set_xy(0, 20)
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*C_WHITE)
        self.cell(210, 8, 'IEEE TECHNOSPHERE IDEATHON 2026', align='C')

        # Main title
        self.set_xy(0, 32)
        self.set_font('Helvetica', 'B', 34)
        self.set_text_color(*C_WHITE)
        self.cell(210, 20, 'TrustGuard', align='C')

        # Subtitle accent bar
        bar_w, bar_h = 50, 2.5
        self.set_fill_color(*C_EMERALD)
        self.rect((210 - bar_w) / 2, 55, bar_w, bar_h, 'F')

        # Tagline
        self.set_xy(0, 60)
        self.set_font('Helvetica', 'I', 13)
        self.set_text_color(200, 200, 255)
        self.cell(210, 10, 'Smarter Shopping, Fewer Fakes', align='C')

        # White content area
        self.set_fill_color(*C_WHITE)

        # Description box
        self.set_xy(30, 82)
        self.set_font('Helvetica', '', 11)
        self.set_text_color(*C_SLATE_700)
        self.multi_cell(150, 7,
            'AI-Powered Fake Review Detection Platform\n'
            'for E-Commerce Products & Restaurant Reviews',
            align='C')

        # Info box
        box_y = 106
        self.set_fill_color(*C_SLATE_50)
        self.set_draw_color(*C_SLATE_200)
        self.set_line_width(0.4)
        self.rect(25, box_y, 160, 66, 'FD')

        rows = [
            ('Tech Stack',  'React 18 + FastAPI + scikit-learn + Supabase PostgreSQL'),
            ('ML Models',   'TF-IDF + LogReg (84.5% F1) · DistilBERT (93.3% F1)'),
            ('Coverage',    'Amazon · Flipkart · Google Maps Restaurants'),
            ('XAI',         'SHAP-Inspired Token Attribution + Phrase Highlighting'),
            ('Database',    'SQLite (Development)  ·  Supabase PostgreSQL (Production)'),
            ('Architecture','FastAPI REST API · React SPA · SQLAlchemy ORM'),
        ]
        y = box_y + 6
        for label, value in rows:
            self.set_xy(30, y)
            self.set_font('Helvetica', 'B', 9)
            self.set_text_color(*C_BRAND)
            self.cell(38, 6, label + ':', align='L')
            self.set_font('Helvetica', '', 9)
            self.set_text_color(*C_SLATE_800)
            self.cell(140, 6, value, align='L')
            y += 9

        # Divider
        self.set_draw_color(*C_SLATE_200)
        self.line(25, 178, 185, 178)

        # Footer note
        self.set_xy(0, 181)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*C_SLATE_500)
        self.cell(210, 6, 'Complete Project Documentation  ·  August 2026  ·  Confidential', align='C')

        # GitHub / stack icon row
        self.set_xy(0, 190)
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*C_BRAND)
        self.cell(210, 6,
            '27 Sections  ·  43 Features Documented  ·  50 Judge Q&A Pairs  ·  Full PPT Scripts',
            align='C')

    # ── Helpers ─────────────────────────────────────────────────────────────
    def rgb(self, r, g, b):
        return (r, g, b)

    def _safe(self, txt):
        return (txt
                .replace('\u2013', '-').replace('\u2014', '--')
                .replace('\u2018', "'").replace('\u2019', "'")
                .replace('\u201c', '"').replace('\u201d', '"')
                .replace('\u2022', '*').replace('\u2026', '...')
                .replace('\u2192', '->').replace('\u2190', '<-')
                .replace('\u03a3', 'E').replace('\u2265', '>=')
                .replace('\u2264', '<=').replace('\u00d7', 'x')
                .replace('\u2212', '-').replace('\u00b0', 'deg')
                .replace('\u00ae', '(R)').replace('\u2122', '(TM)')
                .replace('\u00a9', '(c)').replace('\u00b7', '.')
                .replace('\u2605', '*').replace('\u2606', '*')
                .replace('\u2713', '[OK]').replace('\u2717', '[X]')
                .replace('\u274c', '[X]').replace('\u2705', '[OK]')
                .replace('\u26a0', '[!]').replace('\u2728', '*')
                .replace('\u2139', '[i]').replace('\u1f50d', '[S]')
                .replace('\u00e9', 'e').replace('\u00e8', 'e')
                .replace('\u00ea', 'e').replace('\u00e0', 'a')
                .replace('\u00e2', 'a').replace('\u00f4', 'o')
                .replace('\u00fb', 'u').replace('\u00ee', 'i')
                .replace('\u00ef', 'i').replace('\u00e7', 'c')
                )

    def _strip_emoji(self, txt):
        # Remove emoji / non-latin chars that fpdf2 can't render
        return re.sub(r'[^\x00-\x7F\u00C0-\u024F]', '', txt)

    def safe(self, txt):
        return self._strip_emoji(self._safe(txt))

    def section_h1(self, text):
        """Chapter heading with brand colour stripe."""
        self.ln(4)
        # Accent bar
        self.set_fill_color(*C_BRAND)
        self.rect(self.l_margin, self.get_y(), 170, 1.2, 'F')
        self.ln(2)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(*C_BRAND_DARK)
        self.multi_cell(0, 9, self.safe(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        self.set_draw_color(*C_SLATE_200)
        self.ln(1)

    def section_h2(self, text):
        self.ln(4)
        self.set_fill_color(*C_SLATE_100)
        y = self.get_y()
        self.rect(self.l_margin, y, 170, 8, 'F')
        self.set_fill_color(*C_BRAND)
        self.rect(self.l_margin, y, 3, 8, 'F')
        self.set_xy(self.l_margin + 5, y)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*C_BRAND_DARK)
        self.cell(165, 8, self.safe(text))
        self.ln(8)

    def section_h3(self, text):
        self.ln(3)
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(*C_SLATE_800)
        self.multi_cell(0, 7, self.safe(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def section_h4(self, text):
        self.ln(2)
        self.set_font('Helvetica', 'BI', 10)
        self.set_text_color(*C_SLATE_700)
        self.multi_cell(0, 6, self.safe(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def body_text(self, text, indent=0):
        text = self.safe(text)
        if not text.strip():
            self.ln(2)
            return
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*C_SLATE_800)
        self.set_x(self.l_margin + indent)
        self.multi_cell(170 - indent, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def bullet_item(self, text, level=0):
        text = self.safe(text)
        indent = 5 + level * 6
        bullet = '-'
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*C_BRAND)
        self.set_x(self.l_margin + indent)
        self.cell(5, 5.5, bullet)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*C_SLATE_800)
        self.multi_cell(165 - indent, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def code_block(self, lines):
        if not lines:
            return
        self.ln(2)
        # Calculate height
        n_lines = len(lines)
        h_per_line = 4.5
        block_h = min(n_lines * h_per_line + 8, 120)  # cap at 120mm

        self.set_fill_color(*C_CODE_BG)
        self.set_draw_color(*C_BRAND)
        self.set_line_width(0.5)
        x0, y0 = self.l_margin, self.get_y()
        self.rect(x0, y0, 170, block_h, 'FD')

        self.set_xy(x0 + 4, y0 + 3)
        self.set_font('Courier', '', 7.5)
        self.set_text_color(*C_CODE_FG)
        rendered = 0
        for line in lines:
            line_s = self.safe(line)
            if rendered * h_per_line + 10 > block_h:
                self.set_xy(x0 + 4, self.get_y())
                self.set_font('Courier', 'I', 7)
                self.cell(160, h_per_line, '... (truncated for display) ...')
                self.ln(h_per_line)
                break
            self.set_xy(x0 + 4, y0 + 3 + rendered * h_per_line)
            self.cell(162, h_per_line, line_s[:130])
            rendered += 1

        self.set_xy(x0, y0 + block_h + 1)
        self.ln(3)

    def horizontal_rule(self):
        self.ln(2)
        self.set_draw_color(*C_SLATE_200)
        self.set_line_width(0.4)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(4)

    def render_table(self, rows):
        if not rows or len(rows) < 2:
            return
        header = rows[0]
        n_cols = len(header)
        avail  = 170
        col_w  = avail / n_cols

        self.ln(2)
        # Header row
        self.set_fill_color(*C_SLATE_800)
        self.set_text_color(*C_WHITE)
        self.set_font('Helvetica', 'B', 8)
        x0 = self.l_margin
        for i, cell_txt in enumerate(header):
            self.set_xy(x0 + i * col_w, self.get_y())
            self.cell(col_w, 6.5, self.safe(cell_txt)[:40], border=1, fill=True)
        self.ln(6.5)

        # Data rows
        for r_idx, row in enumerate(rows[1:]):
            if self.get_y() > 265:
                self.add_page()
            fill_color = C_SLATE_50 if r_idx % 2 == 0 else C_WHITE
            self.set_fill_color(*fill_color)
            self.set_text_color(*C_SLATE_800)
            self.set_font('Helvetica', '', 8)
            row_y = self.get_y()
            # Compute row height
            max_h = 6
            cells_text = []
            for cell_txt in row:
                t = self.safe(str(cell_txt))[:60]
                cells_text.append(t)
            for i, t in enumerate(cells_text):
                self.set_xy(x0 + i * col_w, row_y)
                self.cell(col_w, max_h, t, border=1, fill=True)
            self.ln(max_h)
        self.ln(3)


# ── Parse and render markdown ────────────────────────────────────────────────
def render_md(pdf: TrustGuardPDF, md_text: str):
    lines = md_text.splitlines()
    i = 0
    code_buf   = []
    in_code    = False
    table_buf  = []
    in_table   = False
    list_stack = []  # stack of (level, ordered)

    def flush_table():
        nonlocal table_buf, in_table
        if table_buf:
            # Filter separator rows (---|--- rows)
            clean = [r for r in table_buf if not all(
                re.match(r'^\s*:?-+:?\s*$', c) for c in r
            )]
            pdf.render_table(clean)
        table_buf = []
        in_table  = False

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        # ── Code fence ───────────────────────────────────────────
        if stripped.startswith('```'):
            if not in_code:
                in_code   = True
                code_buf  = []
                if in_table:
                    flush_table()
            else:
                in_code = False
                pdf.code_block(code_buf)
                code_buf = []
            i += 1
            continue

        if in_code:
            code_buf.append(raw)
            i += 1
            continue

        # ── Table ─────────────────────────────────────────────────
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            table_buf.append(cells)
            i += 1
            continue
        else:
            if in_table:
                flush_table()

        # ── Horizontal rule ───────────────────────────────────────
        if re.match(r'^(-{3,}|={3,}|\*{3,})$', stripped):
            pdf.horizontal_rule()
            i += 1
            continue

        # ── Headings ──────────────────────────────────────────────
        m = re.match(r'^(#{1,6})\s+(.*)', stripped)
        if m:
            level = len(m.group(1))
            text  = m.group(2)
            # Remove markdown links and bold from headings
            text  = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
            text  = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
            text  = re.sub(r'`([^`]+)`', r'\1', text)
            if pdf.get_y() > 250 and level <= 2:
                pdf.add_page()
            if   level == 1: pdf.section_h1(text)
            elif level == 2: pdf.section_h2(text)
            elif level == 3: pdf.section_h3(text)
            else:            pdf.section_h4(text)
            i += 1
            continue

        # ── Bullet / numbered list items ─────────────────────────
        m_ul = re.match(r'^(\s*)[-*+]\s+(.*)', raw)
        m_ol = re.match(r'^(\s*)\d+[.)]\s+(.*)', raw)
        if m_ul or m_ol:
            m_any = m_ul or m_ol
            indent_spaces = len(m_any.group(1))
            level = indent_spaces // 2
            text  = m_any.group(2)
            # Strip inline markdown
            text  = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
            text  = re.sub(r'\*([^*]+)\*',     r'\1', text)
            text  = re.sub(r'`([^`]+)`',        r'\1', text)
            text  = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
            pdf.bullet_item(text, level=level)
            i += 1
            continue

        # ── Blank line ────────────────────────────────────────────
        if not stripped:
            pdf.ln(2)
            i += 1
            continue

        # ── Normal paragraph ──────────────────────────────────────
        # Collect wrapped paragraph
        para_lines = []
        while i < len(lines):
            l = lines[i].strip()
            if (not l or l.startswith('#') or l.startswith('```') or
                    l.startswith('|') or re.match(r'^(-{3,}|={3,}|\*{3,})$', l) or
                    re.match(r'^\s*[-*+]\s', lines[i]) or re.match(r'^\s*\d+[.)]\s', lines[i])):
                break
            para_lines.append(l)
            i += 1

        para = ' '.join(para_lines)
        # Strip inline markdown
        para = re.sub(r'\*\*([^*]+)\*\*', r'\1', para)
        para = re.sub(r'\*([^*]+)\*',     r'\1', para)
        para = re.sub(r'`([^`]+)`',        r'\1', para)
        para = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', para)
        if para.strip():
            pdf.body_text(para)
        continue

    if in_table:
        flush_table()
    if in_code and code_buf:
        pdf.code_block(code_buf)


# ── Main ─────────────────────────────────────────────────────────────────────
print(f"Reading: {MD_FILE}")
with open(MD_FILE, "r", encoding="utf-8") as f:
    md_text = f.read()

pdf = TrustGuardPDF()
pdf.set_title("TrustGuard – Project Documentation")
pdf.set_author("TrustGuard AI Team")
pdf.set_subject("IEEE Technosphere Ideathon 2026")
pdf.set_creator("TrustGuard PDF Generator (fpdf2)")

# 1. Cover page
pdf.cover()

# 2. Add a new page before content
pdf.add_page()

# 3. Render markdown content
print("Rendering content pages...")
render_md(pdf, md_text)

# 4. Save
print("Writing PDF...")
pdf.output(PDF_FILE)

size_mb = os.path.getsize(PDF_FILE) / (1024 * 1024)
print(f"\nPDF generated successfully!")
print(f"Location : {PDF_FILE}")
print(f"File size: {size_mb:.2f} MB")
print(f"Pages    : {pdf.page}")
