from typing import List, Dict

import requests
from requests import HTTPError, ConnectionError
from shapely.geometry import Point

from repositories.base_repository import BaseRepository


class TfLRepository(BaseRepository):

    def __init__(self):
        super().__init__()

    @staticmethod
    def _clean_mode_names(mode_meta_query: requests.Request) -> list:
        """Gets transport modes and filters out bus and coach.
        :return: a list of transport modes
        """
        modes = [mode["modeName"] for mode in mode_meta_query.json() if mode["isScheduledService"]]
        modes.remove("bus")
        modes.remove("coach")
        return modes

    @staticmethod
    def _clean_stops_information_for_line(lines_info: requests.Request, mode: str, line_name: str) -> List[dict]:
        """Gets data for each mode of transport under the tfl
        :param mode: a mode of transport from a list o modes taken from the _modes_names() method
        :param line_name: the name of a line
        :return: a list of dictionaries storing the relevant data for each tfl stop
        """
        line_information = []
        for line_info in lines_info.json():
            stop_information = dict(Name=line_info["commonName"], mode=mode, line=line_name,
                                    geometry=Point(line_info["lon"], line_info["lat"]))
            line_information.append(stop_information)
        return line_information

    def _get_stop_id(self, station_name: str) -> str:
        """
        Returns a stop_id for a chosen station name
        :param station_name: name of the chosen train station
        :return: stop_id
        """
        stop_id_url = f"{self.config.TFL_BASE_URL}/Stoppoint/Search/{station_name}"
        try:
            stop_id_data = self.request_session.get(stop_id_url)
        except ConnectionError:
            raise RuntimeError("There is a connection error. TfL stop ID data cannot be retrieved.")
        try:
            stop_id_data.raise_for_status()
        except HTTPError:
            raise RuntimeError(f"Could not get stop ID data from TFL API. {stop_id_data.status_code} Response")

        stop_id = stop_id_data.json()["matches"][0]["id"]

        return stop_id

    def get_data(self) -> List[dict]:
        """Gets the stoppoints for every mode in a list of modes and returns it in a list of dictionaries
        :return: a list of dictionaries storing data on each stop under the tfl
        """
        try:
            mode_response = self.request_session.get(f"{self.config.TFL_BASE_URL}/Line/Meta/Modes")
        except ConnectionError:
            raise RuntimeError("There is a connection error. TfL mode data cannot be retrieved.")
        try:
            mode_response.raise_for_status()
        except HTTPError:
            raise RuntimeError(f"Could not query TFL API for available modes. {mode_response.status_code} Response.")
        modes = self._clean_mode_names(mode_response)
        stops = []
        for mode in modes:
            try:
                mode_status_response = self.request_session.get(f"{self.config.TFL_BASE_URL}/line/mode/{mode}/status")
            except ConnectionError:
                raise RuntimeError("There is a connection error. TfL mode status response cannot be retrieved.")
            try:
                mode_status_response.raise_for_status()
            except HTTPError:
                raise RuntimeError(f"Could not connect to TFL API for {mode} transport mode. "
                                   f"{mode_status_response.status_code} Response.")
            lines_in_mode = {line["id"]: line["name"]
                             for line in mode_status_response.json() if line["modeName"] == mode}
            for line_id, line_name in lines_in_mode.items():
                try:
                    line_response = self.request_session.get(f"{self.config.TFL_BASE_URL}/line/{line_id.upper()}"
                                                             f"/stoppoints")
                except ConnectionError:
                    raise RuntimeError("There is a connection error. TfL line data cannot be retrieved.")
                try:
                    line_response.raise_for_status()
                except HTTPError:
                    raise RuntimeError(f"Could not get stop point data from TFL API. {line_response.status_code} "
                                       f"Response")
                line_information = self._clean_stops_information_for_line(line_response, mode, line_name)
                stops.extend(line_information)

        return stops

    def get_arrival_data(self, station_name: str) -> List[Dict[str, str | int | Dict[str, str]]]:
        """
        Gets the arrival times for a chosen station
        :param station_name: name of the chosen station
        :return: a dictionary storing the names of stations and their arrival times
        """
        stopID = self._get_stop_id(station_name)
        arrival_data_url = f"{self.config.TFL_BASE_URL}/StopPoint/{stopID}/Arrivals"
        try:
            arrival_data = self.request_session.get(arrival_data_url)
        except ConnectionError:
            raise RuntimeError("There is a connection error. Arrival times cannot be retrieved.")
        try:
            arrival_data.raise_for_status()
        except HTTPError:
            raise RuntimeError(f"Could not get arrival data from TFL API. {arrival_data.status_code} Response")
        return arrival_data.json()

