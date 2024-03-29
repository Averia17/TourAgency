import os.path

from tour_agency.settings import BASE_DIR

TOUR_TYPES = (
    ("LAND", "Land Tour"),
    ("ONE_DESTINATION", "One Destination Journey"),
    ("RIVER", "River Cruises"),
    ("SMALL_SHIP", "Small Ship Cruises"),
    ("FAMILY", "Family Journeys"),
)
MEALS = (
    ("BREAKFAST", "Breakfast"),
    ("BRUNCH", "Brunch"),
    ("LUNCH", "Lunch"),
    ("SUPPER", "Supper"),
    ("DINNER", "Dinner"),
)

CONVENIENCES_TYPES = (
    ("HOTEL", "Hotel"),
    ("ROOM", "Room"),
)

ORDER_STATUSES = (
    ("SUCCESS", "Successfully ordered"),
    ("BOOKED", "Booked"),
    ("FAULT", "Fault"),
    ("CANCELED", "Canceled"),
)

CHECK_IN_TIME = "13:00:00"

NUMBER_BOOKED_DAYS = 3

ORDER_SUBJECT = "Order created"
ORDER_MESSAGE = "Thank you for ordering tour {tour}"

ORDER_FILE_NAME = "OrderRequest.pdf"
ORDER_FILE_PATH = os.path.join(BASE_DIR, ORDER_FILE_NAME)

HASH_SALT = "token"
