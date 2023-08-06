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


def inspect_parquet_args(args):
    inspect_parquet(args.parquet_path)


def inspect_parquet(parquet_path):
    spark_app_name = "InspectParquet"
    spark = SparkSession.builder.appName(spark_app_name).getOrCreate()

    # Read input parquet
    df = spark.read.parquet(parquet_path)

    logging.warning("Display the schema")
    df.printSchema()

    logging.warning("Display the summary information")
    # count/mean/stddev/min/25%/50%/75%/max
    df.summary().show()

    logging.warning("Display the sample data")
    df.show(3)
