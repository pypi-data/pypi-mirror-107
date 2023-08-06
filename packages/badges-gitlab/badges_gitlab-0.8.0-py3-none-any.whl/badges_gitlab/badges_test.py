"""Generate Tests Badges related by parsing JUnit XML files"""
import os
from xml.parsers.expat import ExpatError

import xmltodict  # type: ignore

from .badges_api import validate_path
from .badges_json import json_badge, print_json


def create_test_json_badges(json_directory, test_results: list) -> str:
    """
    This function returns parses a list with the test summary to json format.
    The list order must be: total tests, total failures, total errors, total_skipped, total_time
    """
    # from the list values we build our dictionary for badges
    total_not_passed = sum(test_results[1:4])
    total_passed = test_results[0] - total_not_passed
    test_badge_color = 'red' if total_not_passed > 0 else 'green'
    test_badge_summary_text = '{0} passed, {1} failed'.format(total_passed, total_not_passed) \
        if total_not_passed > 0 else '{0} passed'.format(total_passed)
    # define badges dicts
    total_tests_dict = print_json('total tests', str(test_results[0]), 'blue')
    total_time_dict = print_json('total execution time', '{0:.2f}s'.format(test_results[4]), 'blue')
    test_summary_dict = print_json('tests', test_badge_summary_text, test_badge_color)
    test_complete_dict = print_json('tests', '{0} passed, {1} failed, {2} errors, {3} skipped'.
                                    format(total_passed, test_results[1], test_results[2], test_results[3]),
                                    test_badge_color)
    # Dictionary Format = filename : [label, value, color]
    test_badges_dict = {
        "total_tests": total_tests_dict,
        "total_time":  total_time_dict,
        "tests": test_summary_dict,
        "tests_complete": test_complete_dict
    }
    for badge in list(test_badges_dict.keys()):
        json_dict = test_badges_dict[badge]
        json_badge(json_directory, badge, json_dict)
    return "Total Tests = {}, Passed = {}, Failed = {}, Errors = {}, Skipped = {}, Time = {:.2f}s.\n" \
           "Badges from JUnit XML test report tests created!".format(test_results[0], total_passed,
                                                                     test_results[1], test_results[2],
                                                                     test_results[3], test_results[4])


def create_badges_test(json_directory, file_path: str) -> str:
    """
    This function parses a JUnit XML file to extract general information
    about the unit tests.
    """
    validate_path(json_directory)
    # Define variables for using it in all functions
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    total_time = 0.0
    if not os.path.isfile(file_path):
        return 'Junit report file does not exist...skipping!'
    with open(file_path) as xml_file:
        # Extract the test suites as dictionaries
        try:
            content = xmltodict.parse(xml_file.read())
            testsuites = content['testsuites']['testsuite']
            for testsuite in testsuites:
                total_tests += int(testsuite['@tests'])
                total_failures += int(testsuite['@failures'])
                total_errors += int(testsuite['@errors'])
                total_skipped += int(testsuite['@skipped'])
                total_time += float(testsuite['@time'])
            return create_test_json_badges(json_directory, [total_tests, total_failures,
                                                            total_errors, total_skipped, total_time])
        except ExpatError:
            return 'Error parsing the file. Is it a JUnit XML?'
