from typing import Any, Text, Dict
from enums.custom_event_type import CustomEventType
from enums.navigation.navigation_screens import NavigationScreens

from model.action_model import ActionModel
from model.custom_event_model import CustomEventModel
from model.next_action import NextAction
from enums.recording.recording_requirements import RecordingRequirements

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from enums.recording.bluetooth import Bluetooth
from enums.recording.car import Car
from enums.recording.gps import GPS
from model.response_model import ResponseModel

class ActionCurrentCar(Action):

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_current_car"

    
    @staticmethod
    def run(dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], **kwargs):

        metadata = tracker.latest_message.get("metadata")

        try:
            current_car = metadata['car_selection_metadata']['car_name'];
        except KeyError:
            current_car = None

        if current_car:
            rep = f"Your current car is {current_car}"
        else: rep = "You have not selected a car"

        response = ResponseModel(
            query=tracker.latest_message.get("text"),
            reply=rep,
            action=ActionModel(
                next_action=NextAction.STANDBY.value
            ),
            data={"intent":tracker.latest_message['intent'].get('name')}
        )
        dispatcher.utter_message(json_message={
            "query": response.query,
            "reply": response.reply,
            "action": response.action.as_dict(),
            "data": response.data
        })
        return []
