# Tic-Tac-Toe-Detector
Takes in a picture of a tic-tac-toe board, interprets the game state, and allows you to play the game starting at that game state.

This program requires the OpenCV library.

When you run ImageDetection.py, it checks for a camera and creates a window showing what the camera is looking at. Pressing the space bar takes a picture. It then checks for keypoints between the taken picture and 6rdTry.png to homogenize the taken picture. It then shows the homogenization process which can be seen with the 1-7 keys. After this is closed with the escape key, it checks it for x's and o's that look like O.png and x.png. If it detects them, it adds them to an array containing the read in board state and asks the user if the info is correct. If the user confirms, it prints the info to hi2.txt and runs TicTacToe.py with hi2.txt as an argument.

When you run TicTacToe.py, it first checks for a passed argument. If one exists, it reads in a board state from the given file. Otherwise it starts with a blank board. The game code loops through a few methods that print the current board, read in a move, and check if the game is over.

I have not tested the image detection with different cameras, but I don't think it'll work with different resolution cameras due to how the homogenized image is read. Otherwise, I don't think there's any bugs, but future work would include fixing that, making the code in ImageDetection.py cleaner, improving the image detection to work with handwritten x's and o's, and adding support for additional games like checkers.
