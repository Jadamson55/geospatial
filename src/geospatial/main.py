
from ftplib import FTP
import io
from datetime import date, datetime
from google.cloud import bigquery
from google.cloud import storage
from google.cloud import secretmanager

# Import necessary libraries
import geopandas as gpd
from shapely.geometry import Point, Polygon
from google.cloud import storage

# Function to perform spatial query and generate a new shapefile
def perform_spatial_query(input_geojson_path, boundary_coords, output_shapefile_path):
    """ 
    Read the input GeoJSON file into a GeoDataFrame
    Create a Polygon object representing the boundary
    Perform the spatial query to check if points are within the boundary
    Save the result as a new shapefile
    """
    gdf = gpd.read_file(input_geojson_path)
    boundary_polygon = Polygon(boundary_coords)
    points_within_boundary = gdf[gdf.geometry.within(boundary_polygon)]
    points_within_boundary.to_file(output_shapefile_path, driver='ESRI Shapefile')

# Function to upload the generated shapefile to Google Cloud Storage
def upload_to_gcs(bucket_name, local_file_path, gcs_file_path):
    """
    Initialize a Google Cloud Storage client
    Get the specified bucket
    Create a blob object representing the file in GCS
    Upload the local file to GCS
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(gcs_file_path)
    blob.upload_from_filename(local_file_path)
    print(f"File uploaded to Google Cloud Storage: gs://{bucket_name}/{gcs_file_path}")


def main(request):
    """
    This function is triggered by an HTTP request.
    """

    # Specify the input GeoJSON file, boundary coordinates, and output shapefile path
    # TODO: these should be passed in as parameters to the Cloud Function
    input_geojson_path = 'path/to/input.geojson' # TODO: collect this from the FTP server
    output_shapefile_path = 'path/to/output.shp' # TODO: store this in a temporary directory
    boundary_coords = [
        (-74.0, 40.0),  # (x1, y1)
        (-74.0, 41.0),  # (x2, y2)
        (-73.0, 41.0),  # (x3, y3)
        (-73.0, 40.0),  # (x4, y4)
    ]

    # Specify Google Cloud Storage details
    bucket_name = 'super-cool-bucket'
    gcs_file_path = 'path/in/gcs/output.shp'

    # Perform spatial query and generate a new shapefile
    # Upload the generated shapefile to Google Cloud Storage
    perform_spatial_query(input_geojson_path, boundary_coords, output_shapefile_path)
    upload_to_gcs(bucket_name, output_shapefile_path, gcs_file_path)

    print('Success! Cloud Function is complete.')
    return ('OK')


if __name__ == '__main__':
    main('request')
