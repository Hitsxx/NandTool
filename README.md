# README #

This repository contains several opensource tools I have written.

Most of the time, each tool has its corresponding blog post.


## firmware-reconstruct.py ##

This script reconstructs a file out of multiple dumps that contains random errors.

Its principle is very basic: for each byte the scripts computes the most frequent value encountered and writes it on the output.

More about this tool [on my related blog post](http://blog.j-michel.org/post/61394420099/firmware-extraction-and-reconstruction)

```
#!sh

usage: ./firmware-reconstruct.py [-h] -o OUTFILE INFILE [INFILE ...]

positional arguments:
  INFILE                Input files

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --output OUTFILE
                        Destination of the rebuilt image
```


## Vingcard.py ##

This is a scapy layer used to dissect Mifare Ultralight dumps corresponding to Vingcard Elsafe hotel key cards.

It can be used either from scapy or as a standalone script. In the latter case, it will dissect the dump and prints on stdout the result.

Read more about it [on this related blog post](http://blog.j-michel.org/post/85755629755/rfid-followup-on-vingcard)


```
#!sh


usage: ./Vingcard.py [-h] FILE

positional arguments:
  FILE

optional arguments:
  -h, --help  show this help message and exit
```

## Nand-dump-tool.py ##

This script deals with NAND flash dumps, extracting the spare area out of a complete chip dump file.

It allows you to specify either the chip parameters (page size and OOB size) or the chip ID code.

By default it will split the dump against a **separate** layout but you can override that by explicitly specifying an **adjacent** layout or try the experimental **guess** layout. The script will first analyze the two possible layouts and use a Hamming distance to choose which one fits best.

You can read more about that tool [on the related blog post](http://blog.j-michel.org)
```
#!sh

usage: ./Nand-dump-tool.py [-h] -i FILE -o FILE [-I ID] [--page-size PAGE]
                           [--oob-size SIZE] [--save-oob FILE]
                           [--layout {adjacent,separate,guess}]

optional arguments:
  -h, --help            show this help message and exit
  -i FILE, --input FILE
  -o FILE, --output FILE
  -I ID, --idcode ID
  --page-size PAGE
  --oob-size SIZE
  --save-oob FILE
  --layout {adjacent,separate,guess}
```

