class Entity_weather:
    def __init__(self, province, city, district, sunRise, sunSet, date, apparentTemperature, pressure, cloudCover, dewPoint, humidity,
                 precipProbability, ozone, precipType, precipAccumulation, temperature, summary, uvIndex, windGust,
                 windSpeed, windBearing):
        self.province = province
        self.city = city
        self.district = district
        self.sunRise = sunRise
        self.sunSet = sunSet
        self.date = date
        self.apparentTemperature = apparentTemperature
        self.pressure = pressure
        self.cloudCover = cloudCover
        self.dewPoint = dewPoint
        self.humidity = humidity
        self.precipProbability = precipProbability
        self.ozone = ozone
        self.precipType = precipType
        self.precipAccumulation = precipAccumulation
        self.temperature = temperature
        self.summary = summary
        self.uvIndex = uvIndex
        self.windGust = windGust
        self.windSpeed = windSpeed
        self.windBearing = windBearing

    def print(self):
        print(self.province,
              self.city,
              self.district,
              self.sunRise,
              self.sunSet,
              self.date,
              self.apparentTemperature,
              self.pressure,
              self.cloudCover,
              self.dewPoint,
              self.humidity,
              self.precipProbability,
              self.ozone,
              self.precipType,
              self.precipAccumulation,
              self.temperature,
              self.summary,
              self.uvIndex,
              self.windGust,
              self.windSpeed,
              self.windBearing,
              )
