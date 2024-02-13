
# Chess Opening AI Guesser

This is a simple proof-of-concept project based on the idea of recognizing the name of the opening given a chess position.

To my knowledge, different chess openings lead to distinct, characteristic positions. Based on this assumption, it is highly possible to determine the chosen opening based on the characteristics of the given position.

The subtle differences in position, transformations throughout the game, and the complexity of the chess game tree (approximately 10^120 positions according to the [Shannon number](https://en.wikipedia.org/wiki/Shannon_number)) make this task difficult.

For this project, I've used Python with TensorFlow Keras to build an NN architecture based on residual blocks.

## Features

- Gathering opening names and moves from [lichess data](https://database.lichess.org/) files. Warning: primarily focused on data without evaluation and clock. Tested data up to April 2017, especially from January 2013 to January 2017.
- Saving and loading games data in the format of: [opening name, white moves, black moves]
- Visualizing chess games
- Simulating chess games based on game notation and saving random board positions with the name of the played opening from these games to a file.
- Creating and training an NN model based on the proposed architecture. Feeding the NN model with loaded position data files.
- Evaluating trained NN model based on loaded positions data file.
- Trained model in action: possibility of loading games from a file, visualizing them, and using the model to predict the played opening based on the chess board position.


## Screenshots

Showcase application:
![1](https://github.com/amddaa/OpeningAIGuesser/assets/67384782/48822011-1da5-4e5e-9cb5-82182ee544dd)

Visualized auto rollout:
![5](https://github.com/amddaa/OpeningAIGuesser/assets/67384782/8f23af45-7b7d-4b48-9762-de572254a60a)

Model in action (chess visualizer logger - real value, guesser logger - predicted value):
![2](https://github.com/amddaa/OpeningAIGuesser/assets/67384782/01ba1c23-86a4-47c9-839a-38140c2f48ca)
![3](https://github.com/amddaa/OpeningAIGuesser/assets/67384782/d15ca0ff-f830-42a5-894c-622a3f56d5b6)
![4](https://github.com/amddaa/OpeningAIGuesser/assets/67384782/3ebdb293-7f2a-41da-99c8-3ac593cb29c8)


## Installation

***Note: Your installation may vary depending on your system and specs. Below is the installation that is working on Windows 10 with Python 3.10. ML made using AMD GPU - RX 5600 XT - it may be required to change requirements.txt and chess-keras files to enable NVIDIA GPU or CPU usage.***

**1. Copy this repo** 

**2. In the copied repo directory do the following in cmd to setup venv:**

```
python -m venv venv 

.\venv\Scripts\activate

pip install --upgrade pip

pip install -r requirements.txt
``` 
**3. Run with:** 
```
python main.py
```   
## Usage/Examples

***This repo comes with trained 72% acuraccy model and all needed data in the static/ folders.***

For the sake of simplicity I created console application which allows for following actions: 

```
1. Read opening names and moves from lichess data
2. Encode unique opening names and save them to file
3. Load encoded unique opening names from file
4. Encode opening names and moves, save them to file
5. Load encoded opening names and moves from file
6. Run chess visualization based on opening names and moves
7. Run chess rollout based on opening names and move, save random positions to file
8. Create and train model based on saved positions
9. Load and evaluate model based on saved positions
10. Run chess visualization with model usage
```

### Typical use cases

- Reading lichess PGNs and saving the data to the file: 1. and 2. or 4.
- Visualizing read games from PGNs: 5. and 6.
- Rolling out chess positions from PGNs and saving one random position from each game to the file: 5. and 7.
- Creating and training custom model based on random positions: 3. and 8.
- Evaluating model based on random positions: 9.
- Running chess visualization with model usage: 5. and 10.



 
## Results

For this task I've chosen 3 different, very popular openings (opening name, % of popularity on the lichess.org in the 2017-01):
- Italian Game - [3,8%](https://lichess.org/opening/Italian_Game/e4_e5_Nf3_Nc6_Bc4)
- Caro-Kann Defense - [3,0%](https://lichess.org/opening/Caro-Kann_Defense/e4_c6)
- English Opening - [3,1%](https://lichess.org/opening/English_Opening/c4)

I gathered almost 3 million games starting from January 2017 and trained my proposed NN architecture model with them.

My model achieved an average accuracy of 72% on unseen data.
## Conclusion

The model showed a promising ability to determine picked opening based on random chess position. Due to this fact, I am confident that well-trained models can be achieved. Despite the various challenges and shortcuts taken, the AI appears to make reasonable guesses.

#### These are potential areas for further development:

- More than 3 classes - Currently, only 3 classes with somewhat similar popularity have been selected (note that I've used all openings that have a substring of the mentioned above - what about every opening in general, not combined?)
- Multi-label classification rather than multi-class classification (some openings are likely to have many positions in common, some openings have hierarchy)
- More training games - lichess database offers (for the time of writing this) above 5 billions of games, 3 millions are nothing compared to that data. Unfortunately 5 billions are also nothing compared to 10^120  :)
- Better architecture
- Better data input form (currently the position is passed as a one-hot encoded array with the shape of 8x8x2(white, black)x6(every piece) and opening as a index of unique openings - this implies unwanted hierarchy - embedding should help?)
