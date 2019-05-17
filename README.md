# Pivoslayer

This is an application intended to serve as the course project for tsoha 
at HYY.

The application is available (without any features) at [https://pivo-slayer.herokuapp.com/](https://pivo-slayer.herokuapp.com/).

## Purpose

I am going to slay Pivo. You took everything from me. All of my categories... gone.

Account-Categories is a database app that will allow users to import 
account transactions (sadly, manually) and set categories for them. The 
application will apply the category to all transactions from the same 
counterparty, except in the case where the transaction has an 
individually set category. 

The user will be able see their spending and income per month, and 
compare spending month-by-month.

Transaction imports will be manual, and assuming different banks offer 
different formats, a maximum of two banks will be supported. 

A user may have several accounts.

### Preliminary database graph

![diagram](/documentation/transactionApp.png)
