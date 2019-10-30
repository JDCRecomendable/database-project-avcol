#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Jared Recomendable.
Licensed under the GNU General Public License Version 3.
This program DOES NOT COME WITH ANY WARRANTY, EXPRESS OR IMPLIED.
"""

from fpdf import FPDF
from datetime import datetime


class PDF(FPDF):
    def __init__(self, header_title_text: str = "", header_subtitle_text: str = "", footer_text: str = "",
                 font_face: str = "Arial"):
        super().__init__()
        self.header_title_text = header_title_text
        self.header_subtitle_text = header_subtitle_text
        self.footer_text = footer_text
        self.font_face = font_face
        self.set_font(font_face)
        self.add_page()

    def header(self):
        """Define the header parameters for the PDF document."""
        self.set_font(self.font_face, "B", 16)
        self.cell(0, 10, self.header_title_text, 0, 0, "L")
        self.cell(0, 10, self.header_subtitle_text, 0, 0, "R")
        self.ln(12)

    def footer(self):
        """Define the footer parameters for the PDF document."""
        self.set_y(-15)
        self.set_font(self.font_face, 'B', 8)
        self.cell(0, 10, self.footer_text, 0, 0, "L")
        self.cell(0, 10, "{} | Page {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.page_no()), 0, 0, "R")

    def auto_write(self, text: str, width: int = 0, height: int = 5, line_break: int = 1):
        """Place a cell of text into the PDF document."""
        self.cell(width, height, text, 0, line_break)
