# Typing Speed Tester

A Python-based desktop application that helps users practice typing
and measure their typing speed, accuracy, and performance.

The application provides different difficulty levels, a 60-second
typing test, performance tracking, graphs, PDF reports, sound effects,
and light/dark themes.

## 🚀 Features

- User login with username
- 60-second typing test
- Easy, Medium, and Hard difficulty levels
- Randomly generated typing sentences
- Typing speed calculation in WPM
- Typing accuracy calculation
- Performance score out of 100
- Automatic score history saved in CSV format
- Typing speed progress graph
- Export typing history as a PDF report
- Countdown sound effects
- Enable/disable sound effects
- Light and Dark theme
- Logout functionality
- About section

## 🛠️ Technologies Used

- Python
- Tkinter
- Pandas
- Matplotlib
- CSV
- FPDF
- Pygame
- Threading

## 📋 Difficulty Levels

| Level | Words |
|-------|-------|
| Easy | 20 words |
| Medium | 40 words |
| Hard | 60 words |

Each typing test runs for a maximum of 60 seconds.

## 📊 Performance Calculation

The application displays:

- **Time Taken** – Time required to complete the test
- **Speed** – Typing speed calculated in Words Per Minute (WPM)
- **Accuracy** – Percentage of correctly typed words
- **Score** – Performance score based on typing speed

### Score System

| Typing Speed | Score |
|--------------|-------|
| 60+ WPM | 100 |
| 40–59 WPM | 80 |
| 20–39 WPM | 60 |
| Below 20 WPM | 40 |

## 💾 Score History

After completing a test, the application saves the following information:

- Date and time
- Typing speed
- Accuracy
- Score

The data is stored in a CSV file using the username entered during login.

## 📈 Performance Graph

Users can view their typing-speed progress through a graph.

The graph displays the user's recent typing speed in WPM over time.

## 📄 PDF Report

The application can generate a PDF report containing:

- Date and time
- Typing speed
- Accuracy
- Score

The report is saved as a PDF file using the user's username.

## 🔊 Sound Effects

The application provides countdown sound effects during the final
seconds of the typing test.

Sound effects can be enabled or disabled from the View menu.

## 🎨 Themes

The application supports:

- Light Theme
- Dark Theme

Users can switch between themes from the View menu.

## 📁 Project Structure

```text
my-first-repository/
│
├── typing_speed_tester_full.py
├── uma maheshwari_scores.csv
└── README.md
