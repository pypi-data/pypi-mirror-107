#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2021 4Paradigm
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from prettytable import PrettyTable
from pyspark.sql import SparkSession


def check_skew_args(args):
    check_skew(args.parquet_path)


def check_skew(parquet_path, distinct_threshold=100, max_count_threshold=0.2):
    spark_app_name = "DetectDataSkew"
    spark = SparkSession.builder.appName(spark_app_name).getOrCreate()

    # Read input parquet
    df = spark.read.parquet(parquet_path)
    df.createOrReplaceTempView("t1")

    # Generate SQL for distinct count for each row
    column_names = df.columns
    # Example SQL: SELECT COUNT(DISTINCT id), COUNT(DISTINCT vendor_id) FROM t1
    distinct_count_sql = "SELECT "
    for column_name in df.columns:
        distinct_count_sql += "COUNT(DISTINCT {}), ".format(column_name)
    distinct_count_sql = distinct_count_sql[:-2] + " FROM t1"
    # logging.warning("Generate distinct count SQL: {}".format(distinct_count_sql))

    # The flag of skew or not for each column
    skew_flags = [False for name in df.columns]

    # Check distinct count if it is less than threshold
    distinct_row = spark.sql(distinct_count_sql).collect()[0]
    distinct_count_result = ["Distinct values"]

    for index, column_name in enumerate(df.columns):
        distinct_count = distinct_row[index]
        logging.warning("Column {} has distinct values: {}".format(column_name, distinct_count))
        distinct_count_result.append(str(distinct_count))
        if distinct_count <= distinct_threshold:
            skew_flags[index] = True
            # logging.warning("May be skew with few distinct values for column {}!!!".format(column_name))

    # Check max count of single value if it is larger than threshold
    total_count = df.count()
    max_count_result = ["Max count"]
    max_count_ratio_result = ["Max count ratio"]

    for index, column_name in enumerate(df.columns):
        # Example SQL: SELECT COUNT(*) FROM t1 GROUP BY store_and_fwd_flag ORDER BY COUNT(*) DESC LIMIT 1
        groupby_count_sql = "SELECT COUNT(*) FROM t1 GROUP BY {} ORDER BY COUNT(*) DESC LIMIT 1".format(column_name)
        # logging.warning("Generate groupby count SQL: {}".format(distinct_count_sql))
        max_count = spark.sql(groupby_count_sql).collect()[0][0]
        max_count_result.append(str(max_count))
        max_count_ratio = max_count / total_count 
        max_count_ratio_result.append(str(max_count_ratio * 100) + "%")

        logging.warning("Column {} has value of max count: {}, ratio: {}".format(column_name, max_count, max_count_ratio))
        if max_count_ratio >= max_count_threshold:
            skew_flags[index] = True
            # logging.warning("May be skew with max count of single value for column {}!!!".format(column_name))

    # Print result as table
    print("Distinct count threshold: {}, max count ration threshold: {}".format(distinct_threshold, str(max_count_threshold * 100)+"%"))
    table = PrettyTable()
    table.field_names = [""] + df.columns
    table.add_row(distinct_count_result)
    table.add_row(max_count_result)
    table.add_row(max_count_ratio_result)
    table.add_row(["Skew"] + ["*" if skew_flag else "" for skew_flag in skew_flags])
    print(table)
