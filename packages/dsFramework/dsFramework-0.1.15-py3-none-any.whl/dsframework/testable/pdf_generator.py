from fpdf import FPDF
from dsframework.testable.reporter_component import ReportComponent
import pathlib
import os

from dsframework.base_classes.object_base import ObjectBase

class PdfGenerator(ObjectBase):
    @staticmethod
    def get_defaults():
        cfg = {}
        cfg['FONT_NAME'] = 'Arial'
        cfg['NORMAL_FONT_SIZE'] = 12
        cfg['TITLE_FONT_SIZE'] = 16
        cfg['HEADER_FONT_SIZE'] = 20
        cfg['IN_CELL_SPACE'] = 5
        cfg['BETWEEN_CELL_SPACE'] = 10
        cfg['HEADER_ALIGN'] = 'C'
        cfg['TEXT_ALIGN'] = 'L'
        cfg['IMAGE_MARGIN'] = 20
        cfg['PAGE_WIDTH'] = 210
        return cfg

    def __init__(self, name='pdf_generator', **kwargs):
        ObjectBase.__init__(self, name, PdfGenerator.get_defaults(), **kwargs)
        self.components    = []
        self.report_path   = ''
        self.report_header = ''
        self.pdf           = None

    def __call__(self, components=[], report_path='', report_header='', **kwargs):
        return self.generate(components, report_path, report_header,  **kwargs)

    def reset(self, compononets=[], report_path='', report_header='', **kwargs):
        if kwargs:
            self.config(**kwargs)

        self.components = compononets
        self.report_path   = report_path
        self.report_header = report_header
        self.pdf = FPDF()
        self.pdf.add_page()
        self.add_text(self.report_header, self.HEADER_FONT_SIZE, self.HEADER_ALIGN)

    def generate(self, compononets=[], report_path='', report_header='',   **kwargs):
        self.reset(compononets, report_path, report_header,  **kwargs)
        self.insert_components(self.components)
        self.save_report(report_path)

    def insert_components(self, component_l):
        for component in component_l:
            self.pdf.add_page()
            self.insert_single_component(component)

    def insert_single_component(self, report_component: ReportComponent):
        self.add_text(report_component.title, self.TITLE_FONT_SIZE, self.TEXT_ALIGN)
        self.add_text(report_component.pre_text, self.NORMAL_FONT_SIZE, self.TEXT_ALIGN)
        self.add_images(report_component.plots)
        self.add_text(report_component.post_text, self.NORMAL_FONT_SIZE, self.TEXT_ALIGN)

    def add_text(self, text, font_size, alignment):
        for line in text.split('\n'):
            self.pdf.set_font(self.FONT_NAME, size=font_size)
            self.pdf.cell(w=0, h=0, txt=line, align=alignment, ln=1)
            self.add_post_elem_space(self.IN_CELL_SPACE)
        self.add_post_elem_space(self.IN_CELL_SPACE)

    def add_images(self, image_l):
        for image_path in image_l:
            self.pdf.image(image_path, x=self.IMAGE_MARGIN, w=self.PAGE_WIDTH-(2*self.IMAGE_MARGIN))
            self.add_post_elem_space(self.IN_CELL_SPACE)

    def add_post_elem_space(self, space_height):
        self.pdf.cell(w=0, h=space_height, ln=1)

    def save_report(self, path=''):
        output_path  = pathlib.Path(path)/'report.pdf'
        if output_path.exists():
            os.remove(output_path)
        self.pdf.output(output_path)

    ## implement this method
    def get_componenets_from_df(self, df):
        return ReportComponent()



