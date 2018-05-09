# -*- coding: utf-8 -*-

from bio2bel.testing import AbstractTemporaryCacheClassMixin
from compath_hgnc import Manager
from tests.constants import hcop_test_path, hgnc_test_path


class TemporaryCacheClassMixin(AbstractTemporaryCacheClassMixin):
    Manager = Manager

    @classmethod
    def populate(cls):
        cls.manager.populate(
            hgnc_file_path=hgnc_test_path,
            hcop_file_path=hcop_test_path,
        )


class TestManager(TemporaryCacheClassMixin):
    def help_check_cd33_model(self, model):
        """Checks if the given model is CD33

        :param pyhgnc.manager.models.HGNC model: The result from a search of the PyHGNC database
        """
        self.assertIsNotNone(model)
        self.assertEqual('1659', str(model.identifier))
        self.assertEqual('CD33', model.symbol)
        self.assertEqual('CD33 molecule', model.name)

    def test_pyhgnc_loaded(self):
        cd33_results = self.manager.hgnc(symbol='CD33')
        self.assertIsNotNone(cd33_results)

        self.assertEqual(1, len(cd33_results))

        cd33_model = cd33_results[0]
        self.help_check_cd33_model(cd33_model)
