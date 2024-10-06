# esoteric-python
Encode any Python >= 3.9 program in 9 unique characters

These 9 characters are: cex'=%() and the '\n' newline character.

Compared to other esoteric Python variants, this variant uses the fewest unique characters for Python 3 and produces the smallest output files. Output file size grows linearly with the input file size with a low coefficient. Execution overhead is also optimized to obtain a fast startup time linear to the program size. Actual program execution speed is same as the original and is unaffected at all. Main python code is encoded in 7 unique characters and stored in the 'x' variable. A decoder for this program written in 9 unique characters is bundled in the output file. Works for any ASCII or ISO/IEC 8859-1 encoded python program and produces valid working python code.

Inspired by [[https://codegolf.stackexchange.com/questions/110648/fewest-distinct-characters-for-turing-completeness/110722#110722]]
Although 8 unique characters is possible for Python 3, its output size grows exponentially compared to linearly with 9 characters.

Run driver.py to use the encode any python code in the 9 characters.
Run esoteric-all.py to use the encode the source files of esoteric-python in the 9 characters.
Look inside driver.py on how to use esoteric-python.

