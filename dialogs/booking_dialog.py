# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datatypes_date_time.timex import Timex
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog


from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module
from datetime import datetime

class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__,
        )
        text_prompt = TextPrompt(TextPrompt.__name__)

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.destination_step,
                self.origin_step,
                self.budget_step,
                self.start_date_step,
                self.end_date_step,
                self.confirm_step,
                self.final_step,
            ],
        )
        self.add_dialog(text_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateResolverDialog(DateResolverDialog.__name__))
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__
        self.logger = None
        self.stats = stats_module.stats
        self.view_manager = self.stats.view_manager
        self.stats_recorder = self.stats.stats_recorder
        self.bot_measure = measure_module.MeasureInt("botdefects",
                                           "number of bot defects",
                                           "botdefects")
        self.bot_view = view_module.View("defect view",
                                    "number of bot defects",
                                    [],
                                    self.bot_measure,
                                    aggregation_module.CountAggregation())
        self.view_manager.register_view(self.bot_view)
        self.mmap = self.stats_recorder.new_measurement_map()
        self.tmap = tag_map_module.TagMap()
        self.metrics_exporter = None
        self.message_history = set()

    def set_logger(self, logger):
        self.logger = logger

    def set_metrics_exporter(self, metrics_exporter):
        self.metrics_exporter = metrics_exporter
        self.view_manager.register_exporter(metrics_exporter)

    async def destination_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a destination city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options
        self.message_history.add(step_context._turn_context.activity.text)
        print("from :",booking_details.origin)
        print("to :",booking_details.destination)
        print("start date  :",booking_details.start_date)
        print("end date  :",booking_details.end_date)
        print("budget :",booking_details.budget)

        if booking_details.destination is None:
            message_text = "Where would you like to travel to?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(booking_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If an origin city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options
        print("User message : ",step_context._turn_context.activity.text)
        self.message_history.add(step_context._turn_context.activity.text)

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result

        if booking_details.origin is None:
            message_text = "From what city will you be travelling?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(booking_details.origin)

    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If an origin city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options
        self.message_history.add(step_context._turn_context.activity.text)
        # Capture the response to the previous step's prompt
        booking_details.origin = step_context.result
        if booking_details.budget is None:
            message_text = "What is your budget?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(booking_details.budget)

    async def start_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If an origin city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """

        booking_details = step_context.options
        self.message_history.add(step_context._turn_context.activity.text)


        # Capture the results of the previous step
        booking_details.budget = step_context.result
        #if booking_details.start_date is None:
         #   message_text = "What is your start date?"
         #   prompt_message = MessageFactory.text(
         #       message_text, message_text, InputHints.expecting_input
         #   )
         #   return await step_context.prompt(
         #       TextPrompt.__name__, PromptOptions(prompt=prompt_message)
         #   )


        if not booking_details.start_date or self.is_ambiguous(
            booking_details.start_date
        ):
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, {"field":booking_details.start_date,"booking_details":booking_details}
            )
        return await step_context.next(booking_details.start_date)

    async def end_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If an origin city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.start_date = step_context.result
        if not booking_details.end_date or self.is_ambiguous(
            booking_details.end_date
        ):
             return await step_context.begin_dialog(
                DateResolverDialog.__name__, {"field":booking_details.end_date,"booking_details":booking_details}
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.end_date)


    async def confirm_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        Confirm the information the user has provided.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.end_date = step_context.result
        message_text = (
            f"Please confirm, I have you traveling to: {booking_details.destination} from: "
            f"{booking_details.origin} for: {booking_details.budget}."
            f"The flight is betwenn {booking_details.start_date} and {booking_details.end_date}"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        if step_context.result:
            booking_details = step_context.options

            return await step_context.end_dialog(booking_details)


        properties = {'custom_dimensions': {'booking_details': step_context.options.get_details(),'message_history':str(self.message_history)}}

        self.logger.warning("User has not confirmed flight",extra=properties)
        self.mmap.measure_int_put(self.bot_measure, 1)
        self.mmap.record(self.tmap)
        metrics = list(self.mmap.measure_to_view_map.get_metrics(datetime.utcnow()))
        print(metrics[0].time_series[0].points[0])

        get_sorry_text = "I'm sorry I couldn't help you"
        get_sorry_message = MessageFactory.text(
            get_sorry_text, get_sorry_text, InputHints.ignoring_input
        )
        await step_context.context.send_activity(get_sorry_message)
        return await step_context.end_dialog()


    def is_ambiguous(self, timex: str) -> bool:
        """ Ensure time is correct.
        """

        timex_property = Timex(timex)
        return "definite" not in timex_property.types
