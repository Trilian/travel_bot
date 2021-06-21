


import sys
import pathlib
import pytest
import aiounittest
import asyncio


from botbuilder.testing.dialog_test_client import DialogTestClient
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.dialogs.prompts import (
    AttachmentPrompt, 
    PromptOptions, 
    PromptValidatorContext, 
)

from botbuilder.core import (
    TurnContext, 
    ConversationState, 
    MemoryStorage, 
    MessageFactory, 
)
from botbuilder.schema import Activity, ActivityTypes, Attachment
from botbuilder.dialogs import DialogSet, DialogTurnStatus
from botbuilder.core.adapters import TestAdapter
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from travel_bot.dialogs.booking_dialog import BookingDialog
from travel_bot.dialogs.main_dialog import MainDialog



class TestBookingDialog():
    def test_is_ambiguous(self):
    
        bd =  BookingDialog()
        ret = bd.is_ambiguous("what")
        
        assert ret

        ret = bd.is_ambiguous("2020-01-01")
        
        assert not ret


class TextPromptTest(aiounittest.AsyncTestCase):
    async def test_email_prompt(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = "Hello, What can I help you with today?"
                        )
                    )
                await dialog_context.prompt("textprompt", options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(reply)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        dialogs.add(TextPrompt("textprompt"))

        step1 = await adapter.test('Hello', 'Hello, What can I help you with today?')
        step2 = await step1.send('Book a flight')
        await step2.assert_reply('Book a flight')


class OriginTestBot(aiounittest.AsyncTestCase):
    async def test_email_prompt(self):
        async def exec_test(turn_context:TurnContext):
            dialog_context = await dialogs.create_context(turn_context)

            results = await dialog_context.continue_dialog()
            if (results.status == DialogTurnStatus.Empty):
                options = PromptOptions(
                    prompt = Activity(
                        type = ActivityTypes.message, 
                        text = "Where would you like to travel to?"
                        )
                    )
                await dialog_context.prompt("textprompt", options)

            elif results.status == DialogTurnStatus.Complete:
                reply = results.result
                await turn_context.send_activity(reply)

            await conv_state.save_changes(turn_context)

        adapter = TestAdapter(exec_test)

        conv_state = ConversationState(MemoryStorage())

        dialogs_state = conv_state.create_property("dialog-state")
        dialogs = DialogSet(dialogs_state)
        dialogs.add(TextPrompt("textprompt"))

        step1 = await adapter.test('book a flight', 'Where would you like to travel to?')
        step2 = await step1.send('Paris')
        await step2.assert_reply('Paris')