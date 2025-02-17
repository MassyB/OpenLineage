# Copyright 2018-2025 contributors to the OpenLineage project
# SPDX-License-Identifier: Apache-2.0

import pytest
from openlineage.common.provider.snowflake import fix_account_name, fix_snowflake_sqlalchemy_uri


@pytest.mark.parametrize(
    "source,target",
    [
        (
            "snowflake://user:pass@xy123456.us-east-1.aws/database/schema",
            "snowflake://xy123456.us-east-1.aws/database/schema",
        ),
        (
            "snowflake://xy123456/database/schema",
            "snowflake://xy123456.us-west-1.aws/database/schema",
        ),
        (
            "snowflake://xy12345.ap-southeast-1/database/schema",
            "snowflake://xy12345.ap-southeast-1.aws/database/schema",
        ),
        (
            "snowflake://user:pass@xy12345.south-central-us.azure/database/schema",
            "snowflake://xy12345.south-central-us.azure/database/schema",
        ),
        (
            "snowflake://user:pass@xy12345.us-east4.gcp/database/schema",
            "snowflake://xy12345.us-east4.gcp/database/schema",
        ),
        (
            "snowflake://user:pass@organization-account/database/schema",
            "snowflake://organization-account/database/schema",
        ),
        (
            "snowflake://user:p[ass@organization-account/database/schema",
            "snowflake://organization-account/database/schema",
        ),
        (
            "snowflake://user:pass@organization]-account/database/schema",
            "snowflake://organization%5D-account/database/schema",
        ),
    ],
)
def test_snowflake_sqlite_account_urls(source, target):
    assert fix_snowflake_sqlalchemy_uri(source) == target


# Unit Tests using pytest.mark.parametrize
@pytest.mark.parametrize(
    "name, expected",
    [
        ("xy12345", "xy12345.us-west-1.aws"),  # No '-' or '_' in name
        ("xy12345.us-west-1.aws", "xy12345.us-west-1.aws"),  # Already complete locator
        ("xy12345.us-west-2.gcp", "xy12345.us-west-2.gcp"),  # Already complete locator for GCP
        ("xy12345aws", "xy12345aws.us-west-1.aws"),  # AWS without '-' or '_'
        ("xy12345-aws", "xy12345-aws"),  # AWS with '-'
        ("xy12345_gcp-europe-west1", "xy12345.europe-west1.gcp"),  # GCP with '_'
        ("myaccount_gcp-asia-east1", "myaccount.asia-east1.gcp"),  # GCP with region and '_'
        ("myaccount_azure-eastus", "myaccount.eastus.azure"),  # Azure with region
        ("myorganization-1234", "myorganization-1234"),  # No change needed
        ("my.organization", "my.organization.us-west-1.aws"),  # Dot in name
    ],
)
def test_fix_account_name(name, expected):
    assert fix_account_name(name) == expected
    assert (
        fix_snowflake_sqlalchemy_uri(f"snowflake://{name}/database/schema")
        == f"snowflake://{expected}/database/schema"
    )
