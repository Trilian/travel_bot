#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = "f6e44223-91c7-429c-88b2-4669a74182df"
    APP_PASSWORD = "d72707e7-4331-4253-8f33-682fd6b72199"
    LUIS_APP_ID = "cafda911-e530-4237-8983-7452fa0cfe08"
    LUIS_API_KEY = "b8e697c56d0340e5a6df74609c2e5d5e"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "westeurope.api.cognitive.microsoft.com"
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "a9b05369-5c22-485c-9e2a-a05e190c22d0"
    )

