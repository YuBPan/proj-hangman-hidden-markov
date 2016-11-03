# Projest Hangman Game AI
## implemented using Hidden Markov Model

Compilers:
- Python 2.7

Run Instructions:

1. modify following parameters

  ```python
  allow_guess = 5     #[hard code!]
  test_game('test_long.txt', allow_guess)     #[hard code!]
  ```
  ```python
  max_num_words = 5   #[hard code!]
  max_num_sentences = 5 #[hard code!]    
  naive_guess_max_perventage = 0.4  #[hard code!]
  ```
2. run
  ```shell
  python Play.py
  ```


\*Further: implement viterbi algorithm to reduce the run complexity of get_sentences_prob() from dfs's m^n to m\*n, but may expect some accuracy loss

![test_long_allow_guess_10](./test_long_allow_guess_10.png)

![test_long_allow_guess_5](./test_long_allow_guess_5.png)

![test_short_allow_guess_10](./test_short_allow_guess_10.png)

![test_short_allow_guess_5](./test_short_allow_guess_5.png)
