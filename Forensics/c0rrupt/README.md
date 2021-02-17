# c0rrupt
Points: 250

## Description
We found this [file](files/mystery). Recover the flag.

## Hints
Try fixing the file header

## Solution
Firstly, we can try to use the [```file```](https://linux.die.net/man/1/file) command to detect the file type. However, it does not return anything useful.

```
$ file mystery
mystery: data
```

Next, we can try to use a hex editor to analyse the file. In this case, I used [Hex Fiend](https://github.com/HexFiend/HexFiend) to solve this challenge. Alternatively, [ghex](https://wiki.gnome.org/Apps/Ghex) can also be used.

![Hex Fiend](images/0.png)

We can determine that the file is a PNG file. According to [this website](http://www.libpng.org/pub/png/spec/1.2/PNG-Contents.html), a PNG file contains several chunk types, such as sRGB, gAMA, pHYS (which we can see from the image above), IDAT, and IEND, and they can be found within this file.

```
$ xxd mystery | grep IDAT
00010000: 6927 db59 0000 fff4 4944 4154 3697 4678  i'.Y....IDAT6.Fx
00020000: ba6b c1fa 0000 fff4 4944 4154 d5df c0b7  .k......IDAT....
00030000: 5997 d200 0000 18a0 4944 4154 bb9d f54c  Y.......IDAT...L
```

```
$ xxd mystery | grep IEND
000318b0: 0000 0000 4945 4e44 ae42 6082            ....IEND.B`.
```

Therefore, we can try to change the file header from 
 
```89 65 4E 34 0D 0A B0 AA``` 

to

```89  50  4e  47  0d  0a  1a  0a```

![file header](images/1.png)

Next, we can use [```pngcheck```](http://www.libpng.org/pub/png/apps/pngcheck.html) command line tool to help us check our progress.

First, save the modified file. Then, execute the following command.

```
$ pngcheck -v mystery
File: mystery (202940 bytes)
  invalid chunk name "C"DR" (43 22 44 52)
```

Prior to fixing the file header, ```pngcheck``` will not recognise the file as a PNG file. Now, it recognised the file perfectly. However, a new type of error is raised based on the output.

According to the output, there is an invalid chunk name ```C"DR```. We can assume that it should be the ```IHDR``` chunk, which is one of the critical chunks of a PNG file and it is located right after the file header.

![IHDR chunk](images/2.png)

```
$ pngcheck -v mystery
File: mystery (202940 bytes)
  chunk IHDR at offset 0x0000c, length 13
    1642 x 1095 image, 24-bit RGB, non-interlaced
  chunk sRGB at offset 0x00025, length 1
    rendering intent = perceptual
  chunk gAMA at offset 0x00032, length 4: 0.45455
  chunk pHYs at offset 0x00042, length 9: 2852132389x5669 pixels/meter
  CRC error in chunk pHYs (computed 38d82c82, expected 495224f0)
ERRORS DETECTED in mystery
```

Now, we managed to fix the ```IHDR``` chunk, but another error is raised.