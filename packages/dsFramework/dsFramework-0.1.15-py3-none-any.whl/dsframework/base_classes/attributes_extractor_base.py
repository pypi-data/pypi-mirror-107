"""
extract attributes from raw html
"""
from dsframework.shared.shared_objects import SharedArtifacts
from dsframework.config.zids_config import ZIDSConfig
from dsframework.utils import RegexHandler
from dsframework.base_classes.object_base import ObjectBase
from string import punctuation


class AttributesExtractorBase(ObjectBase):
    """
    extract attributes from raw html
    """

    def __init__(self, config: ZIDSConfig, shared_artifacts: SharedArtifacts, name: str = "attributes_extractor_base",
                 **kwargs):
        super(AttributesExtractorBase, self).__init__(config=config, shared_artifacts=shared_artifacts, name=name, **kwargs)
        self.attributes = {}

    def get_attributes(self) -> dict:
        """
        return all stored attributes as dict
        :return: dict
        """
        return self.attributes

    def extract_regex_attributes(self, text: str = ''):
        """
        extract regex attributes
        :param text: the input text
        """
        self.extract_numeric(text)
        self.extract_urls(text)
        self.extract_email(text)
        self.extract_punct(text)
        self.extract_case(text)

    def extract_numeric(self, text: str):
        """
        extract attributes as numeric.
        :param text: the input text
        """
        self.attributes['tokens_n_digits'] = []
        self.attributes['tokens_is_numeric'] = []
        for token in text.split():
            n_digits, _ = RegexHandler.get_number_of_digits_and_digits_groups_in_text(token)
            self.attributes['tokens_n_digits'] += [n_digits]
            self.attributes['tokens_is_numeric'] += [len(RegexHandler.remove_punct(token)) == n_digits]

    def extract_urls(self, text: str):
        """
        extract url attributes.
        :param text: the input text
        """
        self.attributes['urls'] = RegexHandler.get_urls(text)
        self.attributes['n_urls'] = len(self.attributes['urls'])
        self.attributes['domains'] = RegexHandler.get_domains(text)
        self.attributes['n_domains'] = len(self.attributes['domains'])

    def extract_email(self, text: str):
        """
        extract email attributes
        :param text: the input text
        """
        users, emails = [], []
        if '@' in text:
            _, users = RegexHandler.get_domains_and_users(text)
            emails = RegexHandler.get_emails(text)
        self.attributes['emails'] = emails
        self.attributes['n_emails'] = len(emails)
        self.attributes['users'] = users
        self.attributes['n_users'] = len(users)

    def extract_punct(self, text: str):
        """
        extract punct attributes
        :param text: the input text
        :return:
        """

        def punct_to_group(punct_:str):
            """
            return type of puct
            :param punct_: the puct str
            :return: type of puct
            """
            if punct_ in ',|~\\/*':
                return 'SEP'
            elif punct_ in '''()[]{}<>+''':
                return 'BRACKETS'
            elif punct_ in '''?!''':
                return 'MARKS'
            elif punct_ in '''@_''':
                return 'AT_'
            elif punct_ in '''=-+''':
                return 'MATH'
            else:
                return 'OTHER'

        self.attributes['tokens_n_punct'] = []
        self.attributes['tokens_is_punct'] = []
        self.attributes['tokens_punct'] = []
        self.attributes['tokens_punct_groups'] = []

        for token in text.split():
            punct = ''.join([c for c in token if c in punctuation])
            n_punct = len(punct)
            is_punct = n_punct == len(token)
            punct_groups = [punct_to_group(c) for c in punct]

            self.attributes['tokens_n_punct'] += [n_punct]
            self.attributes['tokens_is_punct'] += [is_punct]
            self.attributes['tokens_punct'] += [punct]
            self.attributes['tokens_punct_groups'] += [punct_groups]

    def extract_case(self, text: str):
        """
        extract features that case sensitive
        :param text: the input text
        """
        self.attributes['tokens_case'] = [
            'UPPER' if t.isupper() else 'TITLE' if t.istitle() else 'LOWER' if t.islower() else 'MIXED' for t in
            text.split()]
