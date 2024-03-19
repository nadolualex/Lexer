# Lexer Implementation in Python

This project implements a lexer in Python, which is capable of dividing a string of characters into lexemes based on a provided specification. The lexer is implemented using regular expressions, NFA (Nondeterministic Finite Automaton), and DFA (Deterministic Finite Automaton) concepts.

## Project Structure

- **Regex**: A class to represent regular expressions and handle related operations.
- **NFA**: A class to represent Nondeterministic Finite Automaton and related operations.
- **DFA**: A class to represent Deterministic Finite Automaton and related operations.
- **Lexer**: A class responsible for lexing a given input string based on a provided specification.

## Lexer Class

The Lexer class has a constructor that takes a specification as a parameter. The specification is a list of tuples, where each tuple contains a token name and its corresponding regular expression.

The class contains a method called `lex` which takes a string as input and returns the result of lexing in the form of a list of tuples `[token, lexeme]`. If lexing is successful, it returns a list of tuples representing tokens and their corresponding lexemes. In case of an error, it returns a list with a single element in the format `("", "No viable alternative at character _, line _)`. 

### Error Handling

Lexical errors may occur due to incorrect/incomplete configuration or invalid input. Error messages include the line and column where the lexing failed, aiding the programmer in debugging.

- If the lexer encounters an invalid character and cannot accept it, it displays an error message indicating the character index and line.
- If the lexer reaches the end of input without accepting any lexeme, and neither reaches a sink state nor a final state, it displays an error message indicating EOF (end of file) character and line.

## Example

Suppose we have the following specification:

```python
spec = [("TOKEN1", "abbc*"), ("TOKEN2", "ab+"), ("TOKEN3", "a*d")]
```

And the input string is `"abbd"`. Lexical analysis will stop at the character 'd' since the lexer will reach a sink state. The longest substring satisfying both `TOKEN1` and `TOKEN2` is `"abb"`, and `TOKEN1` will be reported since it precedes `TOKEN2` in the specification. Afterwards, the lexer will advance by one character in the input and identify the substring `'d'` as `TOKEN3`.

