import os
import pydicom
from PIL import Image
import numpy as np

def scale_to_8bit(image_array):
    """Scale image array to 8-bit."""
    image_array = image_array - np.min(image_array)
    if np.max(image_array) != 0:
        image_array = image_array / np.max(image_array)
    return (image_array * 255).astype(np.uint8)

def scale_to_16bit(image_array):
    """Scale image array to 16-bit."""
    image_array = image_array - np.min(image_array)
    if np.max(image_array) != 0:
        image_array = image_array / np.max(image_array)
    return (image_array * 65535).astype(np.uint16)

def save_image(image_array, output_path, format):
    """Save the image in the specified format."""
    image = Image.fromarray(image_array)
    image.save(output_path, format)

def convert_dicom_to_format(dicom_folder, output_folder, format):
    """Convert DICOM files to specified format, optimizing for bit depth."""
    for filename in os.listdir(dicom_folder):
        if filename.lower().endswith(('.dicom', '.dcm')):
            # Read DICOM file
            dicom_path = os.path.join(dicom_folder, filename)
            dicom_image = pydicom.dcmread(dicom_path)
            image_array = dicom_image.pixel_array

            # Determine the optimal bit depth for conversion
            if format.upper() == 'JPEG':
                # JPEG uses 8-bit channels
                converted_image = scale_to_8bit(image_array)
            elif format.upper() in ['PNG', 'TIFF']:
                # PNG and TIFF can support 16-bit channels
                # Check if the DICOM image bit depth is greater than 8
                if dicom_image.BitsStored > 8:
                    converted_image = scale_to_16bit(image_array)
                else:
                    converted_image = scale_to_8bit(image_array)
            else:
                raise ValueError("Unsupported format. Please use JPEG, PNG, or TIFF.")

            # Define the output path with the new extension
            new_extension = '.' + format.lower()
            output_path = os.path.join(output_folder, filename.lower().replace('.dcm', new_extension).replace('.dicom', new_extension))
            
            # Save the image in the specified format
            save_image(converted_image, output_path, format.upper())

def convert_dicom_to_jpeg(dicom_folder, output_folder):
    """Convert DICOM files to JPEG format."""
    convert_dicom_to_format(dicom_folder, output_folder, 'JPEG')

def convert_dicom_to_png(dicom_folder, output_folder):
    """Convert DICOM files to PNG format."""
    convert_dicom_to_format(dicom_folder, output_folder, 'PNG')

def convert_dicom_to_tiff(dicom_folder, output_folder):
    """Convert DICOM files to TIFF format."""
    convert_dicom_to_format(dicom_folder, output_folder, 'TIFF')
