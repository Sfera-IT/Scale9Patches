#!/bin/env python3

'''
MIT License

Copyright (c) 2020 Federico Fuga <fuga@studiofuga.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import argparse
from PIL import Image


class PatchGenerator:
    def __init__(self):
        pass

    def parseCommandLine(self):
        parser = argparse.ArgumentParser(description='Generate a scaled version of the source image with 9 patch method')
        parser.add_argument('infile',  type=str, help='The input file')
        parser.add_argument('outfile', type=str, help='The output file')
        parser.add_argument('--size', dest='size', type=int, nargs=2, help='the size of the destination file, width and height')
        parser.add_argument('--scale', dest='scale', type=float, default=0.5, help='the scaling factor')
        parser.add_argument('--border', dest='border', type=int, default=9, help='the size of the border')

        self.params = parser.parse_args()

    def run(self):
        img = Image.open(self.params.infile)
        if self.params.size == None:
            self.width = img.width * self.params.scale
            self.height = img.height * self.params.scale
        else:
            self.width = self.params.size[0]
            self.height = self.params.size[1]

        target = Image.new(size=[self.width, self.height], mode = img.mode)

        self.cx = self.params.border
        self.cy = self.params.border
        self.dx = img.width - self.params.border
        self.dy = img.height - self.params.border

        self.ddx = self.width - self.params.border
        self.ddy = self.height - self.params.border

        topleft = img.crop([0, 0, self.cx, self.cy])
        topright = img.crop([self.dx, 0, img.width, self.cy])
        botleft = img.crop([0, self.dy, self.cx, img.height])
        botright = img.crop([self.dx, self.dy, img.width, img.width])

        top = img.resize(size=[self.width - 2 * self.params.border, self.params.border], box=[self.cx, 0, self.dx, self.cy])
        bot = img.resize(size=[self.width - 2 * self.params.border, self.params.border], box=[self.cx, self.dy, self.dx, img.height])

        left = img.resize(size=[self.params.border, self.height - 2 * self.params.border], box=[0, self.cy, self.cx, self.dy])
        right = img.resize(size=[self.params.border, self.height - 2 * self.params.border], box=[self.dx, self.cy, img.width, img.height - self.cy])

        center = img.resize(size=[self.ddx-self.cx, self.ddy - self.cy], box=[self.cx, self.cy, self.dx, self.dy])

        target.paste(topleft, [0,0])
        target.paste(top, [self.cx,0])
        target.paste(topright, [self.width-self.params.border,0])

        target.paste(left, [0, self.cy])
        target.paste(center, [self.cx, self.cy])
        target.paste(right, [self.ddx, self.cy])

        target.paste(botleft, [0, self.ddy])
        target.paste(bot, [self.cx, self.ddy])
        target.paste(botright, [self.ddx, self.ddy])

        target.save(self.params.outfile)


if __name__ == '__main__':
    generator = PatchGenerator()
    generator.parseCommandLine()
    generator.run()

