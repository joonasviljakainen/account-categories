# Pivo-Slayer

This is an application intended to serve as the course project for tsoha 
at HYY.

The application is available (without any features) at [https://pivo-slayer.herokuapp.com/](https://pivo-slayer.herokuapp.com/).

## Purpose

I am going to slay Pivo. You took everything from me. All of my categories... gone.

Pivo-Slayer is a database app that will allow users to import account transactions and set categories for them.

The aim is to allow category-based spending analysis on a monthly and/or weekly basis to help users understand their cash flow and plan their personal economy.

### Testing

Create a new user profile if you would like to start from stratch, or use the following credentials:

| Attribute | Value |
|:-|:-|
| Username | jones |
| Password | jones |

Or you can check out the admin features, currently very basic:

| Attribute | Value |
|:-|:-|
| Username | admin |
| Password | admin |

### User stories

See [User stories](/documentation/stories.md).

### Installation & Use

You need to have Python 3 and Pip installed.

clone the repository and navigate to the root directory of the app.
`git clone https://github.com/joonasviljakainen/account-categories.git`

Install dependencies:
`pip install -r /path/to/requirements.txt`

Activate virtual environment:
`source venv/bin/activate`

Run the application:
`python3 run.py`

Now navigate to `localhost:5000`.

[Instructions for use](/documentation/instructions.md)

### Database architecture

See [Database Architecture](/documentation/databaseArchitecture.md)
