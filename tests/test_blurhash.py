import sys, os
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(base_path, '..'))

import PIL
import PIL.Image
import blurhash
import numpy as np
import pytest

def test_encode():
    image = PIL.Image.open(os.path.join(base_path, "cool_cat.jpg"))
    blur_hash = blurhash.encode(np.array(image.convert("RGB")))
    assert blur_hash == "UBMOZfK1GG%LBBNG,;Rj2skq=eE1s9n4S5Na"
    
def test_decode():
    image = blurhash.decode("UBMOZfK1GG%LBBNG,;Rj2skq=eE1s9n4S5Na", 32, 32)
    reference_image = np.load(os.path.join(base_path, "blurhash_out.npy"))
    assert np.sum(np.abs(image - reference_image)) < 1.0

def test_asymmetric():
    image = PIL.Image.open(os.path.join(base_path, "cool_cat.jpg"))
    blur_hash = blurhash.encode(np.array(image.convert("RGB")), components_x = 2, components_y = 8)
    assert blur_hash == "%BMOZfK1BBNG2skqs9n4?HvgJ.Nav}J-$%sm"
    
    decoded_image = blurhash.decode(blur_hash, 32, 32)
    assert np.sum(np.var(decoded_image, axis = 0)) > np.sum(np.var(decoded_image, axis = 1))

    blur_hash = blurhash.encode(np.array(image.convert("RGB")), components_x = 8, components_y = 2)
    decoded_image = blurhash.decode(blur_hash, 32, 32)
    assert np.sum(np.var(decoded_image, axis = 0)) < np.sum(np.var(decoded_image, axis = 1))

def test_components():
    image = PIL.Image.open(os.path.join(base_path, "cool_cat.jpg"))
    blur_hash = blurhash.encode(np.array(image.convert("RGB")), components_x = 8, components_y = 3)
    size_x, size_y = blurhash.components(blur_hash)
    assert size_x == 8
    assert size_y == 3

def test_linear_dc_only():
    image = PIL.Image.open(os.path.join(base_path, "cool_cat.jpg"))
    linearish_image = np.array(image.convert("RGB")) / 255.0
    blur_hash = blurhash.encode(linearish_image, components_x = 1, components_y = 1, linear = True)
    avg_color = blurhash.decode(blur_hash, 1, 1, linear = True)
    reference_avg_color = np.mean(linearish_image.reshape(linearish_image.shape[0] * linearish_image.shape[1], -1), 0)
    assert np.sum(np.abs(avg_color - reference_avg_color)) < 0.01
    
def test_invalid_parameters():
    image = np.array(PIL.Image.open(os.path.join(base_path, "cool_cat.jpg")).convert("RGB"))
    
    with pytest.raises(ValueError):
         blurhash.decode("UBMO", 32, 32)
         
    with pytest.raises(ValueError):
         blurhash.decode("UBMOZfK1GG%LBBNG", 32, 32)
         
    with pytest.raises(ValueError):
        blurhash.encode(image, components_x = 0, components_y = 1)
    
    with pytest.raises(ValueError):
        blurhash.encode(image, components_x = 1, components_y = 0)    
    
    with pytest.raises(ValueError):
        blurhash.encode(image, components_x = 1, components_y = 10)
      
    with pytest.raises(ValueError):
        blurhash.encode(image, components_x = 10, components_y = 1)
