from .models import Price


class Bill:
    def __init__(self, call_start, call_end):
        self.call_start = call_start
        self.call_end = call_end
    
    def get_call_duration(self):
        timestamp_start, timestamp_end = self._get_timestamps()
        duration = timestamp_end - timestamp_start
        duration_seconds = duration.total_seconds()
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = duration_seconds % 60
        call_duration = f'{int(hours)}:{int(minutes)}:{int(seconds)}'
        return call_duration

    def get_call_price(self):
        std_minutes, rdc_minutes = self._get_tarrif_minutes()
        price_std, price_rdc = self._get_prices(std_minutes, rdc_minutes)
        total_price = price_std + price_rdc
        return round(total_price, 2)

    def _get_timestamps(self):
        timestamp_start = self.call_start.timestamp
        timestamp_end = self.call_end.timestamp
        return timestamp_start, timestamp_end

    def _get_timestamp_attributes(self):
        timestamp_start, timestamp_end = self._get_timestamps()
        attributes = {
            "hour_start": timestamp_start.hour,
            "hour_end": timestamp_end.hour,
            "minute_start": timestamp_start.minute,
            "minute_end": timestamp_end.minute,
            "date_start": timestamp_start.date(),
            "date_end": timestamp_end.date(),
        }
        return attributes

    def _get_hours_mask(self):
        hours = [x for x in range(0, 24)]
        for i in range(0, 24):
            if i < 22 and i >= 6:
                hours[i] = 1
            else:
                hours[i] = 0
        return hours

    def _get_tarrif_hours(self, date_start, date_end):
        hours = self._get_hours_mask()
        timestamp_attributes = self._get_timestamp_attributes()
        hour_start = timestamp_attributes["hour_start"]
        hour_end = timestamp_attributes["hour_end"]
        if date_end > date_start:
            standard_hours = sum(hours[hour_start:] + hours[:hour_end])
        else:
            standard_hours = sum(hours[hour_start:hour_end])

        timestamp_start, timestamp_end = self._get_timestamps()
        duration_seconds = (timestamp_end - timestamp_start).total_seconds()
        duration_hours = (duration_seconds/60)/60
        reduced_hours = (duration_hours - standard_hours)
        return standard_hours, reduced_hours

    def _get_tarrif_minutes(self):
        timestamp_attributes = self._get_timestamp_attributes()
        date_start = timestamp_attributes["date_start"]
        date_end = timestamp_attributes["date_end"]
        standard_hours, reduced_hours = self._get_tarrif_hours(
            date_start,
            date_end
        )
        standard_minutes = standard_hours*60
        reduced_minutes = reduced_hours*60
        return standard_minutes, reduced_minutes

    def _get_charges(self, tarrif_type):
        if tarrif_type == "standard":
            standard = Price.objects.filter(tarrif_type='standard').last()
            call = float(standard.call_charge)
            standing = float(standard.standing_charge)
        elif tarrif_type == "reduced":
            reduced = Price.objects.filter(tarrif_type='reduced').last()
            call = float(reduced.call_charge)
            standing = float(reduced.standing_charge)
        return call, standing

    def _get_prices(self, standard_minutes, reduced_minutes):
        timestamp_attributes = self._get_timestamp_attributes()
        minute_start = timestamp_attributes["minute_start"]
        minute_end = timestamp_attributes["minute_end"]

        hour_start = timestamp_attributes["hour_start"]
        hour_end = timestamp_attributes["hour_end"]

        call_standard, standing_standard = self._get_charges("standard")
        call_reduced, standing_reduced = self._get_charges("reduced")

        if 6 <= hour_start < 22 and 6 <= hour_end < 22:
            price_standard = call_standard * (
                standard_minutes - minute_start + minute_end
            )
            price_reduced = call_reduced * reduced_minutes + standing_reduced

        elif (hour_start >= 22 or hour_start < 6) and (hour_end >= 22 or hour_end < 6):
            price_standard = call_standard * standard_minutes
            price_reduced = call_reduced * reduced_minutes + standing_reduced

        elif 6 <= hour_start < 22 and (hour_end >= 22 or hour_end < 6):
            price_standard = call_standard * (standard_minutes - minute_start)
            price_reduced = call_reduced * (
                reduced_minutes + minute_start
            ) + standing_reduced

        elif 6 <= hour_end < 22 and (hour_start >= 22 or hour_start < 6):
            price_standard = call_standard * (standard_minutes + minute_end)
            price_reduced = call_reduced * (
                reduced_minutes - minute_end
            ) + standing_reduced

        return price_standard, price_reduced
