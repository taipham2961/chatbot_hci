from typing import Any, Text, Dict, List

import arrow
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

ALLOWED_START = ["côn đảo", "phù cát", "cà mau", "cần thơ", "buôn ma thuột", "đà nẵng",
                 "rạch giá", "phú quốc", "chu lai", "phú bài", "thọ xuân", "vân đồn",
                 "điện biên phủ", "pleiku", "cát bi", "nội bài", "tân sơn nhất",
                 "cam ranh", "liên khương", "vinh", "tuy hòa", "đồng hới"]
ALLOWED_ARRIVE = ["Côn Đảo", "Phù Cát", "Cà Mau", "Cần Thơ", "Buôn Ma Thuột", "Đà Nẵng",
                  "Rạch Giá", "Phú Quốc", "Chu Lai", "Phú Bài", "Thọ Xuân", "Vân Đồn",
                  "Điện Biên Phủ", "Pleiku", "Cát Bi", "Nội Bài", "Tân Sơn Nhất",
                  "Cam Ranh", "Liên Khương", "Vinh", "Tuy Hòa", "Đồng Hới"]

city_db = {
    'Sydney': 'Australia/Sydney',
    'Paris': 'Europe/Paris',
    'London': 'Europe/Dublin',
    'Tokyo': 'Asia/Tokyo',
    'Amsterdam': 'Europe/Amsterdam',
    'Berlin': 'Europe/Berlin',
    'New York': 'America/New_York',
    'Hồ Chí Minh': 'Asia/Ho_Chi_Minh'
}


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.now('Asia/Ho_Chi_Minh')

        if not current_place:
            msg = f"Bây giờ là {utc.format('HH:mm')} tại Hồ Chí Minh. Bạn có thể nhập nơi khác."
            dispatcher.utter_message(text=msg)
            return []

        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"Tôi không nhận diện {current_place}. Bạn nhập đúng chứ?"
            dispatcher.utter_message(text=msg)
            return []

        msg = f"Bây giờ là {utc.to(city_db[current_place]).format('HH:mm')} tại {current_place} bây giờ."
        dispatcher.utter_message(text=msg)

        return []


class ValidateSimpleTicketPlaneForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_ticket_plane_form"

    def validate_start(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `start` value."""

        if slot_value.lower() not in ALLOWED_START:
            dispatcher.utter_message(
                text=f"Tôi không thể đặt vé máy bay từ địa điểm đó.")
            return {"start": None}
        dispatcher.utter_message(
            text=f"OK! Bạn sẽ bắt đầu bay từ {slot_value}.")
        return {"start": slot_value}

    def validate_arrive(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `arrive` value."""

        if slot_value not in ALLOWED_ARRIVE:
            dispatcher.utter_message(
                text=f"Tôi không nhận dạng được bạn sẽ bay đến đâu. Tôi chỉ phục vụ {'/'.join(ALLOWED_ARRIVE)}.")
            return {"arrive": None}
        dispatcher.utter_message(
            text=f"OK! Bạn sẽ bay đến {slot_value}.")
        return {"arrive": slot_value}
