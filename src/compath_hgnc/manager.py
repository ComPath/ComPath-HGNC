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

    def get_pathway_by_name(self, name):
        """Gets all Gene symbols in gene families

        :rtype: Optional[GeneFamily]
        """
        return self.session.query(GeneFamily).filter(GeneFamily.family_name == name).one_or_none()

    def get_all_hgnc_symbols(self):
        """Gets Gene Family by name

        :rtype: set[str]
        """
        return {
            gene.symbol
            for family in self.session.query(GeneFamily)
            for gene in family.hgncs
        }

    def query_pathway_by_name(self, query, limit=None):
        """Returns all pathways having the query in their names

        :param query: query string
        :param Optional[int] limit: limit result query
        :rtype: list[GeneFamily]
        """

        q = self.session.query(GeneFamily).filter(GeneFamily.family_name.contains(query))

        if limit:
            q = q.limit(limit)

        return q.all()

    def autocomplete_gene_families(self, q, limit=None):
        """Wraps the query_pathway_by_name method to return autocompletion in compath

        :param str q: query
        :param int limit: limit of matches
        :rtype: list[str]
        :return:
        """
        return list({
            gene_family.family_name
            for gene_family in self.query_pathway_by_name(q, limit=limit if limit else 10)
        # Limits the results returned to 10
            if gene_family
        })

    def get_families_gene_sets(self):
        """Gets all Gene symbols in gene families

        :rtype: dict[str,set]
        """
        return {
            family.family_name: {gene.symbol for gene in family.hgncs}
            for family in self.session.query(GeneFamily)
        }
