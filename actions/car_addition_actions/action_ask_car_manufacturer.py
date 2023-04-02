from typing import Any, Text, Dict, List
from enums.custom_event_type import CustomEventType
from enums.navigation.navigation_screens import NavigationScreens

from model.action_model import ActionModel
from model.custom_event_model import CustomEventModel
from model.next_action import NextAction
from enums.recording.recording_requirements import RecordingRequirements

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, ActiveLoop, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from enums.recording.bluetooth import Bluetooth
from enums.recording.car import Car
from enums.recording.gps import GPS
from model.response_model import ResponseModel

class ActionAskCarManufacturer(Action):

    @staticmethod
    def name(**kwargs) -> Text:
        return "action_ask_car_manufacturer"

    
    def run(self,dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:


        rep = "Select your car's manufacturer."

        response = ResponseModel(
            query=tracker.latest_message.get("text"),
            reply=rep,
            action=ActionModel(
                next_action=NextAction.RECOGNITION.value
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
