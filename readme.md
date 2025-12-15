# USD Inspector

This is a simple project aimed at helping me better understand USD's (Universal Scene Description) layer stack and API manipulation. Although similar tools can be found in other software, like houdini's stage inspector, I am focusing on gaining hands-on experience with USD and structuring my code in a way that makes it easier to think in a modular and maintainable way.

## Project Purpose

The main goal of this project is to:

- Deepen my understanding of the USD layer stack.
- Learn how to effectively manipulate USD APIs.
- Apply the Model-View-Controller (MVC) design pattern to create a modular architecture.

By using the MVC model, I am forcing myself to structure the project with separation of concerns, making it easier to maintain, extend, and debug.

## Project Structure

This project is organized using the MVC design pattern:

- **Model**: Manages data and the logic for manipulating USD layer stack and APIs.
- **View**: Responsible for displaying the USD scene or any data to the user.
- **Controller**: Handles user input and updates the Model and View accordingly.