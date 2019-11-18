# opencv_pypy3

License : MIT

This repo contains wheel files of [opencv-python](https://github.com/skvark/opencv-python) built for pypy3.


`rearrange.py` is used to sort the generated header types in `_skbuild/$ARCH-$PYVER/cmake-build/modules/python_bindings_generator/pyopencv_generated_types.h` as a workaround for [this issue](https://bitbucket.org/pypy/pypy/issues/3117/fatal-rpython-error-when-importing-opencv).
