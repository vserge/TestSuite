import copy
import os
import pprint

from lxml import etree

from tools.constants import BSYNC_NSMAP

SCH_LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
v2_0_0_SCH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v2.0.0')
v2_2_0_SCH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v2.2.0')


class AssertFailureRolesMixin:
    def assert_failure_counts(self, actual_failures, expected_dict):
        """Makes assertions about the failures. Specifically, their roles as well as
        what assertions they failed on

        :param actual_failures: list of Failures
        :param expected_dict: dict, keys are roles and values are the number of occurrences of that failure role
        """
        actual = failures_by_role(copy.deepcopy(actual_failures))
        expected = copy.deepcopy(expected_dict)
        for expected_role in list(expected.keys()):
            if expected[expected_role] != 0:
                assert expected_role in actual, f"Expected to find failure with role {expected_role}"
                actual_failures = actual.pop(expected_role)
                assert expected[expected_role] == len(actual_failures), f"Expected failures does not equal actual failures for role {expected_role}"
            else:
                assert expected_role not in actual, f"Expected to NOT find failure with role {expected_role}"

        assert len(actual) == 0, f"Expected to account for all failure roles, but found some unaccounted for:\n{pprint.pformat(actual, indent=4)}"

    def assert_failure_messages(self, actual_failures, expected_dict):
        """Makes assertions about the failures. Specifically, their roles as well as
        what the failed assertion messages were.

        :param actual_failures: list of Failures
        :param expected_dict: dict, keys are roles and values lists of assertion messages
        """
        actual = failures_by_role(copy.deepcopy(actual_failures))
        expected = copy.deepcopy(expected_dict)
        for expected_role in expected:
            if len(expected[expected_role]) != 0:
                assert expected_role in actual, f"Expected to find failure with role {expected_role}"
                actual_failure_msgs = [failure.message for failure in actual.pop(expected_role)]
                assert expected[expected_role] == actual_failure_msgs
            else:
                assert expected_role not in actual, f"Expected to NOT find failure with role {expected_role}"

        assert len(actual) == 0, f"Expected to account for all failure roles, but found some unaccounted for:\n{pprint.pformat(actual, indent=4)}"


def failures_by_role(failures):
    """Returns a dict of array of failures, keyed by failure role

    :param failures: list of Failures
    :return: dict
    """
    res = {}
    for failure in failures:
        if failure.role in res:
            res[failure.role].append(failure)
        else:
            res[failure.role] = [failure]

    return res


def exemplary_tree(name, version):
    """Returns parsed lxml tree of the exemplary file

    :param name: str, name of the file, without any file extension
    :param version: str, version directory
    :return: lxml.etree
    """
    exemplary_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), version, 'exemplary_files', f'{name}.xml')
    return etree.parse(exemplary_file)


def remove_element(tree, xpath, expected_removals=1):
    elems = tree.xpath(xpath, namespaces=BSYNC_NSMAP)
    assert len(elems) == expected_removals
    for elem in elems:
        elem.getparent().remove(elem)

    return tree


def replace_element(tree, xpath_to_replace, new_element):
    elems = tree.xpath(xpath_to_replace, namespaces=BSYNC_NSMAP)
    assert len(elems) == 1
    elem = elems[0]
    parent_elem = elem.getparent()
    parent_elem[parent_elem.index(elem)] = new_element

    return tree


def sch_from_imported_pattern(lib_filename, pattern_id):
    """
    Creates a schematron document which only contains the specified pattern

    :param lib_filename: str, filename to use (e.g. buildingElements.sch)
    :param pattern_id: str, pattern ID to use from file
    :return: str
    """
    return f"""<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <ns prefix="auc" uri="http://buildingsync.net/schemas/bedes-auc/2019"/>
    <phase id="Tests">
        <active pattern="{pattern_id}"/>
    </phase>
    <include href="{SCH_LIB_DIR}/{lib_filename}#{pattern_id}"/>
</schema>"""


def sch_from_imported_abstract_pattern(lib_filename, pattern_id, params):
    """
    Creates a schematron document which only includes the specified abastract pattern

    :param lib_filename: str, filename to use (e.g. buildingElements.sch)
    :param pattern_id: str, pattern ID to use from file
    :param params: dict, parameters for abstract pattern, where keys are the parameter name and values are their values
    :return: str
    """
    pattern_instance_id = f'inst.{pattern_id}'
    param_strings = [f'<param name="{key}" value="{val}"/>' for key, val in params.items()]
    joined_param_strings = '\n        '.join(param_strings)
    return f"""<schema xmlns="http://purl.oclc.org/dsdl/schematron">
    <ns prefix="auc" uri="http://buildingsync.net/schemas/bedes-auc/2019"/>
    <phase id="Tests">
        <active pattern="{pattern_instance_id}"/>
    </phase>
    <pattern id="{pattern_instance_id}" is-a="{pattern_id}">
        {joined_param_strings}
    </pattern>
    <include href="{SCH_LIB_DIR}/{lib_filename}#{pattern_id}"/>
</schema>"""
