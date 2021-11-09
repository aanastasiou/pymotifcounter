# `mfinder`


## Obtaining `mfinder`

* `> ./fetch_mfinder.sh` 
    * Or download following [this link](https://www.weizmann.ac.il/mcb/UriAlon/download/network-motif-software).
    * Latest version (Nov 2021) is `1.21`.
    * Place the archive in `binaries/mfinder/mfinder1.21_unix.tar` and uncompress it in place.

## Compiling `mfinder`

* `> cd mfinder1.21`
* Edit the `Makefile` and add `-fcommon` to `CFLAGS`.
* `> make all`

This last step will create the `mfinder` executable in the location that 
`pymotifcounter` expects it to be by default (that is `binaries/mfinder/mfinder1.21/mfinder`).
