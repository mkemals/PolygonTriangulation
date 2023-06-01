import PIL.Image as Image
import PIL.ImageDraw as ImageDraw

im = Image.new("RGB", (400, 300))

draw = ImageDraw.Draw(im)

draw.polygon(((200, 100), (300, 200), (400, 150)))

im.show()

