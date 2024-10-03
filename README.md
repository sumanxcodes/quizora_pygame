
# Quizora Pygame

Quizora is a Python-based educational quiz game built using Pygame and pygame_gui. The game allows users to interact with a GUI interface and provides functionalities for different screens, such as login/logout, playing quizzes, leaderboard and tracking progress.

## Features

- **Menu Screen**: The game includes a dynamic menu screen where users can login, start the game, access leaderboard, track progress, or quit.
- **Quiz Play**: Play multiple-choice quizzes with different levels of difficulty.


## Requirements

To run Quizora Pygame, you need to have Python 3.12.x and Pygame installed on your system. All required packages are listed in `requirements.txt`.

- Python 3.12.x
- Pygame 2.6.1 or higher
- pygame_gui 0.6.0 or higher

### Install Required Libraries

To install the necessary packages, run:

```bash
pip install -r requirements.txt
```

## Project Structure

```
├── assets
│   ├── data
│   ├── fonts
│   │   ├── PressStart2P-Regular.ttf
│   └── images
│       └── dino
├── src
│   ├── ui
│   ├── main.py
│   ├── settings.py
│   └── theme.json
├── .gitignore
├── requirements.txt
└── README.md
```

### Setup

1. Clone the repository to your local machine:
   ```bash
   git clone git@github.com:sumanxcodes/quizora_pygame.git
   cd quizora_pygame
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv quizora_game_env
   source quizora_game_env/bin/activate  # On Windows: quizora_game_env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:
   ```bash
   python src/main.py
   ```

## Troubleshooting

- **Missing Dependencies**: Ensure all packages from `requirements.txt` are installed.
  ```bash
  pip install -r requirements.txt
  ```

- **Module Not Found Error (for assets)**: Ensure that the path to your assets directory is correctly referenced in your `theme.json` and other parts of the code.

## Customizing Fonts

The game allows for custom font integration via `theme.json`. If you want to add a new font, follow these steps:

1. Add your font `.ttf` file to the `assets/fonts/` directory.
2. Update the `theme.json` file to reference the new font:
   ```json
   {
       "font": {
           "name": "YourFontName",
           "size": 16,
           "regular_resource": {
               "package": "assets.fonts",
               "resource": "YourFontFile.ttf"
           }
       }
   }
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


