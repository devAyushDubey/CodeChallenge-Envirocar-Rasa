from typing import Text, Any, Dict
from enums.custom_event_type import CustomEventType
from model.next_action import NextAction
from enums.car_addition.car_addition import CarAddition

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from model.custom_event_model import CustomEventModel

from utils.car_utils.CarUtils import CarUtils
from utils.car_utils.ManufacIdMapping import manufacturer_id_mapping
from model.response_model import ResponseModel
from model.action_model import ActionModel
from model.next_action import NextAction


class ValidateCarAdditionForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_car_addition_form"

    def validate_car_manufacturer(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:


        print(f"slot_value: {slot_value}")

        manufacturer = tracker.get_slot("car_manufacturer")

        print("Printing `ValidateCarAdditionForm` slots: \n",
              "`car_manufacturer`", manufacturer)

        rep=""

        if(manufacturer):
            rep = f"Are you sure you want to go with {manufacturer}?"
        else:
            rep = f"Sorry that was not found in the list, check the dropdown and try again."

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

        return {}
    
    def validate_car_verification(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:


        print(f"slot_value: {slot_value}")

        stance = tracker.get_slot("car_verification")
        manufacturer = tracker.get_slot("car_manufacturer")

        print("Printing `ValidateCarAdditionForm` slots: \n",
              "`car_verifiaction`", stance)

        rep=""

        if(stance):
            rep = f"Okay selecting {manufacturer}."
        else:
            rep = f"Sure, let's try again select your car's manufacturer?"

        response = ResponseModel(
            query=tracker.latest_message.get("text"),
            reply=rep,
            action=ActionModel(
                custom_event=CustomEventModel(
                type=CustomEventType.CarAddition.value,
                name=CarAddition.SELECT.value
            ).as_dict(),
                next_action=NextAction.STANDBY.value
            ),
            data={"intent":tracker.latest_message['intent'].get('name'),"car_manufacturer_id":manufacturer_id_mapping[manufacturer],"car_manufacturer_name":manufacturer}
        )
        dispatcher.utter_message(json_message={
            "query": response.query,
            "reply": response.reply,
            "action": response.action.as_dict(),
            "data": response.data
        })

        return {"car_manufacturer":None,"car_verification":None,"requested_slot":None}
