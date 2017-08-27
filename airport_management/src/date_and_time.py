from datetime import datetime

def get_day_from_datetime(datetime:datetime) -> str:
    return datetime.strftime("%A")