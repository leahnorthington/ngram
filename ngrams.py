from random import choice, random
from nltk import word_tokenize
import argparse
import sys

def get_counts(context_length, training_text):
    """
    This function counts the frequencies of all continuations of each context tuple
    :param context_length: Integer, number of tokens preceding current token (use 2 for trigrams)
    :param training_text: The training data as one big string
    :return: counts: A dictionary of context tuples to dictionaries of continuation probabilities
    """

    counts = {}

    tokens = word_tokenize(training_text)
    for i in range(len(tokens) - context_length):
        context = []
        next_token = tokens[i + context_length]

        if next_token == "Dickens":
            #a=5
            pass

        for j in range(context_length):
            context.append(tokens[i + j])

        # Add 1 to frequency or create new dictionary item for this tuple
        if tuple(context) in counts:
            if next_token in counts[tuple(context)]:
                counts[tuple(context)][next_token] += 1
            else:
                counts[tuple(context)][next_token] = 1
        else:
            counts[tuple(context)] = {next_token: 1}

    return counts

# END FUNCTION GET_COUNTS


def generate_from_file(context_length, training_file, output_length=60):

    # Open the training file
    with open(training_file, 'r') as f:
        training_data = f.read()

    counts = get_counts(context_length, training_data)

    if starter is not None:
        initial = tuple(starter)
        if initial in counts:
            first_tokens = initial
        else:
            first_tokens = choice(list(counts.keys()))  # Choose a random first context

            if initial[-1] == '.':
                inString = " ".join(initial).replace(" .", ".")
                # print("You already have a period!")
                print(inString + " ", end='')
            elif initial[-1] == '!':
                inString = " ".join(initial).replace(" !", "!")
                # print("You already have an exclamation!")
                print(inString + " ", end='')
            elif initial[-1] == '?':
                inString = " ".join(initial).replace(" ?", "?")
                # print("You already have a question mark!")
                print(inString + " ", end='')
            else:
                inString = " ".join(initial)
                print(inString + '. ', end='')
    else:
        first_tokens = choice(list(counts.keys()))  # Choose a random first context

    output_list = list(first_tokens)
    current_context = tuple(first_tokens)

    for i in range(output_length):
        next_context = max(counts[current_context], key=(counts[current_context].get))
        temp = list(current_context)
        temp.pop(0)  # Remove first token in previous context
        temp.append(next_context)  # Add new token for the next context
        next_token = temp[-1]
        next_context = tuple(temp)

        current_context = next_context

        output_list.append(next_token)

    punctuation = {'.', '?', '!'}
    if output_list[-1] not in punctuation:
        output_list.append('.')

    finalOut = " ".join(output_list)
    finalOut = finalOut.replace(' ? ', '? ').replace(' : ', ': ').replace(' , ', ', ').replace(' \' ', '\'').replace(' ! ', '! ').replace(' . ', '. ').replace(' ; ', '; ').replace(' \" ', '\"')

    print(finalOut)


# END FUNCTION GENERATE_FROM_FILE


parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument('--starter', action="store", dest="input", help="Word to begin ngram.")

options = parser.parse_args()

starter = options.input

if starter is not None:
    starter = starter.lower()
    # print(starter)
    starter = word_tokenize(starter)

punctuation = {'.', '?', '!'}

if starter is not None:
    if len(starter) != 2:
        if len(starter) < 2:
            print("Input length is too short!")
            sys.exit()
        elif len(starter) == 3:
            if starter[-1] in punctuation:
                pass
        elif starter[-1] in punctuation:
            print("Your input is too long! Removing the following words:")
            x = 0
            while len(starter) > 3:
                print(starter[x])
                starter.pop(x)
                x += x
            print("Input length is now correct. Beginning to generate bigram.")
        else:
            print("Your input is too long! Removing the following words:")
            x = 0
            while len(starter) > 2:
                print(starter[x])
                starter.pop(x)
                x += x
            print("Input length is now correct. Beginning to generate bigram.")

generate_from_file(2, options.file)


