"""
Créé le 13/08/2021

@Auteur : Constantin van Ypersele

"""

class Hour :
    
    def __init__(self, date, sunshine, wind, rain, temperature):
        """
        @date : Datetime object
        @sunshine : int between 0 and 6
        @wind : int
        @rain : float ([mm])
        @temperature : float (°C)
        
        """
        self.date = date
        self.sunshine = sunshine
        self.wind = wind
        self.rain = rain
        self.temperature = temperature
    
    def get_date(self):
        return self.date
    
    def get_sunshine(self):
        return self.sunshine
    
    def get_wind(self):
        return self.wind
    
    def get_rain(self):
        return self.rain
    
    def get_temperature(self):
        return self.temperature
    
    def set_date(self, new_date):
        self.date = new_date
        
    def set_sunshine(self, new_sunshine):
        self.sunshine = new_sunshine
    
    def set_wind(self, new_wind):
        self.wind = new_wind
    
    def set_rain(self, new_rain):
        self.rain = new_rain
        
    def set_temperature(self, new_temperature):
        self.temperature = new_temperature
        
    def meteo_comparator(self, other_hour):
        """
        @other_hour : object of type Hour
        
        @return : -1 if self < other_hour, 1 if other_hour < self

        """
        if self.sunshine < other_hour.get_sunshine():
            return 1
        
        first_cond =  (self.sunshine == other_hour.get_sunshine())
        
        if (first_cond) and (self.rain > other_hour.get_rain()):
            return 1
            
        second_cond = first_cond and (self.rain == other_hour.get_rain())
        if (second_cond) and (self.wind > other_hour.get_wind()):
            return 1
        
        third_cond = second_cond and (self.wind == other_hour.get_wind())
        if third_cond and self.date > other_hour.get_date():
            return 1
        
        return -1
    
    def date_comparator(self, other_hour):
        if self.date < other_hour.get_date():
            return -1
        
        return 1
    
    def merge(list_a, list_b, comparator):
        result = []
        
        index_a = 0
        index_b = 0
        
        while index_a < len(list_a) and index_b < len(list_b) :
            
            if comparator(list_a[index_a], list_b[index_b]) == -1:
                result.append(list_a[index_a])
                index_a += 1
                
            else:
                result.append(list_b[index_b])
                index_b += 1
        
        while index_a < len(list_a) :
            result.append(list_a[index_a])
            index_a += 1
        
        while index_b < len(list_b) :
            result.append(list_b[index_b])
            index_b += 1
        
        return result
    
    def sort_list(hours, comparator):
        """
        @hours : list of Hour to be sorted
        @return : new sorted list
        
        """
        size = len(hours)   
        if size == 1 :
            return hours
        
        first = Hour.sort_list(hours[:size//2], comparator)
        second = Hour.sort_list(hours[size//2:], comparator)

        return Hour.merge(first, second, comparator)
    
    def __str__(self):
        #message = "On {0} the sunshine will be {1}/6, there will be a wind of {2}".format(self.date, self.sunshine, self.wind)
        #message += "km/h, {0} mm of rain and a temperature of {1} °C.".format(self.rain, self.temperature)
        
        message = "{0},{1},{2},{3},{4}".format(self.date, self.sunshine, self.wind, self.rain, self.temperature)
        return message

"""
from datetime import datetime
a = datetime(1920, 8, 15, 13)
b = datetime(1920, 8, 15, 11)
l = [Hour("12/5/2021", 5, 15, 0.2, 25.0), Hour("17/03/1599", 0, 0, 0, 3000), Hour("12/90/6600", 10, 10000, 2002, 5),
     Hour(a, 15, 20, 1, 18), Hour(b, 15, 20, 1, -158), Hour(a, 3, 10, 10, 7), Hour(a, 3, 8, 177, 0)]

for i in Hour.sort_list(l, Hour.meteo_comparator):
   print(i)
"""