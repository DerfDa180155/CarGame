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

Added entropy calculation. The entropy tells you how many different patterns can be at one point of the map. It is calculated, by checking all the 4 neighbor squares and check which pieces can fit. This is needed for the Wave Function Collapse.
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


## 09.01.2024

I re-wrote the entire algorithm for the map generator because the old one was very slow and had a lot of errors. The new algorithm no longer uses recursion. The algorithm always looks for the next closest empty field and then assigns a random image to it. However, the algorithm has a small error, because an empty field is always output in the bottom right corner.


## 10.01.2024

Fixed the bug in the map generator, that created an empty field in the bottom right corner. 


## 11.01.2024

Created a new thread, that updates the display. With the new thread it is possible to separate the main game from the display in order to carry out calculations in the background.


## 12.01.2024

I added a communications object. The display thread and the main game therad communicate with each other via this communication object. For example, the current game status is stored in the object.


## 13.01.2024

The status is now stored in the Object and used. You can now change the status using a key. So far there are only 2 statuses.


## 14.01.2024

Added new keys to test the map generator.


## 15.01.2024

Cleaned my code and removed code that is no longer needed.
Added map cleaner. This cleans up the generated maps so that only the longest street is displayed.


## 16.01.2024

Created a player, which is a square right now. The player will be a car in the future. Added keys to control it


## 17.01.2024

Updated the ToDo List, added new points and marked what is already done.


## 18.01.2024

Made the window resizable


## 19.01.2024

Made the player scale to the current size of the screen.


## 20.01.2024

Made the Text scale to the current size of the screen.


## 21.01.2024

Added buttons to change the menu and open my GitHub profile.
Created a new Image for the settings button.


## 22.01.2024

Started coding a new map controller.
Cleaned my code.


## 23.01.2024

Added a raceMap class, to store more information about a map.


## 24.01.2024

Implemented the new map controller in the current game.


## 25.01.2024

Updated the GUI, added more menu buttons.


## 26.01.2024

Added a map saver with XML.


## 27.01.2024

Added a map reader so all the saved maps can be loaded.


## 28.01.2024

Updated the gui and implemented buttons to select a saved map.


## 29.01.2024

Saved the information of the mode of the current race, so that the race can be started correctly.


## 30.01.2024

Started with a bounds generator of the maps. This bounds are needed, so that the players and the bots can not leave the track.


## 31.01.2024

Completion of the bound generator, which now works for every map.


## 01.02.2024

Added a second player that can be controlled in the multiplayer mode.


## 02.02.2024

Started with the checkpoint generation. A Checkpoint is a line with the start and end point at the bounds. These checkpoints are created between 2 road map pieces. The checkpoints are needed, to know that a player drives in the right direction.


## 03.02.2024

Finished the checkpoint generation.


## 04.02.2024

Started with ray casting and displaying the rays.


## 05.02.2024

Finished ray casting.


## 06.02.2024

Updated the movement, based on the closest distance off the front rays of a player. Players can no longer drive through walls.


## 07.02.2024

Added a raceObject, which controls the race. Implemented a clock in the raceObject.


## 08.02.2024

Updated the raceObject and added keys to control the race.


## 09.02.2024

Implemented the checkpoints to the raceObject.


## 10.02.2024

Implemented the display of the current round of the 2 players.


## 11.02.2024

Added a leaderboard system and started displaying it.


## 12.02.2024

Added text display of the leaderboard.


## 13.02.2024

Added a starting countdown to the race.


## 14.02.2024

Added a pause menu during a race.


## 15.02.2024

Added two buttons to the leaderboard. One button restarts the race and the other opens the map selector.


## 16.02.2024

Added three buttons to the pause menu. These buttons restart the race, resume the race and quit the race and return to the main menu.


## 17.02.2024

Added text on the map buttons to display the name of the map.


## 18.02.2024

Updated the start countdown, to display the entire countdown.


## 19.02.2024

Updated the player movement. Added acceleration to change the speed of the player.


## 20.02.2024

Updated the player steering. Added a slight slide for the player when steering.


## 21.02.2024

Added a speed boost that increase the max speed for a short time. This speedbost is obtained while steering.


## 22.02.2024

Updated the speed boost to occur after steering rather than during steering. Balanced the speed and duration of the boost.


## 23.02.2024

Added map name on pause and leaderboard screen.


## 24.02.2024

Added a new menu, where the race settings can be set.


## 25.02.2024

Implemented a preview of the map in the race settings menu.


## 26.02.2024

Implemented default race settings.


## 27.02.2024

Added scroll buttons to the race setting menu to change and set the settings.


## 28.02.2024

Updated the pause menu to display the current race settings.


## 29.02.2024

Created new maps.


## 01.03.2024

Started with a better visualisation of the finish line.


## 02.03.2024

Updated finish line texture.


## 03.03.2024

Updated the checkpoint generation to start at the players starting position.


## 04.03.2024

Started updating the checkpoint generation rotation, to go clockwise or counter clockwise, depending on the player starting direction.


## 05.03.2024

Finished checkpoint generation rotation.


## 06.03.2024

Added the map generator in the map selector.


## 07.03.2024

Added random starting positions and random directions to the generator. Fixed a bug where the rotation of the checkpoints not always work.


## 08.03.2024

Started with the documentation and updated the todo list.


## 09.03.2024

Updated the map generator, so that the old generated map is deleted when a new one is generated.


## 10.03.2024

Fixed a bug in the map generator, where an empty map is created.


## 11.03.2024

Implemented the option to save a generated map in a custom maps folder.


## 12.03.2024

Fixed a bug in the map loader, where custom maps where loaded. Also fixed a bug where the values of the starting position had decimal places and therefore couldn´t be stored in an int variable. Changed the variable to float in the whole programm.


## 13.03.2024

Added a new button to the leaderboard that saves the map. This button is only displayed when a generated map was played.


## 14.03.2024

Fixed a bug in the checkpoint generation, where the checkpoints were not generated and rotated correctly. This bug appears only in one case.


## 15.03.2024

Added menu headings to some menus.


## 16.03.2024

Updated the map loader to sort the maps by their names.


## 17.03.2024

Updated the map cleaner to remove empty rows and columns and therefore zoom into the generated map.


## 18.03.2024

Updated the map loader to load the custom maps.


## 19.03.2024

Started updating the map selector, to have multiple map pages. There is a maximum of 15 maps per page. The custom maps are showen on a seperate own page. Updated the button class, so that a button can be enabled and disabled.
























