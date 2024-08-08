import geopandas as gpd
from keplergl import KeplerGl

from config import Config


class Map:
    config = Config()

    # TODO: Fix the map
    @staticmethod
    def get_kepler_map(gdf: gpd.GeoDataFrame, name: str, hover_cols: tuple = tuple("Borough"),
                       config_lat: int = config.LDN_CENTRE_LAT, config_lng: int = config.LDN_CENTRE_LNG,
                       zoom: float | None = None) -> KeplerGl:
        """
        Creates a map of geometries from a gpd.GeoDataFrame object
        :param gdf: a gpd.GeoDataFrame object storing the geometries that you need to map
        :param name: chosen name for the map
        :param hover_cols: names of columns in the df that appear when you hover over a point on the map
        :param config_lat: a latitude value that is used for the centre the map
        :param config_lng: a longitude value that is used for the centre of the map
        :param zoom: integer value storing the zoom
        :return: a keplergl.KeplerGl object that shows a map of the geometries from the gpd.GeoDataFrame object
        """
        kepler_map = KeplerGl()
        kepler_map.add_data(data=gdf, name=name)

        map_config = {
            "version": "v1", "config": {
                "mapState": {
                    "latitude": config_lat,
                    "longitude": config_lng,
                    "zoom": zoom
                },
                "visState": {
                    "layers": [{
                        "type": "point",
                        "config": {
                            "dataID": name,
                        }
                    }],
                    "filters": [{
                        "dataID": name,
                        "name": name
                    }],
                    "interactionConfig": {
                        "tooltip": {
                            "enabled": True,
                            "fieldsToShow": {
                                name: hover_cols
                            }
                        }
                    }

                }
            }
        }

        kepler_map.config = map_config
        return kepler_map
