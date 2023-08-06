import pytest
import json
from delta_lake.DataLake import DataLake
from delta_lake.Util import Util
import delta_lake.const as const


class TestDataLake:

    def __init__(self, spark, storage_account_name, storage_account_access_key, storage_landing, storage_bronze,
                 input_data_param, mount_data_param, colums_validate_merge_param, new_name, database, target, origin):
        self.delta_lake=DataLake(spark, storage_account_name, storage_account_access_key, storage_landing,
                                 storage_bronze, input_data_param, mount_data_param, colums_validate_merge_param,
                                 new_name, database, target, origin)

    def test_initialize_config_storage(self):
        self.delta_lake.initialize_config_storage()
        list_folder = Util.list_folder_delta_lake("".format(self.storage_landing, const.test))
        assert len(list_folder) != 0

    def test_validate_tables(self):
        self.spark.sql("CREATE TABLE IF NOT EXISTS {0}.{1}".format(self.database, self.new_name))
        self.delta_lake.validate_tables()
        assert self.table_exist == True
        self.spark.sql("DROP TABLE {0}.{1}".format(self.database, self.new_name))

    def test_create_colums_merge(self):
        self.delta_lake.create_colums_merge()
        assert self.string_validate_columns == "{0}.{2} = {1}.{2}".format(self.delta_lake.origin,
                                                                          self.delta_lake.target,
                                                                          self.delta_lake.new_name)

    def test_create_json_columns_pass(self):
        self.create_json_columns_pass()
        assert self.delta_lake.json_load_insert_values == json.loads(const.json_colum_test)

