#!/usr/bin/env python

"""
Run dax_extract module with command line arguments
"""

from dax_extract import DaxExtract

def main():
    """
    Run DaxExtract to file or ``STDOUT``.
    """

    _da = DaxExtract()

    if _da.args.dump_json:
        _da.dump_json()

    if _da.args.dump_expressions:
        _da.dump_expressions()

    if _da.args.write_dax_csv:
        _da.write_dax_csv()

    if _da.args.write_powerquery_csv:
        _da.write_powerquery_csv()

    if _da.args.write_relationships_csv:
        _da.write_relationships_csv()
