#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: update.py
# @Created:  2021-05-27 08:32:47
# @Modified: 2021-05-28 08:52:41

__version__ = "0.2"


class _Mode:
    @property
    def normal(self):
        """终端默认样式"""
        return 0

    @property
    def bold(self):
        """高亮或加粗"""
        return 1

    @property
    def underline(self):
        """下划线"""
        return 4

    @property
    def blink(self):
        """闪烁"""
        return 5

    @property
    def invert(self):
        """反白"""
        return 7

    @property
    def hide(self):
        """隐藏"""
        return 8


class _ForegroundColor:
    @property
    def black(self):
        return 30

    @property
    def red(self):
        return 31

    @property
    def green(self):
        return 32

    @property
    def yellow(self):
        return 33

    @property
    def blue(self):
        return 34

    @property
    def purple(self):
        return 35

    @property
    def cyan(self):
        return 36

    @property
    def white(self):
        return 37


class _BackgroudColor:
    @property
    def black(self):
        return 40

    @property
    def red(self):
        return 41

    @property
    def green(self):
        return 42

    @property
    def yellow(self):
        return 43

    @property
    def blue(self):
        return 44

    @property
    def purple(self):
        return 45

    @property
    def cyan(self):
        return 46

    @property
    def white(self):
        return 47


class DisplayStyle:
    foreground_color = _ForegroundColor()
    backgorud_color = _BackgroudColor()
    mode = _Mode()

    @property
    def end(self):
        return 0

    def format_with_one_style(self, src: str, style: int) -> str:
        if type(src) != str:
            raise TypeError(f"type of `src` is {type(src)}, not str")

        if type(style) != int:
            raise TypeError(f"type of `style` is {type(src)}, not int")

        fmt = '\033[%dm%s\033[%dm'
        return fmt % (style, src, self.end)

    def format_with_multiple_styles(self, src: str, *styles: int) -> str:
        if type(src) != str:
            raise TypeError(f"type of `src` is {type(src)}, not str")

        if len(styles) < 2:
            raise TypeError("At least two styles")

        styles_str = []

        for style in styles:
            if type(style) != int:
                raise TypeError(f"type of `style` - [ {style} ] is {type(src)}, not int")
            styles_str.append(str(style))

        style = ";".join(styles_str)
        return f"\033[{style}m{src}\033[{self.end}m"
