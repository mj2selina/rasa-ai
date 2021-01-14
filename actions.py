# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
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
class ActionAnswer_Restaurant(Action):
    def name(self) -> Text:
        return "action_answer_restaurant"

    def run(self,
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        add = tracker.get_slot('address')
        r1 = requests.get(url='restapi.amap.com/v3/geocode/geo?key=febe1d93003fb94251e0d43a9b7c24e6&address=' + add + '&city=')
        r1_json = json.loads(r1.text)
        if r1_json['status'] == 1 and len(r1_json['geocodes']) > 0:
            if 'location' in r1_json['geocodes'][0]:
                loc = r1_json['geocodes'][0]['location']
            else:
                dispatcher.utter_message(text='请重复您的当前位置，否则无法为您查询哦~')
                return []
        else:
            dispatcher.utter_message(text='请重复您的当前位置，否则无法为您查询哦~')
            return []
        cuisine = tracker.get_slot('cuisine')
        r2 = requests.get(url='restapi.amap.com/v3/place/around?key=febe1d93003fb94251e0d43a9b7c24e6&location=' + loc + '&keywords=' + cuisine + '&types=050301&offset=20&page=1&extensions=all')
        r2_json = json.loads(r2.text)
        if r2_json['status'] == 1 and 'pois' in r2_json and len(r2_json['pois']) > 0:
            if 'name' in r2_json['pois'][0]:
                restaurant = r2_json['pois'][0]['name']
            else:
                dispatcher.utter_message(text='没有找到合适的美食呢~')
                return []
        else:
            dispatcher.utter_message(text='没有找到合适的美食呢~')
            return []
        dispatcher.utter_message(text="离您最近的{}是{}，请问满足您的需求吗？".format(cuisine,restaurant))
        return [SlotSet('restaurant',restaurant)]
        