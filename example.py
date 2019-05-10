"""
Example "proper" blurhash usage
"""

import numpy as np
import PIL.Image
import blurhash

# Input/output file names
input_image = "tests/cool_cat.jpg"
output_image = "example_out.png"

# How many components do we want, maximum and minimum?
target_components = 4
min_components = 2

# Which maximum size should we work at for blurhash calculations?
work_size = 64

# What's the final intended output size?
out_size = (320, 180)

"""
Part 1: Encode
"""
# Load the image and store sizes (useful for decoding later, and likely part of your
# metadata objects anyways)
image = PIL.Image.open(input_image).convert("RGB")
image_size = (image.width, image.height)
print("Read image " + input_image + "({} x {})".format(image_size[0], image_size[1]))

# Convert to linear and thumbnail
image_linear = np.vectorize(blurhash.srgb_to_linear)(np.array(image))
image_linear_thumb = []
for i in range(3):
    channel_linear = PIL.Image.fromarray(image_linear[:,:,i].astype("float32"), mode = 'F')
    channel_linear.thumbnail((work_size, work_size))
    image_linear_thumb.append(np.array(channel_linear))
image_linear_thumb = np.transpose(np.array(image_linear_thumb), (1, 2, 0))
print("Encoder working at size: {} x {}".format(image_linear_thumb.shape[1], image_linear_thumb.shape[0]))

# Figure out a good component count
components_x = int(max(min_components, min(target_components, round(image_linear_thumb.shape[1] / (work_size / target_components)))))
components_y = int(max(min_components, min(target_components, round(image_linear_thumb.shape[0] / (work_size / target_components)))))
print("Using component counts: {} x {}".format(components_x, components_y))

# Create blurhash
blur_hash = blurhash.encode(image_linear_thumb, components_x, components_y, linear = True)
print("Blur hash of image: " + blur_hash)

"""
Part 2: Decode
"""
# Figure out what size to decode to
decode_components_x, decode_components_y = blurhash.components(blur_hash)
decode_size_x = decode_components_x * (work_size // target_components)
decode_size_y = decode_components_y * (work_size // target_components)
print("Decoder working at size {} x {}".format(decode_size_x, decode_size_y))

# Decode
decoded_image = np.array(blurhash.decode(blur_hash, decode_size_x, decode_size_y, linear = True))

# Scale so that we have the right size to fill out_size without letter/pillarboxing
# while matching original images aspect ratio.
fill_x_size_y = out_size[0] * (image_size[0] / image_size[1])
fill_y_size_x = out_size[1] * (image_size[1] / image_size[0])
scale_target_size = list(out_size)
if fill_x_size_y / out_size[1] < fill_y_size_x / out_size[0]:
    scale_target_size[0] = max(scale_target_size[0], int(fill_y_size_x))
else:
    scale_target_size[1] = max(scale_target_size[1], int(fill_x_size_y))

# Scale (ideally, your UI layer should take care of this in some kind of efficient way)
print("Scaling to target size: {} x {}".format(scale_target_size[0], scale_target_size[1]))
decoded_image_large = []
for i in range(3):
    channel_linear = PIL.Image.fromarray(decoded_image[:,:,i].astype("float32"), mode = 'F')
    decoded_image_large.append(np.array(channel_linear.resize(scale_target_size, PIL.Image.BILINEAR)))
decoded_image_large = np.transpose(np.array(decoded_image_large), (1, 2, 0))

# Convert to srgb PIL image
decoded_image_out = np.vectorize(blurhash.linear_to_srgb)(np.array(decoded_image_large))
decoded_image_out = PIL.Image.fromarray(np.array(decoded_image_out).astype('uint8'))

# Crop to final size and write
decoded_image_out = decoded_image_out.crop((
    (decoded_image_out.width - out_size[0]) / 2,
    (decoded_image_out.height - out_size[1]) / 2,
    (decoded_image_out.width + out_size[0]) / 2,
    (decoded_image_out.height + out_size[1]) / 2,
))
decoded_image_out.save(output_image)
print("Wrote final result to " + str(output_image))
