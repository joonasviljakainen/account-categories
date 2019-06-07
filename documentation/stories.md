# Pivo-Slayer: User Stories


## Core goals
As a user, I want to...

| Theme | As a ...| ...I want to... | ...so that...| Priority | Status |
|-|-|-|-|-|-|
| Accounts & signing up  | User | I want to be able to create a user account and sign in with it | I can begin adding bank accounts and transactions | Required | In Progress |
| Accounts & administration  | Admin | See a summary of the number of users on the service (and clear the database given Heroku's row limitation) | I can validate my development progress and manage the application | Required | To Do |
| Business / Core | User | Create a bank account | I can have my transactions sorted by account | required | In Progress |
| Business / Core | User | Create and add transactions to each account | Inspect my transactions by account and analyze spending | Required | In Progress |
| Business / Core | User | See my current account balance, calculated from transactions | See how much money I have | Required | Done |
| Business / Core | User | Set categories for my transactions | I can analyze which types of spending dominate my cash flows | Required | In Progess (category table created) |
| Business / Core | User | See a summary of my transactions per account by week, month, day, year | I can see if I'm spending more than I earn | Required | To Do |
| Business / Core | User | See a summary of my transactions per category by week, month, day, year | I can see what I'm spending money on | Required | To Do |
| Business / Core | User | Automatically update the category for all transactions of the same type (Credit vs debit) with a counterparty when I set a category for one transaction (I want to choose whether all should be updated) | I can categorize transactions more easily and semi-automatically | Required | To Do |
| Business | User | Have a default category set for new transactions in the case of pre-existing transactions with the same counterparty | Categorization is effortless | Required | To Do|
| Security | User | Be sure my transactions are not shown to other users | I can trust the login system | Required | To Do|
| Business| User | Import an official bank statement (OP or Nordea) for automatically submitting and categorizing my transactions | I don't need to import transactions manualy | Stretch | To Do |
| Business | User | Set any transaction as a recurring transaction (monthly only) | I can anticipate parts of my income and expenditure | Stretch | To Do |
| Business | User | See a projection of my bank account's balance based on average daily expenses and known recurring transactions | I can make estimate the amount of money on my bank account for the next 2-4 weeks | Stretch | To Do |