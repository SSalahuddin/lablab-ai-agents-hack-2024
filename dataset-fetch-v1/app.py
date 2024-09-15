import ee

# Initialize the Earth Engine API
ee.Initialize()

def export_sentinel2_image_to_drive(latitude, longitude, start_date, end_date, image_name):
    # Define a point around which to get the image
    point = ee.Geometry.Point([longitude, latitude])

    # Load the Sentinel-2 image collection and filter by date and location
    collection = (ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
                  .filterBounds(point)
                  .filterDate(start_date, end_date)
                  .sort('CLOUD_COVER', True))  # Sort by cloud cover to get the least cloudy image

    # Get the first image in the filtered collection
    image = collection.first()

    # Select relevant bands (e.g., RGB bands: B4, B3, B2)
    selected_bands = image.select(['B4', 'B3', 'B2'])

    # Define the region (smaller bounding box around the point, e.g., 1 km buffer)
    region = point.buffer(1000).bounds()

    # Create an export task to Google Drive
    task = ee.batch.Export.image.toDrive(
        image=selected_bands,
        description=image_name,
        folder='EarthEngineImages',  # Folder name in Google Drive
        fileNamePrefix=image_name,
        region=region.getInfo()['coordinates'],
        scale=30,  # Resolution in meters
        crs='EPSG:4326',  # Coordinate Reference System
        fileFormat='GeoTIFF'
    )

    # Start the export task
    task.start()
    print(f"Export task started to Google Drive for {image_name}.")

# Example usage
latitude = 37.7749   # Latitude for San Francisco
longitude = -122.4194  # Longitude for San Francisco
start_date = '2021-06-01'
end_date = '2021-06-30'
image_name = 'sentinel2_sf'

export_sentinel2_image_to_drive(latitude, longitude, start_date, end_date, image_name)