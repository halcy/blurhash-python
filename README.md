# blurhash-python
```python
import blurhash
import PIL.Image
import numpy

PIL.Image.open("cool_cat_small.jpg")
# Result:
```
![A picture of a cool cat.](/cool_cat_small.jpg?raw=true "A cool cat.")
```python
blurhash.encode(numpy.array(PIL.Image.open("cool_cat_small.jpg").convert("RGB")))
# Result: 'UBL_:rOpGG-oBUNG,qRj2so|=eE1w^n4S5NH'

PIL.Image.fromarray(numpy.array(blurhash.decode('UBL_:rOpGG-oBUNG,qRj2so|=eE1w^n4S5NH', 128, 128)).astype('uint8'))
# Result:
```
![Blurhash example output: A blurred cool cat.](/blurhash_example.png?raw=true "Blurhash example output: A blurred cool cat.")
    
Blurhash is an algorithm that lets you transform image data into a small text representation of a blurred version of the image. This is useful since this small textual representation can be included when sending objects that may have images attached around, which then can be used to quickly create a placeholder for images that are still loading or that should be hidden behind a content warning.

This library contains a pure-python implementation of the blurhash algorithm, closely following the original swift implementation by Dag Ågren. The module has no dependencies (the unit tests require PIL and numpy). You can install it via pip:

```bash
$ pip3 install blurhash
```

It exports five functions:
* "encode" and "decode" do the actual en- and decoding of blurhash strings
* "components" returns the number of components x- and y components of a blurhash
* "srgb_to_linear" and "linear_to_srgb" are colour space conversion helpers

Have a look at example.py for an example of how to use all of these working together.

Documentation for each function:

```python
blurhash.encode(image, components_x = 4, components_y = 4, linear = False):
"""
Calculates the blurhash for an image using the given x and y component counts.

Image should be a 3-dimensional array, with the first dimension being y, the second
being x, and the third being the three rgb components that are assumed to be 0-255 
srgb integers (incidentally, this is the format you will get from a PIL RGB image).

You can also pass in already linear data - to do this, set linear to True. This is
useful if you want to encode a version of your image resized to a smaller size (which
you should ideally do in linear colour).
"""

blurhash.decode(blurhash, width, height, punch = 1.0, linear = False)
"""
Decodes the given blurhash to an image of the specified size.
    
Returns the resulting image a list of lists of 3-value sRGB 8 bit integer
lists. Set linear to True if you would prefer to get linear floating point 
RGB back.

The punch parameter can be used to de- or increase the contrast of the
resulting image.

As per the original implementation it is suggested to only decode
to a relatively small size and then scale the result up, as it
basically looks the same anyways.
"""

blurhash.srgb_to_linear(value):
"""
srgb 0-255 integer to linear 0.0-1.0 floating point conversion.
"""
    
blurhash.linear_to_srgb(value):
"""
linear 0.0-1.0 floating point to srgb 0-255 integer conversion.
"""
```
