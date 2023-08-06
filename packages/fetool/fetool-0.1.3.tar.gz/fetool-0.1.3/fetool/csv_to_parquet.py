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
from pyspark.sql import SparkSession


def csv_to_parquet_args(args):
    csv_to_parquet(args.input_csv_path, args.output_parquet_path)


def csv_to_parquet(input_csv_path, output_parquet_path):
    spark_app_name = "CsvToParquet"
    spark = SparkSession.builder.appName(spark_app_name).getOrCreate()

    logging.warning("Load the csv dataset with header in {}".format(input_csv_path))
    df = spark.read.option("header", "true").option("inferSchema", "true").csv(input_csv_path)

    logging.warning("Save the output parquet in {}".format(output_parquet_path))
    df.write.parquet(output_parquet_path, mode="overwrite")
