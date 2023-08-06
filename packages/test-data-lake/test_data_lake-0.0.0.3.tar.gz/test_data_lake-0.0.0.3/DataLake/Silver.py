from DataLake import DataLake


class Silver(DataLake):
    colums_silver_array = []

    def __init__(self):
        super().__init__()
        self.initialize_variables()

    def merge(self):
        try:
            if self.table_exist:
                deltaTable = DeltaTable.forPath(spark, self.mount_data)
                deltaTable.alias(self.target) \
                    .merge(self.events.alias(self.origin), self.string_validate_columns) \
                    .whenMatchedUpdate(set=self.json_load_insert_values) \
                    .whenNotMatchedInsert(values=self.json_load_insert_values) \
                    .execute()
            else:
                self.events.write.format("delta").save(self.mount_data)
                spark.sql("CREATE TABLE IF NOT EXISTS {0}.{1} USING DELTA LOCATION '{2}'".format(self.database, self.table_name,
                                                                                                 self.mount_data))
        except Exception as e:
            print("Error update or create table: " + self.table_name + " explain: " + str(e))


    def initialize_variables(self):
        self.input_data = "{0}{1}".format(self.storage_bronce, self.mount_data_params)
        self.mount_data = "{0}{1}".format(self.storage_silver, self.mount_data_params)
        self.colums_validate_merge = self.colums_validate_merge_params.split(',')
        self.colums_silver_array = self.colums_silver.split(',')

    def load_data(self, input_data):
        self.events = spark.read.format("delta").load("{0}".format(input_data))