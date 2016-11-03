from LocalGameClient import GameClient
from GameSolution import GameSolution

def test_game(test_file_name, allow_guess):

    # Init game client and solution
    solution = GameSolution(allow_guess)
    client = GameClient()
    total_count, test_sentences = load_test_sentences(test_file_name)
    win_count = 0

    for i in range(0, total_count):
        print '/----------------------------------------'
        solution.init()
        result = play_game(client, solution, test_sentences[i], allow_guess)
        if result == 'WIN':
            win_count += 1
        print '\________________________________________'
    print "Accuracy:\twin:{0}\ttotal:{1}\tpercentage:{2:.4f}%".format(win_count, total_count, 1.0 * win_count / total_count * 100)

def play_game(client, solution, full_string, allow_guess):
    result = client.create_game(full_string, allow_guess)
    if result['status'] == 'ERROR':
        print "Init error"

    # Game running
    while result['status'] == 'ONGOING':
        print '/---'
        letter = solution.get_guess_letter(result['str'], result['remain'])
        print "[Guess]\t", letter
        result = client.guess(letter)
        print "[Result]\t", result
        print '\___'

    # Game terminated
    print result
    return result['status']

def load_test_sentences(fileName):
    total_count = 0
    f = open(fileName, 'r')
    test_sentences = []
    for line in f:
        if line.strip() != "":
            total_count += 1
            test_sentences.append(line.lower())
    return total_count, test_sentences

if __name__ == "__main__":
    allow_guess = 5     #[hard code!]
    test_game('test_long.txt', allow_guess)     #[hard code!] 
    print "Test Terminated given allow_guess:%d" % allow_guess
