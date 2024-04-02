from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .StockCalculator import StockCalculator

class ExtractStockPrice(Action):

    def name(self) -> Text:
        return "action_extract_stock_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_entity = next(tracker.get_latest_entity_values('stock'),None)
        
        if stock_entity:
            
            sc = StockCalculator(stock_entity)

            dispatcher.utter_message(text=f"The current stock price for {stock_entity} is {sc.get_stock_price()}")
        else:
            dispatcher.utter_message(text="I didn't get the stock name. What do you wanna do?")
        return []

class ExtractSockRSI(Action):

    def name(self) -> Text:
        return "action_extract_stock_rsi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_entity = next(tracker.get_latest_entity_values('stock'),None)
        
        if stock_entity:
            
            sc = StockCalculator(stock_entity)

            dispatcher.utter_message(text=f"The current RSI for {stock_entity} is {sc.calculate_RSI()}")
        else:
            dispatcher.utter_message(text="I didn't get the stock name. What do you wanna do?")
        return []
    
class ExtractSockMACD(Action):

    def name(self) -> Text:
        return "action_extract_stock_macd"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock_entity = next(tracker.get_latest_entity_values('stock'),None)
        
        if stock_entity:
            
            sc = StockCalculator(stock_entity)

            dispatcher.utter_message(text=f"The current MACD for {stock_entity} is {sc.calculate_MACD()}")
        else:
            dispatcher.utter_message(text="I didn't get the stock name. What do you wanna do?")
        return []
