import os
import nltk
from deep_translator import GoogleTranslator
from termcolor import colored, cprint
from tqdm import tqdm


def clear_terminal():
    """Clears the terminal screen based on the operating system."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def print_info():
    """Displays the program information and credits."""
    print('''
┳┳┓  ┓ •  ┏┓•┓     ┏┳┓       ┓
┃┃┃┓┏┃╋┓  ┣ ┓┃┏┓┏   ┃ ┏┓┏┓┏┓┏┃┏┓╋┏┓┏┓
┛ ┗┗┻┗┗┗  ┻ ┗┗┗ ┛   ┻ ┛ ┗┻┛┗┛┗┗┻┗┗┛┛

Created by: Lorenzo Vaz Marzari
github.com/Lovama
@2024
          
────────────────────────────────────────
''')


def get_target_language():
    """Prompts the user to input the target language code."""
    print("\nAvailable language codes can be found here: https://cloud.google.com/translate/docs/languages")
    return input("Enter the target language code (e.g., 'en' for English, 'fr' for French): ")


def main():
    while True:
        retry = 'y'
        while retry.lower() == 'y':
            clear_terminal()
            print_info()
            directory = input("Enter the folder path: ")
            UNDERLINE = '\033[4m'
            RESET_UNDERLINE = '\033[0m'
            formatted_directory = UNDERLINE + \
                colored(directory) + RESET_UNDERLINE

            print(f"\nSelected directory: {formatted_directory}\n")
            if os.path.isdir(directory):
                clear_terminal()
                print_info()
                print(f"\nSelected directory: {formatted_directory}\n")
                break
            else:
                print("The provided directory does not exist.")
                retry = input("Do you want to try again? (y/n): ")

        if retry.lower() != 'y':
            clear_terminal()
            print("Translator Terminated")
            break

        target_language = get_target_language()
        clear_terminal()
        print_info()
        print(f"\nSelected directory: {formatted_directory}\n")
        cprint(
            f"Selected target language: {colored(target_language, attrs=['bold'])}")

        all_files = os.listdir(directory)
        translated_files_count = 0

        for filename in all_files:
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                with open(file_path, "r", encoding="utf-8") as source_file:
                    original_content = source_file.read()

                # Tokenize the content into sentences
                sentences = nltk.tokenize.sent_tokenize(original_content)

                # Display information about the file
                cprint(f"\nOriginal file name: {filename}", "light_yellow")
                cprint(f"Number of sentences: {len(sentences)}", "cyan")

                # Initialize a progress bar
                translated_sentences = []
                with tqdm(total=len(sentences), desc=f"Translating {filename}", unit="sentence", position=0, leave=False) as progress:
                    # Translate each sentence
                    for sentence in sentences:
                        translation = GoogleTranslator(
                            source='auto', target=target_language).translate(sentence)
                        translated_sentences.append(translation)
                        progress.update(1)  # Update progress

                # Write translated sentences to a new file
                translated_filename = f"TRANSLATED_{filename}"
                translated_file_path = os.path.join(
                    directory, translated_filename)
                with open(translated_file_path, "w", encoding="utf-8") as destination_file:
                    for translated_sentence in translated_sentences:
                        destination_file.write(translated_sentence + '\n')

                # Display information about the translated file
                cprint(
                    f"Translated file name: {translated_filename}", "magenta")
                cprint(
                    f"Number of translated sentences: {len(translated_sentences)}", "green")

                translated_files_count += 1

        cprint(f"\n---------------  Files translated: {translated_files_count}  ---------------\n",
               "black", "on_green", attrs=["bold"])

        again = input(
            "Do you want to run the program in another directory? (y/n): ")
        if again.lower() != 'y':
            clear_terminal()
            print("Translator Terminated. Thanks for running the program.")
            break


if __name__ == "__main__":
    main()
