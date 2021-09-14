import os

from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext

# Goal of this is to read all the text files into two spark dataframes

conf = SparkConf().setMaster("local").setAppName("baby_names")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)


def get_data_national_level(directory):
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, f)) and f.endswith(".txt")]

    def get_year(name):
        new_name = name.replace('names/yob', '').replace('.txt', '')
        return new_name

    def list_append(lst, item):
        lst.append(item)
        return lst

    listed_items = list()
    for file in all_files:
        year = get_year(file)
        rdd = sc.textFile(file)
        split_data = rdd.map(lambda x: tuple(list_append(x.split(','), year))).collect()
        listed_items += split_data
    data = spark.createDataFrame(listed_items, ['name', 'gender', 'count', 'year'])
    data.show()
    return data


def get_data_state_level(directory):
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, f)) and f.endswith(".TXT")]

    listed_items = list()
    for file in all_files:
        rdd = sc.textFile(file)
        split_data = rdd.map(lambda x: x.split(',')).collect()
        listed_items += split_data
    data = spark.createDataFrame(listed_items, ['state', 'gender', 'year', 'name', 'count'])
    data.show()
    return data


if __name__ == '__main__':
    get_data_national_level('names')
    get_data_state_level('namesbystate')
    spark.stop()