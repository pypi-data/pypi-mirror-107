# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2021
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------


import json
import pathlib
import tarfile
import tempfile
import uuid

import pyspark.sql.functions as F
from ibm_wos_utils.joblib.utils.param_utils import get

spark_to_db2_map = {
    "boolean": "boolean",
    "byte": "bigint",
    "short": "bigint",
    "integer": "bigint",
    "long": "bigint",
    "float": "double",
    "double": "double",
    "timestamp": "timestamp",
    "string": "varchar",
    "binary": "blob"
}

def __generate_table_name(prefix, suffix=None):
    return "{}_table_{}".format(
        prefix, suffix or str(
            uuid.uuid4())).replace(
        "-", "")


def __generate_table_ddl(
        ddl_fields,
        table_name: str,
        schema_name: str,
        max_length_categories: dict = {}):

    if not schema_name:
        raise Exception("Schema Name is required.")
    
    if not table_name:
        raise Exception("Table Name is required")
    
    column_string = "("
    collection_items = False

    for field in ddl_fields:
        feature_name = field.get("name")
        feature_type = field.get("type")

        if isinstance(feature_type, dict):
            feature_type = "varchar"
        else:
            db2_element_type = spark_to_db2_map.get(feature_type)
            if db2_element_type is not None:
                feature_type = db2_element_type
                
        get_varchar_length = lambda x: max(64, get(max_length_categories, x, 32)*2)

        if feature_type == "varchar":
            if get(field, "metadata.modeling_role") == "probability":
                feature_type += "(32000)"
            else:
                feature_type += "({})".format(get_varchar_length(feature_name))

        column_string += "\"{}\" {}".format(feature_name, feature_type.upper())
        
        if get(field, "metadata.modeling_role") in ["prediction", "target", "probability", "record-id", "record-timestamp"]:
            column_string += " NOT NULL"
            
        if get(field, "metadata.modeling_role") == "record-id":
            column_string += " PRIMARY KEY"
            
        column_string += ", "

    ddl_column_string = column_string[:-2] + ")"

    ddl_string = "CREATE TABLE \"{}\".\"{}\" {};".format(
        schema_name, table_name, ddl_column_string)

    return ddl_string

def __generate_table_ddl_from_schema(schema_name: str, table_name: str, table_schema: dict, primary_key_cols: list = []):
    if not schema_name:
        raise Exception("Schema Name is required.")
    
    if not table_name:
        raise Exception("Table Name is required")

    column_components = []
    for column, column_meta in table_schema["columns"].items():
        db2_element_type = spark_to_db2_map.get(column_meta["type"])
        if db2_element_type is None:
            db2_element_type = column_meta["type"]
        
        column_string = "\"{}\" {}".format(column, db2_element_type.upper())
        
        if "length" in column_meta:
            column_string += "({})".format(column_meta["length"])
            
        if column_meta.get("not_null"):
            column_string  += " NOT NULL"
            
        if column_meta.get("unique") and not len(primary_key_cols):
            column_string += " PRIMARY KEY"
            
        if "default" in column_meta:
            column_string += " DEFAULT {}".format(column_meta["default"])
        
        column_components.append(column_string)

    if len(primary_key_cols):
        primary_key_cols = ["\"{}\"".format(col) for col in primary_key_cols]
        primary_key_str = "PRIMARY KEY({})".format(",".join(primary_key_cols))
        column_components.append(primary_key_str)
        
    ddl_string = "CREATE TABLE \"{}\".\"{}\" ({});".format(
        schema_name, table_name, ", ".join(column_components))
    
    return ddl_string


def generate_scored_training_table_ddl(
        common_config_data,
        schema_name: str,
        table_prefix: str = "scored_training",
        table_suffix: str = None,
        max_length_categories: dict = {}):
    """Generates Create DDL statement for Scored Training Table of an IBM Watson OpenScale batch subscription.

    Arguments:
        common_config_data {dict} -- Common Configuration JSON
        schema_name {str} -- Schema Name where the table is to be created.

    Keyword Arguments:
        table_prefix {str} -- Prefix for this table name (default: {"scored_training"})
        table_suffix {str} -- Suffix for this table name. Defaults to a random UUID.
        max_length_categories {dict} -- Dictionary with Categorical Columns as keys, and maximum length of categories as values (default: {{}})

    Returns:
        str -- Create DDL statement for Scored Training Table
    """

    table_suffix = table_suffix or str(uuid.uuid4())
    table_name = __generate_table_name(table_prefix, table_suffix)
    common_configuration = common_config_data["common_configuration"]
    output_data_schema = common_configuration.get("output_data_schema")
    ddl_fields = common_configuration.get(
        "training_data_schema")["fields"].copy()

    for field in output_data_schema["fields"]:
        modeling_role = field["metadata"].get("modeling_role")

        if modeling_role in (
            "probability",
                "prediction"):
            ddl_fields.append(field)

    return __generate_table_ddl(
        ddl_fields,
        table_name,
        schema_name,
        max_length_categories)


def generate_feedback_table_ddl(
        common_config_data,
        schema_name: str,
        table_prefix: str = "feedback",
        table_suffix: str = None,
        max_length_categories: dict = {}):
    """Generates Create DDL statement for Feedback Table of an IBM Watson OpenScale batch subscription.

    Arguments:
        common_config_data {dict} -- Common Configuration JSON
        schema_name {str} -- Schema Name where the table is to be created.

    Keyword Arguments:
        table_prefix {str} -- Prefix for this table name (default: {"feedback"})
        table_suffix {str} -- Suffix for this table name. Defaults to a random UUID.
        max_length_categories {dict} -- Dictionary with Categorical Columns as keys, and maximum length of categories as values (default: {{}})

    Returns:
        str -- Create DDL statement for Feedback Table
    """

    table_suffix = table_suffix or str(uuid.uuid4())
    table_name = __generate_table_name(table_prefix, table_suffix)
    common_configuration = common_config_data["common_configuration"]
    output_data_schema = common_configuration.get("output_data_schema")
    ddl_fields = common_configuration.get(
        "training_data_schema")["fields"].copy()

    for field in output_data_schema["fields"]:
        modeling_role = field["metadata"].get("modeling_role")

        if modeling_role in (
            "probability",
            "prediction",
            "record-timestamp",
                "record-id"):
            ddl_fields.append(field)

    return __generate_table_ddl(
        ddl_fields,
        table_name,
        schema_name,
        max_length_categories)

def generate_payload_table_ddl(
        common_config_data,
        schema_name: str,
        table_prefix: str = "payload",
        table_suffix: str = None,
        max_length_categories: dict = {},
        create_index: bool = True):
    """Generates Create DDL statement for Payload Table of an IBM Watson OpenScale batch subscription.

    Arguments:
        common_config_data {dict} -- Common Configuration JSON
        schema_name {str} -- Schema Name where the table is to be created.

    Keyword Arguments:
        table_prefix {str} -- Prefix for this table name (default: {"payload"})
        table_suffix {str} -- Suffix for this table name. Defaults to a random UUID.
        max_length_categories {dict} -- Dictionary with Categorical Columns as keys, and maximum length of categories as values (default: {{}})
        create_index {bool} -- Flag to control whether an index is created on record-timestamp column. (default: {True})

    Returns:
        str -- Create DDL statement for Payload Table
    """

    table_suffix = table_suffix or str(uuid.uuid4())
    table_name = __generate_table_name(table_prefix, table_suffix)
    common_configuration = common_config_data["common_configuration"]
    output_data_schema = common_configuration.get("output_data_schema")
    ddl_fields = [field for field in common_configuration.get("training_data_schema")[
        "fields"] if get(field, "metadata.modeling_role") != "target"]
    record_timestamp = None
    for field in output_data_schema["fields"]:
        modeling_role = field["metadata"].get("modeling_role")

        if modeling_role in (
            "probability",
            "prediction",
            "record-timestamp",
                "record-id"):
            ddl_fields.append(field)
        if modeling_role == "record-timestamp":
            record_timestamp = field.get("name")

    result = __generate_table_ddl(
        ddl_fields,
        table_name,
        schema_name,
        max_length_categories)

    if create_index and (record_timestamp is not None):
        result += "\n"
        result += "CREATE INDEX \"{1}_index\" ON \"{0}\".\"{1}\" (\"{2}\" DESC)".format(schema_name, table_name, record_timestamp)
    return result

def generate_drift_table_ddl(
        drift_archive: bytearray,
        schema_name: str,
        table_prefix: str = "drifted_transactions",
        table_suffix: str = None):
    """Generates Create DDL statement for Drifted Transactions Table of an IBM Watson OpenScale batch subscription.

    Arguments:
        drift_archive {bytearray} -- Drift Archive
        schema_name {str} -- Schema Name where the table is to be created.

    Keyword Arguments:
        table_prefix {str} -- Prefix for this table name (default: {"drifted_transactions"})
        table_suffix {str} -- Suffix for this table name. Defaults to a random UUID.

    Returns:
        str -- Create DDL statement for Drifted Transactions Table
    """

    table_suffix = table_suffix or str(uuid.uuid4())
    table_name = __generate_table_name(table_prefix, table_suffix)

    table_schema = {}
    with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file.write(drift_archive)
        tmp_file.flush()
        with tarfile.open(tmp_file.name, "r:gz") as tf:
            with tf.extractfile("drifted_transactions_schema.json") as json_data:
                table_schema = json.load(json_data)
    
    result = __generate_table_ddl_from_schema(schema_name, table_name, table_schema, primary_key_cols=["scoring_id", "run_id"])
    result += "\n"
    result += "CREATE INDEX \"{1}_index\" ON \"{0}\".\"{1}\" (\"run_id\", \"is_model_drift\", \"is_data_drift\")".format(schema_name, table_name)
    return result

def generate_explanations_table_ddl(
        schema_name: str,
        table_prefix: str = "explanations",
        table_suffix: str = None):
    """Generates Create DDL statement for Explanations Table of an IBM Watson OpenScale batch subscription.

    Arguments:
        schema_name {str} -- Schema Name where the table is to be created.

    Keyword Arguments:
        table_prefix {str} -- Prefix for this table name (default: {"explanations"})
        table_suffix {str} -- Suffix for this table name. Defaults to a random UUID.

    Returns:
        str -- Create DDL statement for Explanations Table
    """

    table_suffix = table_suffix or str(uuid.uuid4())
    table_name = __generate_table_name(table_prefix, table_suffix)
    
    table_schema = {}
    
    current_dir = str(pathlib.Path(__file__).parent.absolute())
    with open(current_dir + "/explanations_table.json", "r") as fp:
        table_schema = json.load(fp)
    
    result = __generate_table_ddl_from_schema(schema_name, table_name, table_schema)
    result += "\n"
    result += "CREATE INDEX \"{1}_index\" ON \"{0}\".\"{1}\" (\"subscription_id\", \"request_id\", \"scoring_id\", \"finished_at\" DESC)".format(schema_name, table_name)

    return result

