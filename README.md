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
    
This is a pure-python implementation of the blurhash algorithm in pure python, closely following the original swift implementation by Dag Ågren.
