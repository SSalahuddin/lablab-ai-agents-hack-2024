import rasterio
from matplotlib import pyplot as plt
import numpy as np

# Path to the downloaded GeoTIFF file
image_path = './downloaded_images/sentinel2_sf.tif'

# Open the image with rasterio
with rasterio.open(image_path) as src:
    # Read the image bands (B4: red, B3: green, B2: blue)
    band_red = src.read(1)   # Band 4 (red)
    band_green = src.read(2) # Band 3 (green)
    band_blue = src.read(3)  # Band 2 (blue)

    # Stack the bands to create an RGB image
    rgb_image = np.dstack((band_red, band_green, band_blue))

    # Normalize the pixel values to 0-1 for display purposes (since Sentinel-2 values range from 0 to 10,000+)
    rgb_image = rgb_image.astype(np.float32)
    rgb_image = (rgb_image - rgb_image.min()) / (rgb_image.max() - rgb_image.min())

    # Plot the image using matplotlib
    plt.figure(figsize=(10, 10))
    plt.imshow(rgb_image)
    plt.title("Sentinel-2 RGB Image (B4: Red, B3: Green, B2: Blue)")
    plt.show()