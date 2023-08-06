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

import os
import logging
import yaml
from py4j.java_gateway import JavaGateway
from py4j.java_gateway import GatewayParameters


def gen_fedb_ddl_args(args):
    gen_fedb_ddl(args.yaml_path)


def gen_fedb_ddl(yaml_path):
    if "SPARK_HOME" not in os.environ:
        print("SPARK_HOME should be set for fetool gen_fedb_ddl")
        return -1

    # Read yaml file
    try:
        yaml_config = yaml.load(open(yaml_path, "r"))
    except yaml.YAMLError as exc:
        mark = exc.problem_mark
        logging.error("Error position: (%s:%s)" % (mark.line + 1, mark.column + 1))
        exit(-1)

    # TODO: change with spark home jars
    #classpath = os.path.join(os.environ["SPARK_HOME"], "jars/")
    classpath = "/Users/tobe/code/4pd/SparkFE/sparkfe/target/sparkfe-0.1.1-macos-SNAPSHOT.jar"
    #classpath = "/Users/tobe/code/4pd/SparkFE/spark/temp/spark-3.0.0-bin-sparkfe/jars/:/Users/tobe/code/4pd/SparkFE/sparkfe/target/sparkfe-0.1.1-macos-SNAPSHOT.jar"

    # Start the jvm gateway
    gateway = JavaGateway.launch_gateway(classpath=classpath, die_on_exit=True)

    # Get Registered tables
    nameParquetMap = gateway.jvm.java.util.HashMap()
    for k, v in yaml_config.get("tables", {}).items():
        nameParquetMap.put(k, v)

    # Read SQL file
    if "sql_file" in yaml_config:
        with open(yaml_config.get("sql_file"), "r") as f:
            sql_text = f.read()
    else:
        sql_text = yaml_config.get("sql_text")

    # TODO: Use test sql
    sql_text = "SELECT * FROM t1;"

    fetool_entrypoint = gateway.jvm.com._4paradigm.hybridsql.sparkfe.FetoolEntryPoint()

    ddl_sql = fetool_entrypoint.genFedbDdl(nameParquetMap, sql_text, 10, 10)

    print("Get result ddl sql: {}".format(ddl_sql))
