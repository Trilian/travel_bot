# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os.path

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import (
    MessageFactory,
    CardFactory,
    TurnContext,
)
from botbuilder.schema import InputHints, Activity, Attachment, ChannelAccount

from booking_details import BookingDetails
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from dialogs.booking_dialog import BookingDialog

from config import DefaultConfig
CONFIG = DefaultConfig()

class MainDialog(ComponentDialog):
    def __init__(
            self,
            luis_recognizer: FlightBookingRecognizer,
            booking_dialog: BookingDialog
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        text_prompt = TextPrompt(TextPrompt.__name__)

        wf_dialog = WaterfallDialog(
            "WFDialog", [self.intro_step, self.act_step, self.final_step, self.greeting_step]
        )
 
        self._luis_recognizer = luis_recognizer
        self._booking_dialog_id = booking_dialog.id

        self.add_dialog(text_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(booking_dialog)
        self.add_dialog(wf_dialog)

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        message_text = (
            str(step_context.options)
            if step_context.options
            else "What can I help you with today?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

        return await step_context.next(None)
    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty BookingDetailsInstance.
            return await step_context.begin_dialog(
                self._booking_dialog_id, BookingDetails()
            )

        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )
        if intent == Intent.BOOK_FLIGHT.value and luis_result:
            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._booking_dialog_id, luis_result)
            
        if intent == Intent.CANCEL.value:
            get_cancel_text = "Ok your travel is cancelled !"
            get_cancel_message = MessageFactory.text(
                get_cancel_text, get_cancel_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_cancel_message)

            return await step_context.next(None)

        else:
            properties = {}
            properties['intent'] = intent
            
            self.telemetry_client.track_event("UnrecognizedIntent", properties, 3)
            self.telemetry_client.flush()

            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        if step_context.result is not None:
            result = step_context.result

            # Now we have all the booking details call the booking service.

            # If the call to the booking service was successful tell the user.
            card = self.create_adaptive_card_attachment(result)
            response = MessageFactory.attachment(card)
            await step_context.context.send_activity(response)

        message_text = "What else can I do for you?"
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        #return await step_context.replace_dialog(self.id, prompt_message)
        
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def greeting_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            message_text = "I’m the traveler agent, How can I help you ?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )   
            await step_context.context.send_activity(prompt_message)
            
            return await step_context.replace_dialog(self.id)

        else :
            message_text = "Thank you for your booking and good bye !"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )   
            await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
            return await step_context.end_dialog(self.id)
            
    def replace(self, template: dict, data: dict):
        import re
        str_temp = str(template)
        for key in data:
            pattern = "\${" + key + "}"
            str_temp = re.sub(pattern, str(data[key]), str_temp)
        return eval(str_temp)

    # Load attachment from file.
    def create_adaptive_card_attachment(self, result):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "../cards/flightCard.json")

        with open(path) as in_file:
            card_template = json.load(in_file)
        budget = result.budget + "$"
        destination = result.destination
        origin = result.origin
        start_date = result.start_date
        end_date = result.end_date

        template_data = {"budget": budget, "destination": destination, "origin": origin, "start_date": start_date, "end_date": end_date}
        card = self.replace(card_template, template_data)
        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card
        )

