from .models import Price


class Bill:
    def __init__(self, call_start, call_end):
        self.call_start = call_start
        self.call_end = call_end

    def get_price(self):
        timestamp_start = self.call_start.timestamp
        timestamp_end = self.call_end.timestamp
        hour_start = timestamp_start.hour
        hour_end = timestamp_end.hour
        minute_start = timestamp_start.minute
        minute_end = timestamp_end.minute

        hours = [x for x in range(0, 24)]
        for i in range(0, 24):
            if i < 22 and i >= 6:
                hours[i] = 1
            else:
                hours[i] = 0

        duration_seconds = (timestamp_end - timestamp_start).total_seconds()
        duration_hours = (duration_seconds/60)/60

        standard = Price.objects.filter(tarrif_type='standard').last()
        call_charge_standard = float(standard.call_charge)
        standing_charge_standard = float(standard.standing_charge)
        
        reduced = Price.objects.filter(tarrif_type='reduced').last()
        call_charge_reduced = float(reduced.call_charge)
        standing_charge_reduced = float(reduced.standing_charge)

        if timestamp_end.date() > timestamp_start.date():    
            standard_minutes = (sum(hours[hour_start:] + hours[:hour_end]))*60
            reduced_minutes = (duration_hours - standard_minutes/60)*60
            
            if 6 <= hour_start < 22 and 6 <= hour_end < 22:
                price_standard = call_charge_standard * (standard_minutes - minute_start + minute_end)
                price_reduced = call_charge_reduced * reduced_minutes + standing_charge_reduced

            elif (hour_start >= 22 or hour_start < 6) and (hour_end >= 22 or hour_end < 6):
                price_standard = call_charge_standard * (standard_minutes)
                price_reduced = call_charge_reduced * reduced_minutes + standing_charge_reduced

            elif 6 <= hour_start < 22 and (hour_end >= 22 or hour_end < 6):
                price_standard = call_charge_standard * (standard_minutes - minute_start)
                price_reduced = call_charge_reduced * (reduced_minutes + minute_start) + standing_charge_reduced

            elif 6 <= hour_end < 22 and (hour_start >= 22 or hour_start < 6):
                price_standard = call_charge_standard * (standard_minutes  + minute_end)
                price_reduced = call_charge_reduced * (reduced_minutes - minute_end) + standing_charge_reduced

            total_price = price_standard + price_reduced
            return round(total_price, 2)
        else:
            standard_minutes = (sum(hours[hour_start:hour_end]))*60
            reduced_minutes = (duration_hours - standard_minutes/60)*60

            if 6 <= hour_start < 22 and 6 <= hour_end < 22:
                price_standard = call_charge_standard * (standard_minutes - minute_start + minute_end)
                price_reduced = call_charge_reduced * reduced_minutes + standing_charge_reduced

            elif (hour_start >= 22 or hour_start < 6) and (hour_end >= 22 or hour_end < 6):
                price_standard = call_charge_standard * (standard_minutes)
                price_reduced = call_charge_reduced * reduced_minutes + standing_charge_reduced

            elif 6 <= hour_start < 22 and (hour_end >= 22 or hour_end < 6):
                price_standard = call_charge_standard * (standard_minutes - minute_start)
                price_reduced = call_charge_reduced * (reduced_minutes + minute_start) + standing_charge_reduced

            elif 6 <= hour_end < 22 and (hour_start >= 22 or hour_start < 6):
                price_standard = call_charge_standard * (standard_minutes  + minute_end)
                price_reduced = call_charge_reduced * (reduced_minutes - minute_end) + standing_charge_reduced

            total_price = price_standard + price_reduced

            return round(total_price, 2)