#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
<<<<<<< HEAD
    APP_ID = ""
    APP_PASSWORD = ""
    LUIS_APP_ID = "5705e735-228d-430c-94fd-cab67b7f69ae"
    LUIS_API_KEY = "b8e697c56d0340e5a6df74609c2e5d5e"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "westeurope.api.cognitive.microsoft.com"
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "cfb53cfc-b75a-4d5f-bdc7-db9eb6d86bec"
    )
=======
    APP_ID = "9c2af855-06e0-4252-a525-c6a912fc7502"
    APP_PASSWORD = "5myP_L_w_uN86cujUW18t1xp1.xcZEnxP-"
    LUIS_APP_ID = "9a4d53de-3156-4e7a-80ec-30803825ce2f"
    LUIS_API_KEY = "b8e697c56d0340e5a6df74609c2e5d5e"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = "westeurope.api.cognitive.microsoft.com"
    APPINSIGHTS_INSTRUMENTATION_KEY = "5d803f79-22bd-47a9-be82-831e81c189b7"
>>>>>>> 2703a99832f4b083441414c98f81ff737d1f38c9
