from abc import ABC, abstractmethod
from pyspark.sql.functions import *
import json


class DataLake(ABC):
    events = None
    string_validate_columns = ""
    input_data = ""
    mount_data = ""
    json_load_insert_values = {}
    colums_validate_merge = []

    def __init__(self, spark, storage_account_name, storage_account_access_key, storage_landing, storage_bronze,
                 input_data_param, mount_data_param, colums_validate_merge_param, new_name, database, target, origin):
        self.spark = spark
        self.storage_account_name=storage_account_name
        self.storage_account_access_key=storage_account_access_key
        self.storage_landing = storage_landing
        self.storage_bronze = storage_bronze
        self.input_data_param = input_data_param
        self.mount_data_param = mount_data_param
        self.colums_validate_merge_param = colums_validate_merge_param
        self.new_name = new_name
        self.table_name = new_name
        self.table_exist = False
        self.database = database
        self.target = target
        self.origin = origin



    abstractmethod
    def merge(self):
        pass

    abstractmethod
    def initialize_variables(self):
        pass

    abstractmethod
    def load_data(self):
        pass

    def initialize_config_storage(self):
        self.spark.conf.set(
            "fs.azure.account.key." + self.storage_account_name + ".blob.core.windows.net",
            self.storage_account_access_key)

    def validate_tables(self):
        list_tables = self.spark.catalog.listTables(self.database)
        for item in list_tables:
            print(item)
            print(type(item))
            print(item.name)
            self.table_exist = item.name.lower() == self.table_name.lower()
            if self.table_exist:
                break

    def load_data_csv(self, input_data):
        self.events = self.spark.read.format("csv").option("header", "true").load(input_data)

    def create_colums_merge(self):
        string_and = "and"
        for item in self.colums_validate_merge:
            condition = "{0}.{2} = {1}.{2}".format(self.origin, self.target, item)
            if item is not "":
                if self.string_validate_columns is "":
                    self.string_validate_columns = condition
                else:
                    self.string_validate_columns = "{0} {1} {2}".format(self.string_validate_columns, string_and, condition)
        print(self.string_validate_columns)

    def create_json_columns_pass(self):
        insert_values = "{"
        for item in self.colums_silver_array:
            if item is not "":
                insert_values = "{0}{1}".format(insert_values, '"{0}":"{1}.{0}", '.format(item, self.origin))

        insert_values = insert_values[0: len(insert_values) - 2] + '}'

        self.json_load_insert_values = json.loads(insert_values)
        print(self.json_load_insert_values)