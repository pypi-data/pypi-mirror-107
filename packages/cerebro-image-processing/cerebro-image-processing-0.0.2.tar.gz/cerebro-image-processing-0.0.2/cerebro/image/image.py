# ------------------------------------------------------------------------------
#  MIT License
#
#  Copyright (c) 2021 Cerebro Labs. All rights reserved.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# ------------------------------------------------------------------------------
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from cerebro.image import COLORS, ColorsConverter


class Image:
    """
    This class is used to handle an image.
    ---------
    @author:    Hieu Pham.
    @created:   19-05-2021.
    @updated:   27-05-2021.
    """

    @property
    def data(self):
        """Get image data as numpy/mat array."""
        return self._data

    @property
    def colors(self):
        """Get image colorspace."""
        return self._colors

    @property
    def shape(self):
        """Get image shape."""
        return None if self._data is None else self._data.shape

    @property
    def dim(self):
        """Get image dimensions."""
        return None if self.shape is None else len(self.shape)

    @property
    def title(self):
        """Get image title."""
        return self._title

    def __init__(self, src=None, unchange: bool = False):
        """
        Construct an image from source as grayscale or RGB.
        :param src:         image source.
        :param unchange:    do not change order of channel.
        """
        # Initialize.
        self._data, self._title, self._colors = None, None, None
        # Read image if source exists.
        if src is not None:
            self.read(src=src, unchange=unchange)

    def read(self, src=None, unchange: bool = False):
        """
        Read image from source as grayscale or RGB.
        :param src:         image source.
        :param unchange:    do not change order of channel.
        :return:            image itself.
        """
        # Read image from array.
        if isinstance(src, (list, np.ndarray)):
            self._data = np.squeeze(src).astype(np.uint8)
            self._title = 'array.jpg'
        # Read image from string.
        elif isinstance(src, str):
            # Read image from file path string.
            if os.path.isfile(src):
                self._data = cv2.imread(src, cv2.IMREAD_UNCHANGED)
                self._title = str(src.split('/')[-1])
            # Otherwise, read image from pure string.
            else:
                self._data = cv2.imdecode(np.fromstring(src).astype(np.uint8), cv2.IMREAD_UNCHANGED)
                self._title = 'buffer.jpg'
        # Set image colors based on image dimension.
        if self.dim == 2:
            self._colors = COLORS.GRAY
        elif self.dim == 3 and (not unchange):
            self._colors = COLORS.RGB
            self._data = self.data[:, :, ::-1]
        # Return result.
        return self

    def write(self, file: str = None):
        """
        Write image to file.
        :param file:    file to write.
        :return:        image itself.
        """
        # Validate file.
        file = self._title if file is None else file
        # Extract file extension.
        name, ext = os.path.splitext(file)
        ext = '.jpg' if '.' not in ext else ext
        file = '%s%s' % (name, ext)
        # Swap channel to make BRG image for opencv.
        image = self.data if self.dim <= 2 else self.data[:, :, ::-1]
        # PNG image will be written at maximum compression ratio.
        if ext == '.png':
            cv2.imwrite(file, image, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        # JPEG image will be written as 80% quality to keep the file small.
        elif ext == '.jpg' or ext == '.jpeg':
            cv2.imwrite(file, image, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        # Otherwise, write as default.
        else:
            cv2.imwrite(file, image)
        # Return result.
        return self

    def show(self, title: str = None, view: str = None):
        """
        Show image to view window.
        :param title:   window title.
        :param view:    view engine.
        :return:        image itself.
        """
        # Validate window title.
        title = self._title if title is None else title
        # Show via matplotlib engine.
        if view in ['matplotlib', 'plt']:
            if self.colors == COLORS.GRAY or self.colors == COLORS.BIN:
                plt.imshow(self.data, cmap='gray', vmin=0, vmax=255, interpolation='bicubic')
            else:
                plt.imshow(self.data, interpolation='bicubic')
            plt.title(title)
            plt.show()
        # Show via default opencv engine.
        else:
            cv2.imshow(title, self.data if self.dim <= 2 else self.data[:, :, ::-1])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        # Return result.
        return self

    def set_title(self, title: str = 'untitled.jpg'):
        """
        Set image title.
        :param title:   image title.
        :return:        image itself.
        """
        # Set image title.
        self._title = str(title)
        # Return result.
        return self

    def convert(self, colors: COLORS = COLORS.RGB):
        """
        Convert image colors to desired one.
        :param colors:  desired colors.
        :return:        image itself.
        """
        # Perform color convert.
        self._data = ColorsConverter.convert(self.colors, colors)(self.data)
        self._colors = colors
        # Return result.
        return self

    def resize(self, size: tuple = (224, 224), resample: int = cv2.INTER_CUBIC):
        """
        Resize image to desired size.
        :param size:        desired size.
        :param resample:    resampling method.
        :return:            image itself.
        """
        # Resize image.
        self._data = cv2.resize(self.data, size, interpolation=resample)
        # Return result.
        return self

    def square_pad(self):
        """
        Convert image into square image with zero-paddings.
        :return:    squared image.
        """
        # Calculate elements.
        h, w = self.shape[0], self.shape[1]
        max_edge = max(h, w)
        dh, dw = max_edge - h, max_edge - w
        top, bottom = dh // 2, dh - (dh // 2)
        left, right = dw // 2, dw - (dw // 2)
        # Square padding.
        self._data = cv2.copyMakeBorder(self.data, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        # Return result.
        return self.set_title('%s-squared%s' % os.path.splitext(self.title))
