
class Structure_generator:
    """
    This class is responsible for generating the structure of the documentation.
    It creates a list of dictionaries representing the structure of the documentation.
    Each dictionary contains the following keys:
        - name: The name of the section
        - type: The type of section (e.g. 'section', 'subsection', 'subsubsection')
        - content: The content of the section (if any)
        - children: A list of child sections
    """

    def __init__(self, tablelist, for_word=False):
        """
        Constructor
        :param tablelist: A list of tables
        :param for_word: Format for MS Word
        """
        self.tablelist = tablelist
        self.generated_structure = ''
        self.gen_table_structures_for_adoc(for_word)

    def get_table_structures(self):
        return self.generated_structure

    def gen_table_structures_for_adoc(self, for_word):
        """
        A táblák struktúráját az asciidoctor számára könnyen feldolgozható formába alakítja.
        :param db: adatbázis objektum
        :return: a táblák struktúrája az asciidoctor számára könnyen feldolgozható formában
        """
        out = []
        for table in self.tablelist:
            table_structure = table.get_structure(for_word)
            table_structure_formatted = self._add_header_and_separators(table_structure)
            out.append(f'== {table.name}\n')
            out.append('|===\n')
            for column in table_structure_formatted:
                out.append(column.replace('None', ' '))
            out.append('|===' + '\n\n')
        self.generated_structure = ''.join(out)

    @staticmethod
    def _add_header_and_separators(columns):
        """
        Az oszlopokat az asciidoctor számára könnyen feldolgozható formába alakítja
        és kiegészíti a táblázatot egy fejléccel.
        :param columns: oszlopok listája
        :return: az oszlopok listája kiegészített formátumban
        """
        out = ['| Mező | Típus | Alapértelmezett érték | Kötelező? | Leírás\n']
        for column in columns:
            out.append(f'| {column[0]} | {column[1]} | {column[2]} | {column[3]} | {column[4]}\n')
        return out
