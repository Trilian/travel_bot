# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from booking_details import BookingDetails


class Intent(Enum):
    BOOK_FLIGHT = "BookFlight"
    CANCEL = "Cancel"
    HELP = "Help"
    NONE_INTENT = "NoneIntent"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
            luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.BOOK_FLIGHT.value:
                result = BookingDetails()

                # We need to get the result from the LUIS JSON which at every level returns an array.
                dst_city_entities = recognizer_result.entities.get("$instance", {}).get(
                    "dst_city", []
                )

                if len(dst_city_entities) > 0:
                    result.destination = dst_city_entities[0]["text"].capitalize()

                or_city_entities = recognizer_result.entities.get("$instance", {}).get(
                    "or_city", []
                )
                if len(or_city_entities) > 0:
                    result.origin = or_city_entities[0]["text"].capitalize()

                budget_entities = recognizer_result.entities.get("$instance", {}).get(
                    "budget", []
                    )
                if len(budget_entities) > 0:

                    result.budget = budget_entities[0]["text"]

                start_date_entities = recognizer_result.entities.get("$instance", {}).get(
                    "str_date", []
                    )
                if start_date_entities:
                        timex = start_date_entities[0]["timex"]

                        if timex:
                            datetime = timex[0].split("T")[0]

                            result.start_date = datetime
                        else:
                            result.start_date = None

                end_date_entities = recognizer_result.entities.get("$instance", {}).get(
                    "end_date", []
                    )
                if end_date_entities:
                        timex = end_date_entities[0]["timex"]

                        if timex:
                            datetime = timex[0].split("T")[0]

                            result.end_date = datetime
                        else:
                            result.end_date = None
        except Exception as exception:
            print(exception)

        return intent, result
