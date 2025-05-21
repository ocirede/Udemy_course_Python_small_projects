## **Python Small Projects**  

### **Projects Overview**  

This repository contains a collection of small Python projects, each designed to help me practice and learn different aspects of Python programming. The projects include a mix of object-oriented programming (OOP), game development, and graphical applications using libraries like Turtle, Tkinter, or Pandas.  

### **1. Happy Birthday Letter Generator**  
- **Description**: This project automates the process of generating personalized birthday letters. It reads a starting template letter from a file and a list of names from another file, replacing the placeholder `[NAME]` with the actual recipient's name. The personalized letters are saved into individual files for each recipient.  
- **Skills Learned**: File reading and writing, string manipulation, automating repetitive tasks.  

### **2. Birthday Automated Mail with SMTP**  
- **Description**: This project automates the process of sending personalized birthday emails using SMTP. It reads a template letter from a file and a list of names from another file, replacing the placeholder `[NAME]` with the actual recipient's name. It then checks if the current date matches a birthday and sends a personalized email to that person. The email is sent via Gmail's SMTP server.  
- **Skills Learned**: File reading and writing, string manipulation, automating repetitive tasks, working with SMTP and environment variables, sending emails programmatically.  

### **3. Coffee Machine OOP**  
- **Description**: A simple coffee machine built using object-oriented programming (OOP) principles. This project simulates a coffee machine that can make various types of coffee, handle user input, and track resources like water, coffee beans, and milk. It calculates the money received and gives change if necessary.  
- **Skills Learned**: OOP, class and object management, input handling.  

### **4. NATO Alphabet Converter**  
- **Description**: Translates user-input words into their NATO phonetic alphabet equivalents (e.g., "A" → "Alpha"). Uses dictionary mapping and input validation.  
- **Skills Learned**: Dictionary usage, string manipulation, error handling.  

### **5. Paint Hacking (Using Turtle)**  
- **Description**: Creates random dot patterns using Python's Turtle graphics library.  
- **Skills Learned**: Turtle graphics, randomization.  

### **6. Pomodoro Timer**  
- **Description**: Implements the Pomodoro Technique with work/break intervals and session tracking using Tkinter.  
- **Skills Learned**: Tkinter GUI, time management, UI updates.  

### **7. Pong Arcade Game**  
- **Description**: Classic Pong game implementation using Turtle.  
- **Skills Learned**: Game development, collision detection.  

### **8. Quiz Game**  
- **Description**: Text-based multiple-choice quiz with scoring system.  
- **Skills Learned**: User input handling, conditionals.  

### **9. Rock, Paper, Scissors Game**  
- **Description**: CLI implementation of the classic game against computer AI.  
- **Skills Learned**: Randomization, game logic.  

### **10. Snake Game**  
- **Description**: Classic Snake game using Turtle graphics.  
- **Skills Learned**: Game loops, collision detection.  

### **11. Turtle Crossing Road Game**  
- **Description**: Turtle must cross a road with moving cars (Turtle graphics).  
- **Skills Learned**: Event handling, collision detection.  

### **12. US States Game**  
- **Description**: Geography quiz that plots guessed US states on a Turtle graphics map.  
- **Skills Learned**: Pandas data handling, Turtle graphics.  

### **13. Flash Card Game (German-English Translation)**  
- **Description**: Tkinter-based flashcard app for language learning with:  
  - German-English word pairs  
  - Flip animation with delayed translation  
  - Progress tracking (known/unknown words)  
  - Data persistence (CSV or JSON)  
- **Skills Learned**: Tkinter GUI, event binding, file I/O, dictionary manipulation  

### **14. Flight Search with Amadeus and Twilio API**  
- **Description**: This project integrates the Amadeus API to search for flights based on origin, destination, and price. The system automatically manages access tokens, searches for flight offers, and parses the results to extract flight segments and pricing information. Once a flight match is found, the application formats the flight details and sends them as a text message via the Twilio SMS API.  
- **Skills Learned**: REST API integration (Amadeus), access token management, JSON parsing, working with datetime and IATA codes, automated messaging with Twilio, environment variable handling.

### **15. Password Manager Project**  
- **Description**: Tkinter GUI for generating/storing passwords with clipboard support.  
- **Skills Learned**: Tkinter widgets, encryption basics, clipboard integration.  

### **16. Stock News Notifier**  
- **Description**: This project fetches the latest stock data for Bitcoin and analyzes its price change from the previous day. If the price change exceeds 5%, the script fetches relevant news articles and sends them as a text message (via Twilio) to a specified phone number. The message includes a summary of the price change and a headline from the latest news related to Bitcoin.  
- **Skills Learned**: API interaction (Alphavantage, NewsAPI), data manipulation, Twilio integration for SMS, working with environment variables.  

## **Requirements**  
```sh
pip install -r requirements.txt
