# Pivo-Slayer: User Stories


## Core goals
As a user, I want to...

| Theme | As a ...| ...I want to... | ...so that...| Priority | Status | SQL |
|-|-|-|-|-|-|-|
| Accounts & signing up  | User | I want to be able to create a user account and sign in with it | I can begin adding bank accounts and transactions | Required | Done |
| Accounts & signing up  | System developer | I want be sure that the system uses password hashing | I can protect users from the dangers of database leaks | Required | Done 13.6. |
| Accounts & administration  | Admin | See a summary of the number of users on the service | I can validate my development progress | Required | Done |
| Business / Core | User | Create a bank account | I can have my transactions sorted by account | required | Done |
| Business / Core | User | Create and add transactions to each account | Inspect my transactions by account and analyze spending | Required | Done |
| Business / Core | User | See my current account balance, calculated from transactions | See how much money I have | Required | Done |
| Business / Core | User | Set categories for my transactions | I can analyze which types of spending dominate my cash flows | Required | Done |
| Business / Core | User | See a summary of my transactions per category for the current month, current year, and for all time | I can see what I'm spending money on | Required | Done | E.g. `SELECT sum(transact.amount) AS amount, category.name, category.id FROM transact LEFT JOIN category ON transact.category_id = category.id WHERE ((transact.credit_or_debit = :credit_or_debit AND transact.bankaccount_id = :bankaccount_id) AND  (transact.booking_date BETWEEN :start_date AND :end_date)) GROUP BY category.id, category.name ORDER BY category.name` |
| Business / Core | User | Automatically update the category for all transactions of the same type (Credit vs debit) with a counterparty when I set a category for one transaction (I want to choose whether all should be updated) | I can categorize transactions more easily and semi-automatically | Required | Won't do |
| Business | User | Have a default category set for new transactions in the case of pre-existing transactions with the same counterparty | Categorization is effortless | Required | Won't do |
| Security | User | Be sure my transactions are not shown to other users | I can trust the login system | Required | Done |
| Business| User | Import an official bank statement (OP or Nordea) for automatically submitting and categorizing my transactions | I don't need to import transactions manualy | Stretch | Won't Do |
| Business | User | Set any transaction as a recurring transaction (monthly only) | I can anticipate parts of my income and expenditure | Stretch | Won't Do |
| Business | User | See a projection of my bank account's balance based on average daily expenses and known recurring transactions | I can make estimate the amount of money on my bank account for the next 2-4 weeks | Stretch | Won't Do |