import pytest
import pandas as pd
import pandas.api.types as ptypes
import yaml

ENCINA_QPCR = "Encina_sewage_qPCR.csv"
ENCINA_SEQS = "Encina_sewage_seqs.csv"

POINTLOMA_QPCR = "PointLoma_sewage_qPCR.csv"
POINTLOMA_SEQS = "PointLoma_sewage_seqs.csv"

SOUTHBAY_QPCR = "SouthBay_sewage_qPCR.csv"
SOUTHBAY_SEQS = "SouthBay_sewage_seqs.csv"

QPCR = [ENCINA_QPCR, POINTLOMA_QPCR, SOUTHBAY_QPCR]
SEQS = [ENCINA_SEQS, POINTLOMA_SEQS, SOUTHBAY_SEQS]

QPCR_COLUMNS = ["Sample_Date", "Mean viral gene copies/L"]

SEQ_CONFIG = "plot_config.yml"

@pytest.fixture
def qpcr_files():
    return [(file, pd.read_csv( file, parse_dates=["Sample_Date"] )) for file in QPCR]

@pytest.fixture
def seq_files():
    return [(file, pd.read_csv( file, parse_dates=["Date"] )) for file in SEQS]

@pytest.fixture
def seq_config():
    with open( SEQ_CONFIG, "r" ) as f:
        config = yaml.load( f, Loader=yaml.FullLoader )
    return config

@pytest.fixture
def seq_columns( seq_config ):
    columns = []
    for key in seq_config.keys():
        if key not in ["Other"]:
            columns.extend( seq_config[key]["members"] )
    return columns

def test_qpcr_contain_correct_colums( qpcr_files ):
    for file, df in qpcr_files:
        assert all( df.columns == QPCR_COLUMNS ), f"{file} does not have the right columns names. Want: {QPCR_COLUMNS} GOT: {df.columns}"

def test_qpcr_date_is_correct( qpcr_files ):
    for file, df in qpcr_files:
        assert ptypes.is_datetime64_any_dtype( df["Sample_Date"] ), f"{file} date column is incorrect dtype. Want: dtype('<M8[ns]') Got: {df['Sample_Date'].dtype}"
        assert ptypes.is_numeric_dtype( df["Mean viral gene copies/L"] ), f"{file} gene copies column is not numeric"

def test_other_entry_in_config( seq_config ):
    assert "Other" in seq_config, "YAML is not complete. Does not contain 'Other' entry."

def test_correct_keys_in_config( seq_config ):
    for key in seq_config.keys() :
        for value in ["name", "members", "color"] :
            assert value in seq_config[key], f"YAML entry {key} is not complete. Does not contain '{value}' entry."

# All the files are concated at some point so we just need columns to be present in one file or another.
def test_seqs_contain_requested_columns( seq_files, seq_columns ):
    total_cols = []
    for file, df in seq_files:
        total_cols.extend( df.columns )
    total_cols = set( total_cols )
    for variant in seq_columns:
        assert variant in total_cols, f"No sequence file contains column {variant} as request in config."

def test_seqs_columns_are_correct_format( seq_files, seq_columns ):
    for file, df in seq_files:
        for column in df.columns:
            if column == "Date":
                assert ptypes.is_datetime64_any_dtype( df["Date"] ), f"{file} date column is incorrect dtype. Want: dtype('<M8[ns]') Got: {df['Date'].dtype}"
            else:
                assert ptypes.is_numeric_dtype( df[column ] ), f"{file} column {column:q} is not numeric"