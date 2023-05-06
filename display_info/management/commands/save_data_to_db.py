import requests
import os

import requests
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv, find_dotenv

from display_info.models import EqDataDbModel, IntensityDbModel, AqiDataDbModel


class Command(BaseCommand):
    help = "Save data from api to the database"

    def handle(self, *args, **options):
        EqDataDbModel.objects.all().delete()
        IntensityDbModel.objects.all().delete()
        AqiDataDbModel.objects.all().delete()

        load_dotenv(find_dotenv())
        EPA_api_key = os.environ['EPA_api_key']
        CWB_api_key = os.environ['CWB_api_key']
        r_aqi = requests.get(
            f'https://data.epa.gov.tw/api/v2/aqx_p_432?language=zh&offset=23&limit=100&api_key={EPA_api_key}')

        r_eq = requests.get(
            f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization={CWB_api_key}&limit=1&format=JSON&timeFrom=2023-05-01T00%3A00%3A00')

        list_of_dicts_aqi = r_aqi.json()
        list_of_dicts_eq = r_eq.json()

        for aqi_info in list_of_dicts_aqi['records']:
            aqi_in_each_site = aqi_info['aqi']
            station_lat = aqi_info['latitude']
            station_lon = aqi_info['longitude']
            publish_time=aqi_info['publishtime']
            aqi_data = AqiDataDbModel(
                station_lat=station_lat,
                station_lon=station_lon,
                aqi_value=aqi_in_each_site,
                aqi_time=publish_time,
            )
            aqi_data.save()

        for eq_info in list_of_dicts_eq['records']['Earthquake']:
            eq_time = eq_info['EarthquakeInfo']['OriginTime']
            epi_lat = eq_info['EarthquakeInfo']['Epicenter']['EpicenterLatitude']
            epi_lon = eq_info['EarthquakeInfo']['Epicenter']['EpicenterLongitude']
            eq_magnitude = eq_info['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue']
            eq_model : EqDataDbModel = EqDataDbModel(
                epi_lat=epi_lat,
                epi_lon=epi_lon,
                eq_magnitude=eq_magnitude,
                eq_time=eq_time,
            )
            eq_model.save()
            intensity = eq_info['Intensity']['ShakingArea']
            for info in intensity:
                for eq_station_info in info['EqStation']:
                    shaking_area_lat = eq_station_info['StationLatitude']
                    shaking_area_lon = eq_station_info['StationLongitude']
                    seismic_intensity = eq_station_info['SeismicIntensity']
                    intensity_model = IntensityDbModel(
                        seismic_intensity=seismic_intensity,
                        shaking_area_lat=shaking_area_lat,
                        shaking_area_lon=shaking_area_lon,
                        id_earthquake=eq_model,
                    )
                    intensity_model.save()
