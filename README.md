# Quiz Application

This is a simple quiz application with three different versions, each using a different way to store data.

## Versions Available

### 1. Program Memory Storage (quiz_app_program_memory)
- Stores all data in computer's memory while the program runs
- Data is lost when you close the program
- Fastest but temporary storage
- Good for testing and learning

### 2. File Storage (quiz_app_files)
- Stores data in text files:
  - users.txt: stores usernames and passwords
  - scores.json: stores quiz scores and history
- Data stays saved even after closing the program
- Easy to understand and view data
- Good for small applications

### 3. Database Storage (quiz_app_database)
- Uses SQLite database to store data
- Data stays saved even after closing the program
- More organized way to store data
- Good for handling lots of users and scores

## Features in All Versions
- User signup and login
- Three types of quizzes:
  1. Math Quiz (random questions)
  2. Science Quiz (multiple choice)
  3. History Quiz (multiple choice)
- View score history
- Password protection for users

## How to Run
1. Choose which version you want to use
2. Go to that folder
3. Run the program:   ```
   python quiz.py   ```

## Requirements
- Python 3.x
- No extra installations needed

## Note
Each version works the same way but stores data differently. Choose the version that best fits your needs:
- Memory Storage: For practice and testing
- File Storage: For simple use
- Database Storage: For more organized data storage 