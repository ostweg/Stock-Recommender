from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ExtractStockEntity(Action):

    def name(self) -> Text:
        return "action_extract_stock_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_entity = next(tracker.get_latest_entity_values('stock'),None)
        
        print(f"****____{stock_entity}_____*********")

        if stock_entity:
            dispatcher.utter_message(text=f"Will retrieve data for '{stock_entity}!")
        else:
            dispatcher.utter_message(text="I didn't get the stock name. What do you wanna do?")
        return []
