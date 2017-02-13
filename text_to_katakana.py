#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtranslate import translate


def main():
    to_translate = 'Procter & Gamble'
    print(translate(to_translate))
    print(translate(to_translate, 'ja'))
    print(translate(to_translate, 'ru'))


if __name__ == '__main__':
    main()
