import os
from PIL import Image

def CombineImages(targetImagesFolderPath, output_path):
    
    images = sorted([file for file in os.listdir(targetImagesFolderPath) if file.endswith(('.png', '.jpg', '.jpeg'))])

    row_size = int(input("Row Size ( example: 4 ) :"))
    column_size = int(input("Column Size ( example: 4 ) : "))


    total_image_number = row_size * column_size
    if len(images) < total_image_number:
        print("There are not enough images in the folder.")
        return


    combined_width = 0
    combined_height = 0
    images_array = []

    for i in range(total_image_number):
        image_path = os.path.join(targetImagesFolderPath, images[i])
        image = Image.open(image_path)
        images_array.append(image.convert('RGBA'))

        combined_width = max(combined_width, image.width)
        combined_height = max(combined_height, image.height)

    combined_width *= column_size
    combined_height *= row_size


    combined_image = Image.new('RGBA', (combined_width, combined_height))

    for row in range(row_size):
        for column in range(column_size):
            index = row * column_size + column
            image = images_array[index]
            combined_image.paste(image, (column * image.width, row * image.height))

    combined_image.save(output_path)


targetImagesFolderPath = (input("Target Images Folder Path: "))
output_path = 'combined_image.png'

CombineImages(targetImagesFolderPath, output_path)
