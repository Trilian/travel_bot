#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = ""
    APP_PASSWORD = ""
    LUIS_APP_ID = "5705e735-228d-430c-94fd-cab67b7f69ae"
    LUIS_API_KEY = "b8e697c56d0340e5a6df74609c2e5d5e"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "westeurope.api.cognitive.microsoft.com"
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "cfb53cfc-b75a-4d5f-bdc7-db9eb6d86bec"
    )
