# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:48:12 2024

@author: kian0
"""

import contextily as ctx
import matplotlib.pyplot as plt
from shapely.geometry import box
import geopandas as gpd
import pyproj


class LaunchSiteMap:
    def __init__(self, latitude, longitude, extent_x=None, extent_y=None, utm_zone=29, epsg=32629):
        self.latitude = latitude
        self.longitude = longitude
        self.extent_x = extent_x if extent_x else [2000, 2000]
        self.extent_y = extent_y if extent_y else [2000, 2000]
        self.utm_zone = utm_zone
        self.epsg = epsg

        self.proj_utm = pyproj.Proj(proj='utm', zone=self.utm_zone, ellps='WGS84')
        self.origin_x, self.origin_y = self.proj_utm(self.longitude, self.latitude)

        self.bbox = box(
            self.origin_x - self.extent_x[0], self.origin_y - self.extent_y[0],
            self.origin_x + self.extent_x[1], self.origin_y + self.extent_y[1]
        )
        self.gdf = gpd.GeoDataFrame({'geometry': [self.bbox]}, crs=f"EPSG:{self.epsg}")



    def get_map(self, filename="map.png", show=False, add_lines=False):
        fig, ax = plt.subplots(figsize=(10, 10), dpi=224)
        ax.set_xlim([self.origin_x - self.extent_x[0], self.origin_x + self.extent_x[1]])
        ax.set_ylim([self.origin_y - self.extent_y[0], self.origin_y + self.extent_y[1]])

        ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, crs=self.gdf.crs.to_string(), zoom=15)

        if add_lines:
            ax.axhline(y=self.origin_y, color='black', linewidth=0.5, linestyle='-')  # Horizontal line
            ax.axvline(x=self.origin_x, color='black', linewidth=0.5, linestyle='-')  # Vertical line

        if show:
            plt.show()

        ax.axis('off')
        plt.savefig(filename, bbox_inches='tight', pad_inches=0, dpi=224)


    def get_bbox_coordinates(self):
        return self.bbox.bounds


# Example usage
if __name__ == "__main__":
    latitude = 39.39072
    longitude = -8.289618

    custom_map = LaunchSiteMap(latitude, longitude)
    custom_map.get_map(filename="launch_site_map.png", add_lines=True)




##### Old Code #####

# import contextily as ctx
# import matplotlib.pyplot as plt
# from shapely.geometry import box
# import geopandas as gpd
# import pyproj

# # Coordinates of the launch site
# latitude = 39.39072
# longitude = -8.289618

# # Define the extent in meters around the launch site (UTM projection)
# extent_meters_x = [2000, 2000]
# extent_meters_y = [2000, 2000]


# # Convert the latitude and longitude to UTM coordinates
# proj_utm = pyproj.Proj(proj='utm', zone=29, ellps='WGS84')  # Replace with your UTM zone
# origin_x, origin_y = proj_utm(longitude, latitude)

# # Create a bounding box around the launch site
# bbox = box(origin_x - extent_meters_x[0], origin_y - extent_meters_y[0], 
#            origin_x + extent_meters_x[1], origin_y + extent_meters_y[1])

# gdf = gpd.GeoDataFrame({'geometry': [bbox]}, crs="EPSG:32629")  # Replace with correct EPSG code

# # Plot the basemap using contextily
# fig, ax = plt.subplots(figsize=(10, 10), dpi=224)

# # Set the limits of the plot to the bounding box
# ax.set_xlim([origin_x - extent_meters_x[0], origin_x + extent_meters_x[1]])
# ax.set_ylim([origin_y - extent_meters_y[0], origin_y + extent_meters_y[1]])

# # Add the basemap cropped to the bounding box
# ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, crs=gdf.crs.to_string(), zoom=15)

# # Remove axis for a clean image
# ax.axis('off')

# # Save the map as an image
# map_filename = "launch_site_map1.png"
# plt.savefig(map_filename, bbox_inches='tight', pad_inches=0, dpi=224)

# # Optionally, show the map
# #plt.show()

