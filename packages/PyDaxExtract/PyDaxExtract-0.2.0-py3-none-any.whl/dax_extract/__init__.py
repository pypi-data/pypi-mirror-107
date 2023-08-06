"""
Extract table relationships and `m` and `DAX` expressions from a `Power BI`
template file.

`Power BI` files in the `pbix` and `pbit` formats are basically zip archives
containing other compressed data.

The `DataModel` file in a `pbix` file contains all the `DAX` expressions created
when processing data. All data is saved in the `Xpress9` format, which is a
proprietary compresson method optimized to dump memory to disk and vice-versa,
with encryption and all kinds of other wonderful features which will break your
heart if you try to get a peek inside.

Fortunately, if one saves a `Power BI` workbook as a template, the table
relationships, `m` expressions and `DAX` expressions are now saved in the
`DataModelSchema` object, which is unencrypted and requires only a bit of
fiddling to remove.

This module, and command-line script are intended to help with that fiddling,
and to aid users in serializing work done in an otherwise fairly opaque binary
format. Here's hoping it's useful to you.

At this point, there appears to be no way to automate exporting `pbix` files as
`pbit`, so you'll have to do that the usual way.


command line usage: daxextract.py [-h] [--dump-json] [--dump-expressions] [--write-dax-csv]
              [--write-powerquery-csv] [--write-relationships-csv]
              pbit_path

Extract PowerQuery (m) / DAX expressions from Power BI template file.

positional arguments:
  pbit_path             Path to .pbit file.

optional arguments:
  -h, --help            show this help message and exit
  --dump-json           Write full dump of DataModelSchema to stdout in json
                        format.
  --dump-expressions    Write DAX and PowerQuery (m) expressions to stdout in
                        json format.
  --write-dax-csv       write csv file containing DAX measures and metadata in
                        csv format.
  --write-powerquery-csv
                        write csv file containing PowerQuery expressions and
                        metadata in csv format.
  --write-relationships-csv
                        write csv file containing table relationships in csv
                        format.

Example:
::
    >> from pathlib import Path
    >> from dax_extract import read_data_model_schema
    >> pbit_path = Path("/path/to/my_awesome.pbit")
    >> data = read_data_model_schema(pbit_path)
"""

from io import BytesIO
import argparse
import csv
import json
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile


def read_data_model_schema(pbit_path):
    """
    Extract ``DataModelSchema`` from ``.pbit`` archive.

    Args:
        pbit_path (pathlib.Path): Path to ``.pbit`` archive.

    Returns:
        data (dict): ``dict`` object of ``DataModelSchema`` data.
    """

    if not pbit_path.is_file():
        raise OSError(f"{pbit_path} not found or not a file.")

    if not pbit_path.parts[-1:][0].endswith(".pbit"):
        raise OSError(f"{pbit_path} is not a Power BI template (pbit) file.")

    # extract data to temporary directory
    with tempfile.TemporaryDirectory() as tempdir:
        with ZipFile(pbit_path, "r") as pbit:
            for info in pbit.infolist():
                if info.filename == "DataModelSchema":
                    filepath = Path(tempdir, info.filename)
                    pbit.extract(info, tempdir)
                    # read data as utf-8
                    with open(filepath, "r") as _fh:
                        data = json.loads(bytes(_fh.read(), "utf-8"))
                        if data:
                            return data

    # if we are here, there was either no "DataModelSchema" object, or it
    # was empty. Bummer.

    raise OSError(f"Unable to extract DataModelSchema from {pbit_path}.")


class DaxExtract:
    """
    Extract ``DAX`` expressions from Power BI templates."
    """

    def __init__(self):
        """
        Run ``argparse.ArgumentParser`` to give a nice args object.
        """

        parser = argparse.ArgumentParser(
            description="Extract PowerQuery (m) / DAX expressions from Power BI template file."
        )

        parser.add_argument("pbit_path", type=str, help="Path to .pbit file.")

        parser.add_argument(
            "--dump-json",
            action="store_true",
            help="Write full dump of DataModelSchema to stdout in json format.",
        )

        parser.add_argument(
            "--dump-expressions",
            action="store_true",
            help="Write DAX and PowerQuery (m) expressions to stdout in json format.",
        )

        parser.add_argument(
            "--write-dax-csv",
            action="store_true",
            help="""write csv file containing DAX measures and metadata in csv format.""",
        )

        parser.add_argument(
            "--write-powerquery-csv",
            action="store_true",
            help="""write csv file containing PowerQuery expressions and metadata in csv format.""",
        )

        parser.add_argument(
            "--write-relationships-csv",
            action="store_true",
            help="""write csv file containing table relationships in csv format.""",
        )

        self.args = parser.parse_args()

    def extract_data_model_schema(self):
        """
        Extract ``DataModelSchema`` from ``.pbit`` archive.

        Returns:
            data (dict): ``dict`` object of ``DataModelSchema`` data.
        """

        pbit_path = Path(self.args.pbit_path)

        return read_data_model_schema(pbit_path)

    def extract_dax(self):
        """
        Extract ``DAX`` formulas from ``DataModelSchema``.

        Returns:
            dax (dict): dax formulas and metadata.
        """

        data = self.extract_data_model_schema()

        dax = {
            "fieldnames": [
                "table_name",
                "measure_name",
                "data_type",
                "dax_expression",
            ],
            "rows": [],
        }

        for table in data["model"]["tables"]:
            if "measures" in table:
                for measure in table["measures"]:
                    dax["rows"].append(
                        {
                            "table_name": table.get("name"),
                            "measure_name": measure.get("name"),
                            "data_type": measure.get("dataType"),
                            "dax_expression": measure.get("expression"),
                        }
                    )

        return dax

    def extract_powerquery_expressions(self):
        """
        Extract ``PowerQuery (m)`` formulas from ``DataModelSchema``.

        Returns:
            pqx (dict): PowerQuery formulas and metadata.
        """

        data = self.extract_data_model_schema()

        pqx = {
            "fieldnames": [
                "name",
                "kind",
                "expression",
            ],
            "rows": [],
        }

        for exp in data["model"]["expressions"]:
            pqx["rows"].append(
                {
                    "name": exp.get("name"),
                    "kind": exp.get("kind"),
                    "expression": exp.get("expression"),
                }
            )

        return pqx

    def extract_relationships(self):
        """
        Extract relationships from ``DataModelSchema``.

        Returns:
            pqx (dict): PowerQuery formulas and metadata.
        """

        data = self.extract_data_model_schema()

        rels = {
            "fieldnames": [
                "from_table",
                "to_table",
                "from_column",
                "to_column",
            ],
            "rows": [],
        }

        for exp in data["model"]["relationships"]:
            rels["rows"].append(
                {
                    "from_table": exp.get("fromTable"),
                    "to_table": exp.get("toTable"),
                    "from_column": exp.get("fromColumn"),
                    "to_column": exp.get("toColumn"),
                }
            )

        return rels

    def dump_json(self):
        """
        Dump well-formatted JSON file to STDOUT
        """

        data = self.extract_data_model_schema()
        sys.stdout.write(json.dumps(data, indent=True))

    def dump_expressions(self):
        """
        Write nicely-formatted ``DAX`` and ``PowerQuery (m)`` expressions and metadata to STDOUT
        """
        data = {
            "table_relationships": self.extract_relationships(),
            "powerquery_expressions": self.extract_powerquery_expressions(),
            "dax_expressions": self.extract_dax(),
        }
        sys.stdout.write(json.dumps(data, indent=True))

    def write_dax_csv(self):
        """
        Write ``DAX`` measures and metadata to file in ``.csv`` format.
        """

        return self.write_csv("dax-measures", self.extract_dax())

    def write_powerquery_csv(self):
        """
        Write ``PowerQuery (m)`` expressions and metadata to file in ``.csv``
        format.
        """
        return self.write_csv(
            "powerquery-expressions", self.extract_powerquery_expressions()
        )

    def write_relationships_csv(self):
        """
        Write table relationships to file in ``.csv`` format.
        """
        return self.write_csv("relationships", self.extract_relationships())

    def write_csv(self, data_type, data):
        """
        Write data to file in ``.csv`` format.
        """

        name = Path(self.args.pbit_path).parts[-1:][0].strip(".pbit")
        filename = f"{name}-{data_type}.csv"

        with open(Path(filename), "w", newline="") as _fh:
            writer = csv.DictWriter(_fh, fieldnames=data["fieldnames"])
            writer.writeheader()
            writer.writerows(data["rows"])
