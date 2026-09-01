# -*- coding: utf-8 -*-
"""Rebuild Mariam's CV: adds portrait photo, removes the law degree,
adds Casa Gelso, and matches the tone of the portfolio site."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

OUT = "/home/claude/work/portfolio/cv/mariam-kajaia-cv.pdf"
PORTRAIT = "/home/claude/work/portfolio/assets/portrait.jpg"

INK = colors.HexColor("#121417")
RUST = colors.HexColor("#a45234")
BLUE = colors.HexColor("#203a59")
MUTED = colors.HexColor("#5c6064")
LINE = colors.HexColor("#c9c7c0")

W, H = A4
ML, MR = 18 * mm, 18 * mm
CW = W - ML - MR

# photo column on the right of the header
PHOTO_W = 33 * mm
PHOTO_H = PHOTO_W * 5 / 4

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Mariam Kajaia CV")
c.setAuthor("Mariam Kajaia")
c.setSubject("Digital Designer and Front-End Developer")

y = H - 16 * mm


def rule(yy, x0=ML, x1=W - MR, col=LINE, wgt=0.6):
    c.setStrokeColor(col)
    c.setLineWidth(wgt)
    c.line(x0, yy, x1, yy)


def wrap(text, font, size, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(text, yy, size=8.4, font="Helvetica", col=MUTED, width=CW, x=ML, lead=11.4):
    for ln in wrap(text, font, size, width):
        c.setFont(font, size)
        c.setFillColor(col)
        c.drawString(x, yy, ln)
        yy -= lead
    return yy


def section(title, yy):
    yy -= 4
    c.setFont("Helvetica-Bold", 7.6)
    c.setFillColor(RUST)
    c.drawString(ML, yy, title.upper())
    yy -= 4.5
    rule(yy)
    return yy - 11


# ---------------------------------------------------------------- header
text_w = CW - PHOTO_W - 8 * mm

c.setFont("Helvetica-Bold", 21)
c.setFillColor(INK)
c.drawString(ML, y, "Mariam Kajaia")
y -= 15

c.setFont("Helvetica", 10)
c.setFillColor(BLUE)
c.drawString(ML, y, "Digital Designer and Front-End Developer")
y -= 15

contact = [
    "marykajaia8@gmail.com",
    "WhatsApp +995 599 298 912",
    "linkedin.com/in/mariam-kajaia1997999",
    "github.com/digitalinvitee",
    "Tbilisi, Georgia. Remote or hybrid.",
]
c.setFillColor(MUTED)
for line in wrap("  |  ".join(contact), "Helvetica", 8, text_w):
    c.setFont("Helvetica", 8)
    c.drawString(ML, y, line)
    y -= 10.5

# portrait, top right, aligned with the name
img = Image.open(PORTRAIT)
iw, ih = img.size
target_ratio = PHOTO_W / PHOTO_H
if iw / ih > target_ratio:
    new_w = int(ih * target_ratio)
    left = (iw - new_w) // 2
    img = img.crop((left, 0, left + new_w, ih))
else:
    new_h = int(iw / target_ratio)
    img = img.crop((0, 0, iw, new_h))
img = img.resize((520, int(520 / target_ratio)), Image.LANCZOS)
tmp = "/tmp/cv_portrait.jpg"
img.save(tmp, quality=86, optimize=True)

px = W - MR - PHOTO_W
py = H - 16 * mm + 6 - PHOTO_H
c.drawImage(ImageReader(tmp), px, py, PHOTO_W, PHOTO_H,
            preserveAspectRatio=False, mask=None)
c.setStrokeColor(LINE)
c.setLineWidth(0.6)
c.rect(px, py, PHOTO_W, PHOTO_H, stroke=1, fill=0)

y = min(y, py) - 10

# ---------------------------------------------------------------- profile
y = section("Profile", y)
y = para(
    "Digital designer and front-end developer. I design and build websites and launch campaigns for "
    "brands, and I do the whole thing myself: the campaign concept, the copy, the art direction, the "
    "front-end build and the testing. Nine live sites delivered for real clients, most recently a full "
    "three-act launch campaign for a luxury fashion house, written and shipped in three languages. Four "
    "years managing large corporate accounts before I moved into building, so a client brief and a "
    "non-technical stakeholder are familiar ground. Looking for a stable role on a creative team.",
    y,
)

# ---------------------------------------------------------------- experience
y = section("Experience", y - 5)


def role(title, org, dates, body, yy):
    c.setFont("Helvetica-Bold", 9.6)
    c.setFillColor(INK)
    c.drawString(ML, yy, title)
    c.setFont("Helvetica", 8)
    c.setFillColor(RUST)
    c.drawRightString(W - MR, yy, dates)
    yy -= 11
    c.setFont("Helvetica-Bold", 8.2)
    c.setFillColor(BLUE)
    c.drawString(ML, yy, org)
    yy -= 11
    yy = para(body, yy)
    return yy - 8


y = role(
    "Founder, Designer and Developer", "INVITÉ, digital experience studio, Tbilisi", "May 2026 to now",
    "Digital experience studio for brand launches, openings and weddings. I own the concept, the client "
    "relationship, the design, the front-end build, the testing and the delivery on every project. "
    "Delivered the Casa Gelso launch campaign, the JETOUR Georgia bilingual event product and five "
    "independent wedding sites, each with its own art direction.",
    y,
)

y = role(
    "Large Corporate Clients Manager", "GPI Holding, Vienna Insurance Group", "2020 to 2024",
    "Managed relationships with corporate stakeholders and clients: gathering requirements, negotiating "
    "terms, prioritising deliverables and taking responsibility for outcomes. This is the foundation for "
    "how I now scope and run client-facing digital projects.",
    y,
)

# ---------------------------------------------------------------- projects
y = section("Selected projects", y + 2)


def project(name, meta, body, url, yy):
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(INK)
    c.drawString(ML, yy, name)
    nw = pdfmetrics.stringWidth(name, "Helvetica-Bold", 9)
    c.setFont("Helvetica", 7.6)
    c.setFillColor(RUST)
    c.drawString(ML + nw + 6, yy, meta)
    yy -= 10.5
    yy = para(body, yy)
    c.setFont("Helvetica-Oblique", 7.8)
    c.setFillColor(BLUE)
    c.drawString(ML, yy, url)
    return yy - 13


y = project(
    "Casa Gelso", "luxury fashion launch, Tbilisi",
    "A three-act launch campaign for a fashion house carrying Ferragamo, Moschino, Tom Ford and Bottega "
    "Veneta: a teaser, a scroll-driven brand reveal and a private invitation with RSVP and guest data "
    "capture, on one continuous page in English, Georgian and Italian. Campaign concept, storytelling, "
    "copy, art direction, front-end, sound, form logic and QA, all by me.",
    "digitalinvitee.github.io/casa-gelso", y,
)

y = project(
    "JETOUR Georgia", "commercial client project",
    "A bilingual event experience with RSVP, Google Sheets data collection, a countdown and location "
    "details, delivered end to end with a full QA pass. Reused for a second brand activation.",
    "digitalinvitee.github.io/JETOUR", y,
)

y = project(
    "Five wedding experiences", "independent live sites",
    "Five live wedding sites sharing one feature system of RSVP, maps, schedules, galleries and "
    "multilingual UI, with five distinct visual identities.",
    "github.com/digitalinvitee", y,
)

# ---------------------------------------------------------------- education
y = section("Education", y + 2)


def edu(title, org, dates, body, yy):
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(INK)
    c.drawString(ML, yy, title)
    c.setFont("Helvetica", 7.8)
    c.setFillColor(RUST)
    c.drawRightString(W - MR, yy, dates)
    yy -= 10
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(BLUE)
    c.drawString(ML, yy, org)
    yy -= 10.5
    yy = para(body, yy)
    return yy - 7


y = edu("Web Development", "Barcelona Code School", "2023 to 2024",
        "Front-end foundations, responsive development and practical implementation with HTML, CSS and "
        "JavaScript.", y)

y = edu("Manual Quality Assurance", "GenOfIT", "2025",
        "Manual testing, user flows, bug reporting, test cases and API testing fundamentals.", y)

# ---------------------------------------------------------------- skills
y = section("Skills", y + 2)

skills = [
    ("Design", "Web design, art direction, typography, digital campaigns, interactive experiences, UI and UX"),
    ("Development", "HTML, CSS, JavaScript, responsive development, API integration, GSAP, Git and GitHub, Google Apps Script. Learning React and backend."),
    ("Quality", "Manual QA, responsive testing, user flows, edge cases, Postman, Jira, TestRail"),
    ("Product and business", "Digital product thinking, stakeholder communication, requirements, client management, prioritisation, negotiation, ownership"),
    ("Languages", "Georgian, English, German"),
]

LABEL_W = 34 * mm
for label, body in skills:
    c.setFont("Helvetica-Bold", 8.2)
    c.setFillColor(BLUE)
    c.drawString(ML, y, label)
    yy = y
    for ln in wrap(body, "Helvetica", 8.2, CW - LABEL_W):
        c.setFont("Helvetica", 8.2)
        c.setFillColor(MUTED)
        c.drawString(ML + LABEL_W, yy, ln)
        yy -= 10.8
    y = yy - 2.5

c.showPage()
c.save()
print("written", OUT, os.path.getsize(OUT), "bytes")
