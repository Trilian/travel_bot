#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = "9c2af855-06e0-4252-a525-c6a912fc7502"
    APP_PASSWORD = "da8bdf15-a842-4459-b10f-f1364501f93a"
    LUIS_APP_ID = "cafda911-e530-4237-8983-7452fa0cfe08"
    LUIS_API_KEY = "b8e697c56d0340e5a6df74609c2e5d5e"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "westeurope.api.cognitive.microsoft.com"
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "a9b05369-5c22-485c-9e2a-a05e190c22d0"
    )