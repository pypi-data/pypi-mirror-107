import sys
import mkslug


def main() -> None:

    try:
        sentence = sys.argv[1]
    except IndexError:
        raise SystemExit("The sentence must be populated. For example: python -m 'How do you fix a car' in the terminal. Please try again.")

    slug = mkslug.generate(sentence)
    print(f"{slug}")


if __name__ == "__main__":
    main()
