import pytest
from delta_lake.Bronze import Bronze
from delta_lake.Util import Util


class TestBronze:

    def __init__(self, spark, storage_account_name, storage_account_access_key, storage_landing, storage_bronze,
                 input_data_param, input_data_param_v1, input_data_param_v2, input_data_param_v3,
                 colums_validate_merge_param, new_name, database, target, origin, colum_filter, value_filter,
                 colum_validate_data, value_validate_data):
        self.colum_filter = colum_filter
        self.value_filter = value_filter
        self.colum_validate_data = colum_validate_data
        self.value_validate_data = value_validate_data
        self.delta_lake_v1 = Bronze(spark, storage_account_name, storage_account_access_key, storage_landing,
                                 storage_bronze, input_data_param, input_data_param_v1, colums_validate_merge_param,
                                 new_name, database, target, origin)
        self.delta_lake_v2 = Bronze(spark, storage_account_name, storage_account_access_key, storage_landing,
                                    storage_bronze, input_data_param, input_data_param_v2, colums_validate_merge_param,
                                    new_name, database, target, origin)
        self.delta_lake_v3 = Bronze(spark, storage_account_name, storage_account_access_key, storage_landing,
                                    storage_bronze, input_data_param, input_data_param_v3, colums_validate_merge_param,
                                    new_name, database, target, origin)

    def test_bronze(self):
        self.delta_lake_v1.initialize_config_storage()
        self.delta_lake_v1.validate_tables()
        self.delta_lake_v1.create_colums_merge()
        self.delta_lake_v1.load_data_csv(self.delta_lake_v1.input_data)
        self.delta_lake_v1.initialize_config_storage()
        self.delta_lake_v1.merge()
        df = self.spark.delta_lake_v1.sql("select * from {0}.{1}").format(self.delta_lake_v1.database,
                                                                          self.delta_lake_v1.table_name)
        assert df.count() == 5

        self.delta_lake_v2.initialize_config_storage()
        self.delta_lake_v2.validate_tables()
        self.delta_lake_v2.create_colums_merge()
        self.delta_lake_v2.load_data_csv(self.delta_lake_v2.input_data)
        self.delta_lake_v2.initialize_config_storage()
        self.delta_lake_v2.merge()
        df = self.delta_lake_v2.spark.sql("select * from {0}.{1}").format(self.delta_lake_v1.database,
                                                                          self.delta_lake_v1.table_name)
        assert df.count() == 11

        self.delta_lake_v3.initialize_config_storage()
        self.delta_lake_v3.validate_tables()
        self.delta_lake_v3.create_colums_merge()
        self.delta_lake_v3.load_data_csv(self.delta_lake_v3.input_data)
        self.delta_lake_v3.initialize_config_storage()
        self.delta_lake_v3.merge()
        df = self.spark.sql("select {0} From {1}.{2} where {3}={4}").format(self.colum_validate_data,
                                                                            self.delta_lake_v1.database,
                                                                            self.delta_lake_v1.table_name,
                                                                            self.colum_filter, self.value_filter)
        value = df.collect()
        assert value[0][self.colum_validate_data] == self.value_validate_data
        self.delta_lake_v1.spark.sql("DROP TABLE {0}.{1}".format(self.delta_lake_v1.database,
                                                                 self.delta_lake_v1.table_name))
        list_file = Util.list_folder_delta_lake(self.delta_lake_v1.mount_data)
        for item in list_file:
            Util.delete_file_delta_lake(item.path)
