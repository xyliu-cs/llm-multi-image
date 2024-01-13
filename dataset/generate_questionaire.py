import json
from PIL import Image, ImageDraw
import markdown2
import os

# Load the JSON file
file_path = 'question_answer_pairs.json'
images_folder = '../../images'

# Function to create an image grid
def create_image_grid(images, max_images_per_row=3, gap=10):
    # Load images
    loaded_images = [Image.open(os.path.join(images_folder, img)) for img in images]
    
    # Determine grid size
    max_width = max(image.width for image in loaded_images)
    max_height = max(image.height for image in loaded_images)
    num_rows = (len(images) + max_images_per_row - 1) // max_images_per_row

    # Calculate the size of the grid image including gaps
    grid_width = max_width * max_images_per_row + gap * (max_images_per_row - 1)
    grid_height = max_height * num_rows + gap * (num_rows - 1)

    # Create a new image with a black background
    grid_image = Image.new('RGB', (grid_width, grid_height), 'black')
    draw = ImageDraw.Draw(grid_image)

    # Place images in the grid with gaps
    for index, image in enumerate(loaded_images):
        row = index // max_images_per_row
        col = index % max_images_per_row
        x = (max_width + gap) * col
        y = (max_height + gap) * row
        grid_image.paste(image, (x, y))

    return grid_image

# Read the JSON file and parse the data
with open(file_path, 'r') as file:
    data = json.load(file)

# Markdown content
markdown_content = "# Question-Answer Pairs with Images\n\n"

# Process each item in the JSON
for item in data:
    question = item['question']
    images = item['image_required']
    # if (len(images) == 0):
    #     print(item['question_id'])
    
    # Create an image grid for the required images
    grid_image = create_image_grid(images)
    grid_image_path = f"grid_image_{item['question_id']}.png"
    grid_image.save(os.path.join(images_folder, grid_image_path))
    
    # Add to markdown
    markdown_content += f"## Question {item['question_id']}\n"
    markdown_content += f"**Question:** {question}\n\n"
    markdown_content += f"![Image Grid](./{grid_image_path})\n\n"


# Save the markdown content to a file
markdown_file_path = './questionaire.md'
with open(markdown_file_path, 'w') as md_file:
    md_file.write(markdown_content)

# # Convert markdown to HTML (optional, if needed)
html = markdown2.markdown(markdown_content)
html_file_path = './questionaire.html'
with open(html_file_path, 'w') as html_file:
    html_file.write(html)
