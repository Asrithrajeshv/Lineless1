"""import uuid

def generate_booking_id():
    Generate a unique booking ID.
    return str(uuid.uuid4())  # Generates a random unique UUID"""

import random

def generate_booking_id():
    # Generate a random 8-digit number as the booking ID
    booking_id = str(random.randint(10000000, 99999999))
    return booking_id