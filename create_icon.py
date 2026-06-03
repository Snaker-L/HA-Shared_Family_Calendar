from PIL import Image, ImageDraw

img = Image.new('RGB', (256, 256), color='white')
draw = ImageDraw.Draw(img)
draw.rectangle([20, 40, 236, 236], outline='#1e88e5', width=4, fill='#f5f5f5')
draw.rectangle([20, 40, 236, 80], fill='#1e88e5')

for i in range(1, 7):
    draw.line([(20 + i * (216/7), 80), (20 + i * (216/7), 236)], fill='#cccccc', width=2)

for i in range(1, 5):
    draw.line([(20, 80 + i * (156/5)), (236, 80 + i * (156/5))], fill='#cccccc', width=2)

img.save('icon.png')
print("Icon created successfully")
