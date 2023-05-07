import dataclasses
from typing import List

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
import folium
from .models import AqiDataDbModel, EqDataDbModel, IntensityDbModel


# Create your views here.
@dataclasses.dataclass
class AqiDataUi:
    station_lon: float
    station_lat: float
    aqi_value: int


@dataclasses.dataclass
class EqDataUi:
    epi_lat: float
    epi_lon: float
    eq_time: str


@dataclasses.dataclass
class IntensityDataUi:
    seismic_intensity: str
    shaking_area_lat: float
    shaking_area_lon: float


def home_page(request: HttpRequest):
    aqi_model_list: List[AqiDataDbModel] = [model for model in AqiDataDbModel.objects.all()]
    aqi_data_list: List[AqiDataUi] = []
    for model in aqi_model_list:
        aqi_data_list.append(
            AqiDataUi(
                station_lat=model.station_lat,
                station_lon=model.station_lon,
                aqi_value=model.aqi_value,
            ))

    fmap = folium.Map(location=[23.768001, 120.927373], zoom_start=7, world_copy_jump=True)
    feature_gp_aqi = folium.FeatureGroup(name='aqi')

    for aqi_data in aqi_data_list:
        if aqi_data.aqi_value:
            index = int(aqi_data.aqi_value)
            color = ''
            if index <= 50:
                color = 'green'
            elif 51 <= index <= 100:
                color = 'yellow'
            elif 101 <= index <= 150:
                color = 'orange'
            elif 151 <= index <= 200:
                color = 'red'
            elif 201 <= index <= 300:
                color = 'purple'
            elif 301 <= index <= 500:
                color = 'brown'
            folium.Circle(location=(aqi_data.station_lat, aqi_data.station_lon),
                          color=color,
                          radius=2000,
                          popup=f'{aqi_data.aqi_value}',
                          fill=True,
                          fill_opacity=0.5
                          ).add_to(feature_gp_aqi)

        feature_gp_aqi.add_to(fmap)

    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")
    eq_model_list: List[EqDataDbModel] = [model for model in
                                          EqDataDbModel.objects.filter(eq_time__istartswith=formatted_date)]  # condition
    eq_data_list: List[EqDataUi] = []
    intensity_model_list: List[IntensityDbModel] = []
    intensity_data_list: List[IntensityDataUi] = []
    for model in eq_model_list:
        eq_data_list.append(
            EqDataUi(
                epi_lat=model.epi_lat,
                epi_lon=model.epi_lon,
                eq_time=model.eq_time
            )
        )
        if model.intensitydbmodel_set.all():
            intensity_model_list.append(
                model.intensitydbmodel_set.all()
            )

    if len(intensity_model_list) != 0:
        for model in intensity_model_list[0]:
            if model.seismic_intensity:
                intensity_data_list.append(
                    IntensityDataUi(
                        seismic_intensity=model.seismic_intensity,
                        shaking_area_lat=model.shaking_area_lat,
                        shaking_area_lon=model.shaking_area_lon,
                    )
                )

    feature_gp_eq = folium.FeatureGroup(name='earthquake')

    for data in eq_data_list:
        folium.Marker(location=(data.epi_lat, data.epi_lon),
                      icon=folium.Icon(color="red", icon='glyphicon-star')).add_to(feature_gp_eq)

    for data in intensity_data_list:
        if data.seismic_intensity:
            icon = folium.DivIcon(html=f'{data.seismic_intensity}')
            folium.Marker(location=(data.shaking_area_lat, data.shaking_area_lon), icon=icon).add_to(feature_gp_eq)

    feature_gp_eq.add_to(fmap)
    folium.LayerControl().add_to(fmap)

    context = {
        'map': fmap._repr_html_()
    }

    return render(request, 'display_info/index.html', context)
