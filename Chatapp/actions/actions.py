# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

#
# def get_user_balance(pin_number):
#     url = "https://ibank.crusaderpensions.com/wildfly/pensionserver-web/rest/partnerservice/BalanceByUserDetails"
#     headers = {"Content-Type": "application/json"}
#     data = {"pin": pin_number}
#
#     try:
#         response = requests.post(url, json=data, headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
#
#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             # Parse the JSON response and return it
#             user_balance_data = response.json()
#             return user_balance_data['data']
#     except requests.exceptions.RequestException as e:
#         # Handle exceptions (e.g., connection error, timeout)
#         print(f"An error occurred: {e}")
#         return None
#

#
# def update_user_nok(pin_number):
#     url = "https://ibank.crusaderpensions.com/wildfly/pensionserver-web/rest/partnerservice/updateNok"
#     headers = {"Content-Type": "application/json"}
#     data = {"pin": pin_number}
#
#     try:
#         response = requests.post(url, json=data, headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
#
#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             # Parse the JSON response and return it
#             user_balance_data = response.json()
#             return user_balance_data['data']
#     except requests.exceptions.RequestException as e:
#         # Handle exceptions (e.g., connection error, timeout)
#         print(f"An error occurred: {e}")
#         return None
#
#
# def update_user_employer(pin_number):
#     url = "https://ibank.crusaderpensions.com/wildfly/pensionserver-web/rest/partnerservice/updateEmployer"
#     headers = {"Content-Type": "application/json"}
#     data = {"pin": pin_number}
#
#     try:
#         response = requests.post(url, json=data, headers=headers)
#         response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
#
#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             # Parse the JSON response and return it
#             user_balance_data = response.json()
#             return user_balance_data['data']
#     except requests.exceptions.RequestException as e:
#         # Handle exceptions (e.g., connection error, timeout)
#         print(f"An error occurred: {e}")
#         return None


#
#

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType


def get_user_pin(phone_number):
    url = "https://ibank.crusaderpensions.com/wildfly/pensionserver-web/rest/partnerservice/GetUserPin"
    headers = {"Content-Type": "application/json"}
    data = {"phoneNo": phone_number}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response and return it
            user_pin_data = response.json()
            return user_pin_data['data']
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., connection error, timeout)
        print(f"An error occurred: {e}")
        return None


class ActionGetPin(Action):

    def name(self) -> Text:
        return "action_get_pin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        phone_number = tracker.get_slot("phonenum")
        # phone_number = next(tracker.get_latest_entity_values("phonenum"), None)

        if phone_number:
            pin = get_user_pin(phone_number)

            response = "Your rsa pin is \n{}".format(pin['pin'])
            dispatcher.utter_message(response)
        else:
            response = "Invalid response {}".format(phone_number)
            dispatcher.utter_message(response)
        return []


class ValidatePhoneValue(Action):

    def name(self) -> Text:
        return "validate_phone_value"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []

    def validate_name(
            self,
            slot_value: Any,
            dispatcher: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """validate slot value"""
        if not slot_value:
            return ({"get_phone": None})
        else:
            return ({"get_phone": slot_value})


class ValidateBalanceForm(Action):

    def name(self) -> Text:
        return "validate_balance_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []

    def validate_name(
            self,
            slot_value: Any,
            dispatcher: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """validate slot value"""
        if not slot_value:
            return ({"get_phone": None})
        else:
            return ({"get_phone": slot_value})


class ApiService:
    BASE_URL = "https://ibank.crusaderpensions.com/wildfly/pensionserver-web/rest/partnerservice"
    HEADERS = {"Content-Type": "application/json"}

    def __init__(self):
        pass

    def _make_request(self, endpoint, data):
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = requests.post(url, json=data, headers=self.HEADERS)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json().get('data')
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_user_statement(self, pin_number):

        data = data = {"pin": pin_number}
        return self._make_request("GetStatement", data)

    def update_user_nok(self, pin_number):

        data = {"pin": pin_number}
        return self._make_request("updateNok", data)

    def update_user_employer(self, pin_number):

        data = {"pin": pin_number}
        return self._make_request("updateEmployer", data)

    def get_user_balance(self, pin_number):

        data = {"pin": pin_number}
        return self._make_request("BalanceByUserDetails", data)


class ActionGetRsaBalance(Action):
    def name(self) -> Text:
        return "action_get_rsa_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        pin = tracker.get_slot("pennum")
        surname = tracker.get_slot("surname")
        relationship = tracker.get_slot("relationship")
        employer = tracker.get_slot("employer")
        statedate = tracker.get_slot("statedate")

        api = ApiService()

        try:
            if pin and not surname and not relationship and not statedate and not employer:
                result = api.get_user_balance(pin.lower())
                if result is not None:
                    response = f"Hey, your rsa balance is {result['balance']}"
                else:
                    response = "Sorry, we couldn't retrieve your balance. Please check your PIN."
                dispatcher.utter_message(response)
                return [SlotSet("pennum", None)]
            elif pin and employer and not surname and not relationship and not statedate:
                api.update_user_employer(pin.lower())
                response = f"Hey, your employer change completed successfully"
                dispatcher.utter_message(response)
                return [SlotSet("employer", None)]
            elif pin and surname and relationship and not statedate and not employer:
                api.update_user_nok(pin.lower())
                response = f"Hey, your next of kin change completed successfully"
                dispatcher.utter_message(response)
                return [SlotSet("relationship", None), SlotSet("surname", None)]
            elif pin and statedate and not employer and not surname and not relationship:
                api.get_user_statement(pin.lower())
                response = f"Hey, PDF statement is sent to the Account holder's email"
                dispatcher.utter_message(response)
                return [SlotSet("statedate", None)]
            else:
                response = f"Invalid response: {pin}"
        except Exception as e:
            print(f"An error occurred: {e}")
            response = "An error occurred while processing your request. Please try again later."

        dispatcher.utter_message(response)
        return []
