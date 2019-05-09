# blurhash-python

    import blurhash
    import PIL.Image
    import numpy
    
    PIL.Image.open("cool_cat_small.jpg")
    # Result:
    
![A picture of a cool cat.](/cool_cat_small.jpg?raw=true "A cool cat.")
    
    blurhash.encode(numpy.array(PIL.Image.open("cool_cat_small.jpg").convert("RGB")))
    # Result: 'UBL_:rOpGG-oBUNG,qRj2so|=eE1w^n4S5NH'
    
    PIL.Image.fromarray(numpy.array(blurhash.decode("UBMOZfK1GG%LBBNG,;Rj2skq=eE1s9n4S5Na", 128, 128)).astype('uint8'))
    # Result:

![Blurhash example output: A blurred cool cat.](/blurhash_example.png?raw=true "Blurhash example output: A blurred cool cat.")
    
Blurhash is an algorithm that lets you transform image data into a small text representation of a blurred version of the image. This is useful since this small textual representation can be included when sending objects that may have images attached around, since it can be used to quickly create a placeholder for images that are still loading or that should be hidden behind a content warning.

This library contains a pure-python implementation of the blurhash algorithm, closely following the original swift implementation by Dag Ågren. The module has no dependencies (the unit tests require PIL and numpy). It exports only two functions, "encode" and "decode". You can find usage details here: TODO.
