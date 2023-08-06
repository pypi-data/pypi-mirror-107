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
import cv2
from enum import Enum


class COLORS(Enum):
    """
    This class defines all supported color-system of the program.
    ---------
    @author:    Hieu Pham.
    @created:   19-05-2021.
    @updated:   27-05-2021.
    """
    # Binary color.
    BIN = -1
    # Grayscale color.
    GRAY = 0
    # Red, Green, Blue color.
    RGB = 1
    # Hue, Saturation, Lightness color.
    HSV = 2
    # LAB color. @reference: https://en.wikipedia.org/wiki/CIELAB_color_space.
    LAB = 3
    # YCbCr color is used in video and digital photography systems.
    YCrCb = 4


class ColorsConverter:
    """
    This class includes colors converters methods.
    ---------
    @author:    Hieu Pham.
    @created:   27-05-2021.
    @updated:   27-05-2021.
    """

    @staticmethod
    def convert(from_colors: COLORS = COLORS.RGB, to_colors: COLORS = COLORS.RGB):
        """
        Get function to convert between two colors.
        :param from_colors:     color to be converted.
        :param to_colors:       color to convert to.
        """
        # Validate from colors.
        assert from_colors != COLORS.BIN, 'Binary color does not have enough information to be converted to others.'
        # Return necessary converter method.
        if from_colors == COLORS.RGB:
            return ColorsConverter.rgb_to(to_colors)
        elif from_colors == COLORS.GRAY:
            return ColorsConverter.gray_to(to_colors)
        elif from_colors == COLORS.HSV:
            return ColorsConverter.hsv_to(to_colors)
        elif from_colors == COLORS.LAB:
            return ColorsConverter.lab_to(to_colors)
        elif from_colors == COLORS.YCrCb:
            return ColorsConverter.ycbcr_to(to_colors)
        else:
            return lambda x: x

    @staticmethod
    def rgb_to(colors: COLORS = COLORS.RGB):
        """
        Get function to convert RGB to desired colors.
        :param colors:  desired colors.
        :return:        function to convert colors.
        """
        if colors == COLORS.BIN:
            return lambda x: ColorsConverter.gray_to(colors)(cv2.cvtColor(x, cv2.COLOR_RGB2GRAY))
        if colors == COLORS.GRAY:
            return lambda x: cv2.cvtColor(x, cv2.COLOR_RGB2GRAY)
        elif colors == COLORS.HSV:
            return lambda x: cv2.cvtColor(x, cv2.COLOR_RGB2HSV)
        elif colors == COLORS.LAB:
            return lambda x: cv2.cvtColor(x, cv2.COLOR_RGB2LAB)
        elif colors == COLORS.YCrCb:
            return lambda x: cv2.cvtColor(x, cv2.COLOR_RGB2YCrCb)
        else:
            return lambda x: x

    @staticmethod
    def gray_to(colors: COLORS = COLORS.GRAY):
        """
        Get function to convert grayscale to desired colors.
        :param colors:  desired colors.
        :return:        function to convert colors.
        """
        if colors == COLORS.BIN:
            return lambda x: cv2.adaptiveThreshold(x, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        elif colors == COLORS.GRAY:
            return lambda x: x
        else:
            return lambda x: ColorsConverter.rgb_to(colors)(cv2.cvtColor(x, cv2.COLOR_GRAY2RGB))

    @staticmethod
    def hsv_to(colors: COLORS = COLORS.HSV):
        """
        Get function to convert HSV to desired colors.
        :param colors:  desired colors.
        :return:        function to convert colors.
        """
        return lambda x: x if colors == COLORS.HSV \
            else ColorsConverter.rgb_to(colors)(cv2.cvtColor(x, cv2.COLOR_HSV2RGB))

    @staticmethod
    def lab_to(colors: COLORS = COLORS.LAB):
        """
        Get function to convert LAB to desired colors.
        :param colors:  desired colors.
        :return:        function to convert colors.
        """
        return lambda x: x if colors == COLORS.LAB \
            else ColorsConverter.rgb_to(colors)(cv2.cvtColor(x, cv2.COLOR_LAB2RGB))

    @staticmethod
    def ycbcr_to(colors: COLORS = COLORS.YCrCb):
        """
        Get function to convert YCbCr to desired colors.
        :param colors:  desired colors.
        :return:        function to convert colors.
        """
        return lambda x: x if colors == COLORS.YCrCb \
            else ColorsConverter.rgb_to(colors)(cv2.cvtColor(x, cv2.COLOR_YCrCb2RGB))
