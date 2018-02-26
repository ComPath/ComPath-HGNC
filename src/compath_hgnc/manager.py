# -*- coding: utf-8 -*-

from bio2bel_hgnc.manager import Manager as Bio2BELManager
from bio2bel_hgnc.models import GeneFamily, HGNC


class Manager(Bio2BELManager):
    """An minimized version of the Bio2BELManager manager adapted for ComPath"""

    def query_gene_set(self, gene_set):
        """Returns HGNCs within the gene set

        :param gene_set: set of gene symbols
        :rtype: list[models.HGNC]
        :return: list of proteins
        """
        return self.session.query(HGNC).filter(HGNC.symbol.in_(gene_set)).all()

    def get_families_gene_sets(self):
        """Gets all Gene symbols in gene families

        :rtype: dict[str,set]
        """
        return {
            family.family_name: {gene.symbol for gene in family.hgncs}
            for family in self.session.query(GeneFamily)
        }
