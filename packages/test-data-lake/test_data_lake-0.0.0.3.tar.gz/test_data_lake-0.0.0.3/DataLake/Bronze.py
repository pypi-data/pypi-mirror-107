import DataLake
class Bronze(DataLake):

    def __init__(self):
        super().__init__()
        initialize_variables()


    def merge(self):
        try:
            if self.table_exist:
                deltaTable = DeltaTable.forPath(spark, self.mount_data)
                deltaTable.alias(self.target) \
                    .merge(self.events.alias(self.origin), self.string_validate_columns) \
                    .whenMatchedUpdateAll() \
                    .whenNotMatchedInsertAll() \
                    .execute()
            else:
                self.events.write.format("delta").save(self.mount_data)

                spark.sql("CREATE TABLE IF NOT EXISTS {0}.{1} USING DELTA LOCATION '{2}'".format(self.database,
                                                                                                 self.table_name,
                                                                                                 self.mount_data))
        except Exception as e:
            print("Error update or create table: " + self.table_name + " explain: " + str(e))

    def initialize_variables(self):
        self.input_data = "{0}{1}".format(self.storage_landing, self.input_data_param)
        self.mount_data = "{0}{1}".format(self.storage_bronce, self.mount_data_param)
        self.colums_validate_merge = self.colums_validate_merge_param.split(',')

    def load_data(self, input_data):
        self.events = spark.read.parquet(input_data)