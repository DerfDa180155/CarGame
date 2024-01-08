# DevLog

## 01.01.2024

Created the git repository and wrote the first documentation of the project.
MIT LICENSE added


## 02.01.2024

Links in README added


## 03.01.2024

First map images drawn, these will later be used for the map generator.
First code written, this loads all images and displays them in random order. These images are also scaled to the window size.


## 04.01.2024

Added display maps using 2 dimensional arrays. These arrays can be infinitely large. 
For example: 1x1, 30x30, 100x100, ...
Starting with the map generator using Wave Function Collapse. This generator then delivers this 2 dimensional array. You will be able to adjust later how big the map should be and where the starting point is.


## 05.01.2024

Added entropy calculation. The entropy tells you how many different patterns can be at one point of the map. It is caculated, by checking all the 4 neighbour squares and check which pieces can fit. This is needed for the Wave Function Collapse.
Fixed a display bug, where the map was displayed mirrored.


## 06.01.2024

Added the first part of Wave Function Collapse.
Fixed bug in entropy calculation where entropy was calculated for a field that is not empty.


## 07.01.2024

Fixed a small display error where the images were not displayed correctly.
New map images created.
Wave Function Collapse now works almost perfectly, but still has a small error where it may be that not all fields are filled.


## 08.01.2024

Wave function collapse bugs fixed, but there is still a small bug where some fields don't get an image.






