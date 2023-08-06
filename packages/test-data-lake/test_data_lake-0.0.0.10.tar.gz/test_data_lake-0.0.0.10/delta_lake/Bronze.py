from delta_lake.DataLake import DataLake
from delta.tables import DeltaTable

class Bronze(DataLake):

    def __init__(self, spark, storage_account_name, storage_account_access_key, storage_landing, storage_bronze,
                 input_data_param, mount_data_param, colums_validate_merge_param, new_name, database, target, origin):
        super().__init__(spark, storage_account_name, storage_account_access_key, storage_landing, storage_bronze,
                 input_data_param, mount_data_param, colums_validate_merge_param, new_name, database, target, origin)
        self.initialize_variables()


    def merge(self):
        try:
            if self.table_exist:
                deltaTable = DeltaTable.forPath(self.spark, self.mount_data)
                deltaTable.alias(self.target) \
                    .merge(self.events.alias(self.origin), self.string_validate_columns) \
                    .whenMatchedUpdateAll() \
                    .whenNotMatchedInsertAll() \
                    .execute()
            else:
                self.events.write.format("delta").save(self.mount_data)

                self.spark.sql("CREATE TABLE IF NOT EXISTS {0}.{1} USING DELTA LOCATION '{2}'".format(self.database,
                                                                                                 self.table_name,
                                                                                                 self.mount_data))
        except Exception as e:
            print("Error update or create table: " + self.table_name + " explain: " + str(e))

    def initialize_variables(self):
        self.input_data = "{0}{1}".format(self.storage_landing, self.input_data_param)
        self.mount_data = "{0}{1}".format(self.storage_bronze, self.mount_data_param)
        self.colums_validate_merge = self.colums_validate_merge_param.split(',')

    def load_data(self, input_data):
        self.events = self.spark.read.parquet(input_data)