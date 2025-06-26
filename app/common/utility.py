from datetime import datetime, date

class Utility:
    def convert_datetime_2_date(self, dt: datetime) -> date:
        return dt.date()
