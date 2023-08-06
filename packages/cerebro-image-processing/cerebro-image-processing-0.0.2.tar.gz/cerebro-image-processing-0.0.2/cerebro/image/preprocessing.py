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
from cerebro.image import Image, COLORS


class Preprocessing:
    """
    This class includes preprocessing utility functions.
    ---------
    @author:    Hieu Pham.
    @created:   27-05-2021.
    @updated:   27-05-2021.
    """

    @staticmethod
    def histogram_equalization(image: Image = None) -> Image:
        """
        Perform histogram equalization.
        :param image:   input image.
        :return:        equalized image.
        """
        # Equalize grayscale image.
        if image.dim <= 2:
            result = Image(cv2.equalizeHist(image.data))
        # Equalize colored image.
        else:
            colors = image.colors
            # Convert to YCrCb and perform equalization at Y-channel.
            data = image.convert(COLORS.YCrCb).data
            data[:, :, 0] = cv2.equalizeHist(data[:, :, 0])
            # Create image and convert back to origin colors.
            result = Image(data, unchange=True)
            result._colors = COLORS.YCrCb
            result.convert(colors)
        # Return result.
        return result.set_title('%s-equalized%s' % os.path.splitext(image.title))
