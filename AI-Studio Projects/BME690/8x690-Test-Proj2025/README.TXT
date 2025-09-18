USB MTP Firmware : v1.4
Date : 17-05-2021
Filesystem : FlogFS
Board : APP3.1
Manufacturer : Bosch Sensortec GmbH

Open source software information
--------------------------------
1.FlogFS
    Link   - https://github.com/conservify/FLogFS
    Author - Ben Nahill <bnahill@gmail.com>

2.Android Open Source Project (AOSP)
    Link - https://android.googlesource.com/platform/frameworks/av/+/android-5.1.1_r8/media/mtp/mtp.h

Known limitations
---------------------------------
  MTP stack and FlogFS filesystem
        * Maximum of 128 files is accessible in a session
        * Renaming files not supported
        * File name is limited to 40 characters
        * No support for directories, file timestamps
