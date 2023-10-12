# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#!/usr/bin/env python3

import aws_cdk as cdk 

from airflow_cdk.airflow_cdk_vpc import AirflowCdkStackVPC
from airflow_cdk.airflow_cdk_eks import AirflowCdkStackEKS
from airflow_cdk.airflow_cdk_rds import AirflowCdkStackRDS

env=cdk.Environment(region="eu-west-1", account="XXXXXXX")
airflow_props = {'airflow_env' : 'airflow-ato-demo', 'rds_name' : 'atordstest'}


app = cdk.App()

airflow_eks_cluster_vpc = AirflowCdkStackVPC(
    scope=app,
    id="airflow-ato-vpc",
    env=env
)

airflow_eks_cluster_rds = AirflowCdkStackRDS(
    scope=app,
    id="airflow-ato-rds",
    env=env,
    vpc=airflow_eks_cluster_vpc.vpc,
    airflow_props=airflow_props
)

airflow_eks_cluster = AirflowCdkStackEKS(
    scope=app,
    id="airflow-ato-eks",
    env=env,
    vpc=airflow_eks_cluster_vpc.vpc,
    airflow_props=airflow_props
)

app.synth()
