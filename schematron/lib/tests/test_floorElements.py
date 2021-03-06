import os
from copy import deepcopy

from lxml import etree

from tools.validate_sch import validate_schematron
from tools.constants import BSYNC_NSMAP
from schematron.conftest import AssertFailureRolesMixin, sch_from_imported_abstract_pattern

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


class TestFloorElements(AssertFailureRolesMixin):

    def test_fa_maxOneOfEachType_passes_valid_doc(self):
        # -- Setup
        example_file = os.path.join(DATA_DIR, 'ex01.xml')
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.maxOneOfEachType",
            {'parent': 'auc:Building/auc:FloorAreas'})

        # -- Act
        failures = validate_schematron(schematron, example_file)

        # -- Assert
        self.assert_failure_messages(failures, {})

    def test_fa_maxOneOfEachType_fails_when_duplicate_floor_area_types(self):
        # -- Setup
        example_tree = etree.parse(os.path.join(DATA_DIR, 'ex01.xml'))
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.maxOneOfEachType",
            {'parent': 'auc:Building/auc:FloorAreas'})

        # make sure it's valid
        failures = validate_schematron(schematron, example_tree)

        # -- Act
        # add extra floor areas
        def _dup_elem(tree, xpath):
            elem = tree.xpath(xpath, namespaces=BSYNC_NSMAP)
            assert len(elem) == 1
            elem = elem[0]
            elem.getparent().append(deepcopy(elem))
        _dup_elem(example_tree, '//auc:Building/auc:FloorAreas/auc:FloorArea[auc:FloorAreaType/text() = "Gross"]')
        _dup_elem(example_tree, '//auc:Building/auc:FloorAreas/auc:FloorArea[auc:FloorAreaType/text() = "Heated and Cooled"]')

        failures = validate_schematron(schematron, example_tree)

        # -- Assert
        self.assert_failure_messages(failures, {
            'ERROR': [
                "element 'auc:FloorAreaType' with value 'Gross' is ALLOWED NO MORE THAN ONCE for 'auc:FloorAreas'",
                "element 'auc:FloorAreaType' with value 'Heated and Cooled' is ALLOWED NO MORE THAN ONCE for 'auc:FloorAreas'"
            ]
        })

    def test_fa_haveTypeAndValue_passes_valid_doc(self):
        # -- Setup
        example_file = os.path.join(DATA_DIR, 'ex01.xml')
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.haveTypeAndValue",
            {'parent': 'auc:Building/auc:FloorAreas/auc:FloorArea'})

        # -- Act
        failures = validate_schematron(schematron, example_file)

        # -- Assert
        self.assert_failure_messages(failures, {})

    def test_fa_oneOfType_passes_valid_doc(self):
        # -- Setup
        example_file = os.path.join(DATA_DIR, 'ex01.xml')
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.oneOfType",
            {
                'floorAreaType': "'Gross'",
                'parent': 'auc:Building/auc:FloorAreas',
            })

        # -- Act
        failures = validate_schematron(schematron, example_file)

        # -- Assert
        self.assert_failure_messages(failures, {})

    def test_fa_dontUse_passes_valid_doc(self):
        # -- Setup
        example_file = os.path.join(DATA_DIR, 'ex01.xml')
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.dontUse",
            {'parent': 'auc:Building/auc:FloorAreas'})

        # -- Act
        failures = validate_schematron(schematron, example_file)

        # -- Assert
        self.assert_failure_messages(failures, {})

    def test_fa_noneDefinedWarn_passes_valid_doc(self):
        # -- Setup
        example_file = os.path.join(DATA_DIR, 'ex01.xml')
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.noneDefinedWarn",
            {
                'floorAreaType': "'Ventilated'",
                'parent': 'auc:Building/auc:FloorAreas'
            })

        # -- Act
        failures = validate_schematron(schematron, example_file)

        # -- Assert
        self.assert_failure_messages(failures, {
            'WARNING': ["element 'auc:FloorAreaType' with value 'Ventilated' is RECOMMENDED for: 'auc:FloorAreas'"]
        })

    def test_fa_oneOfMechType_passes_valid_doc(self):
        # -- Setup
        example_file = os.path.join(DATA_DIR, 'ex01.xml')
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.oneOfMechType",
            {'parent': 'auc:Building/auc:FloorAreas'})

        # -- Act
        failures = validate_schematron(schematron, example_file)

        # -- Assert
        self.assert_failure_messages(failures, {})

    def test_fa_mechTypeChecks_passes_valid_doc(self):
        # -- Setup
        example_file = os.path.join(DATA_DIR, 'ex01.xml')
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.mechTypeChecks",
            {'parent': 'auc:Building/auc:FloorAreas'})

        # -- Act
        failures = validate_schematron(schematron, example_file)

        # -- Assert
        self.assert_failure_messages(failures, {
            'INFO': [
                "'Gross' Floor Area: 4477800",
                "'Cooled only' Floor Area: 0",
                "'Heated only' Floor Area: 0",
                "'Heated and Cooled' Floor Area: 4477800",
                "'Ventilated' Floor Area: 0",
                "'Conditioned' Floor Area: 4477800",
                "'Unconditioned' Floor Area: 0"
            ]
        })

    def test_fa_buildingSectionGrossAreaChecks_passes_valid_doc(self):
        # -- Setup
        example_file = os.path.join(DATA_DIR, 'ex01.xml')
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.buildingSectionGrossAreaChecks",
            {'parent': 'auc:Buildings/auc:Building'})

        # -- Act
        failures = validate_schematron(schematron, example_file)

        # -- Assert
        self.assert_failure_messages(failures, {
            'INFO': [
                "Building Gross Floor Area: 4477800",
                "Sum of all auc:Section[auc:SectionType='Space function'] Gross Floor Area: 123",
            ]
        })

    def test_fa_type_valueOrPercent_passes_valid_doc(self):
        # -- Setup
        example_file = os.path.join(DATA_DIR, 'ex01.xml')
        schematron = sch_from_imported_abstract_pattern(
            "floorElements.sch", "fa.type.valueOrPercent",
            {'parent': 'auc:FloorAreas/auc:FloorArea'})

        # -- Act
        failures = validate_schematron(schematron, example_file)

        # -- Assert
        self.assert_failure_messages(failures, {})
