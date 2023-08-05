class ReportComponent:
    def __init__(self, title='', pre_text='', plots=[], post_text=''):
        self.title     = title
        self.pre_text  = pre_text
        self.plots     = plots
        self.post_text = post_text

    def to_json(self):
        return vars(self)

    def __repr__(self):
        return str(vars(self))