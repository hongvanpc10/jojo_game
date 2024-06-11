# Game JOJO

## Demo

![Demo](assets/images/demo.gif)

## Features

-   Player can move left, right, jump, dash, and attack with a gun to kill enemies and destroy obstacles.
-   Shoot to barrels to explode them and kill enemies around. Note that the explosion can also hurt the player.
-   Collect life potions to recover health.
-   Increase score by killing enemies.
-   Enemy portal will spawn enemies continuously, and the player can destroy the portal to stop the spawn.
-   Create custom levels with Tiled Map Editor.
-   Save and load game progress.
-   Music and sound effects.
-   Cross-level game play.

## Installation

1.  Clone the repository.

```bash
git clone https://github.com/hongvanpc10/jojo_game.git
```

Or download the zip file from the repository.

2.  Install the required packages.

```bash
pip install -r requirements.txt
```

If using `venv`, activate the environment before installing the packages.

3.  Run the game.

```bash
python main.py
```

## Usage

### Play the game

1. Run the game.

```bash
python main.py
```

2. Controls:

-   When in menu:
    -   Use arrow keys to navigate.
    -   Press `enter` to select.
-   Use arrow keys to move left, right, and jump.
-   Press `C` to dash.
-   Press `X` to shoot.
-   If on ladder, use arrow keys to move up and down.
-   Press `esc` to pause the game during play.

3. Rules:

-   The player initially has 1 live.
-   The player will lose a live if killed by an enemy or an explosion or fall off the map.
-   The player will lose the game if all lives are lost.
-   The player can recover health by collecting life potions.
-   The player can kill enemies by shooting them.
-   The player can destroy obstacles by shooting them.
-   The player can destroy enemy portals by shooting them.
-   The player can increase score by killing enemies.

### Create custom levels

1. Run editor.

```bash
python editor.py
```

2. Controls:

-   Use keys `a`, `s`, `d`, `w` to move the camera.
-   At the top left conner of the screen, there is a image of the current tile. Scroll the mouse wheel to change the current tile, shift + scroll to change the tileset.
-   Click on the map to place the current tile at the clicked position.
-   Right click on the map to remove the tile at the clicked position.
-   Press `o` to save the map to a file.
-   Press `t` to auto-tiling the map.

3. Notes:

-   A map must have only one player spawn tile, one skull tile (end of the level).

### Load custom levels

1.  Create a map with Tiled Map Editor and save it to a file.

2.  Put the map file in the `maps` folder.
    After created the map, the map file will be placed at root folder with the name `map.json`. To load the map, put it in the `data/maps` folder and rename it due to the position of the map in the game (fist map is `0.json`).

3.  Run the game and play.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
