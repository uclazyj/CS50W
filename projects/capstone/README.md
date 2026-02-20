# Soccer captain 

## Motivation

I am a big soccer fan. I play soccer a lot. Before a soccer game, players who signed up for the game need to be splitted into two teams. Randomly splitting the players into two teams is not ideal, because that could lead to an unbalanced game (e.g. one team has all the good players). Therefore, we usually have two captains pick players alternatively in private a few hours before the game starts (we don’t want to do this onsite right before the game starts when everyone is on the field, because we don’t want to make players embarrassed: Imagine how you would feel if you got picked last). Typically, the two captains pick players from the best to the worst alternatively, making the game more balanced.

A conventional way to do this is: Two captains arrange a time, then text each other back and forth the player they want to pick. However, a lot of times a captain has only one phone in his hand and needs to switch between two windows back and forth, one window displays the sign up sheet, and the other window is used to text the other captain the player he picks. Meanwhile, the captain needs to keep track of the players that have already been picked: The captain needs to stare at the sign-up sheet, and remember which players have been picked. Some captains choose to take a screenshot of the sign-up sheet, then use an app to add marks on the names that have been picked. But this introduces the hassle of downloading the app, as well as switching between two colors in the app to mark the players in two teams. Some captains choose to make a phone call while they are picking the players, or use another device (laptop) to avoid switching between two windows, but these are not feasible a lot of times. Therefore in practice, the hassle from the player-picking process sometimes surpasses the fun of being a captain and blueprinting the team for the game.

## Description
In this project, I created a web application to facilitate this player-picking process for captains. Either captain can add players in the web application, either manually or by uploading a screenshot of the sign up sheet. Initially, all the player icons have a green background, located in a “waiting area”. When a captain wants to pick a player, he simply needs to drag the player icon to the left / right side of the screen, and the background color of the icon will become red / blue, indicating a team is assigned to the player. The result is synced to the other captain every second. Therefore, the player-picking process for two captains becomes similar to playing online chess: Each captain makes a move by dragging a player icon to his side (left or right, corresponding to red team or blue team). In the end, each team’s roster will appear on the home page. Either captain can copy and paste them to their soccer game group chat, announcing the team rosters ahead of the game.

## Distinctiveness and Complexity
This project solves a real-life problem that I encounter a lot when being a captain for our soccer team. It contains several features that the other projects in CS50w don’t have, and are rather complex to implement. These features are:
* The “drag and drop” animation using javascript (when a user drags and drops a player icon to assign a player to a team).
* The synchronization among all browser windows, which is important for two captions to view the same current state. This is achieved by “polling”: The javascript code fetches the data from the backend database every second to update the frontend.
* Add players by uploading a screenshot of the sign-up sheet: This is achieved by calling Google GEMINI API. If the API call fails, the pytesseract OCR library in Python will be used instead.
* The positions of the player icons remain fixed relative to the background image when users change the size of the browser window. This is achieved by saving the x, y coordinates of an icon as the percentage of the width and height of the viewport, and the real position of the icon is updated every time the “polling” happens (every second).

## What’s contained in each file I created
`capstone/soccer/staic/soccer/soccer.js`: Javascript code used in this application.
`capstone/soccer/staic/soccer/style.css`: CSS code used in this application.
`capstone/soccer/staic/soccer/images/soccer_field.png`: Background image.
`capstone/soccer/staic/soccer/templates/soccer/index.html`: Home page of the application. It displays the rosters for the two teams. If a user upload a screenshot of a sign-up sheet, it displays that as well.
`capstone/soccer/staic/soccer/templates/soccer/layout.html`: The template for all html files.
`capstone/soccer/staic/soccer/templates/soccer/login.html`: The login page.
`capstone/soccer/staic/soccer/templates/soccer/register.html`: The registration page.
`capstone/soccer/staic/soccer/templates/soccer/team_split.html`: The page for captains to add player icons and drag players into different teams.

`capstone/soccer/utils.py`: utility functions for extracting names from certain screenshots / texts.

Standard files (e.g. manage.py, models.py, etc) in a Django application are not included above.

## How to run the application.
### From local:
1. Create a Python virtual environment (venv)
    * In the project folder (where `manage.py` exists), create a virtual environment and enter it

        `python -m venv venv`

        then 

        `source venv/bin/activate`
2. Install all the dependencies in the `requirements.txt` file
    * `pip install -r requirements.txt`

3. Run the migration
    * `python manage.py migrate`

4. Run `python manage.py runserver` from the terminal. 

Click the “Split into teams” button on the upper left to get started. After adding some players and splitting them into two teams, clicking the “Home” button will show you the roster for each team.

### From the internet:
Simply visit https://zhaoyujian.pythonanywhere.com/ in your browser using a laptop or a mobile phone. I deployed my project there!



## Additional information for CS50w staff
Feel free to play around with this project at https://zhaoyujian.pythonanywhere.com/
If you did, please add a player icon with the name “CS50w staff”, or send me an email: zhaoyujian@ucla.edu. I would appreciate your feedback!

In the future, if time permits, I plan to add more features to the website:
* Save each game event, which contains the roster, the score of the game, and who showed up late for the event.
* Allow captions to upload video recordings of the games to the website, or add links to the video recordings.
* (Ambitious) Persuade my soccer fellows to register on my website, and sign up / withdraw soccer games directly on the website, rather than in our wechat group.

These features would make this project so much cooler… But I think the current state of the project is good enough for the final project of CS50w.
