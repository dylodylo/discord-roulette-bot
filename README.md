# DISCORD ROULETTE BOT

## How to install bot
1. Download repository.
2. Create .env file.
3. Paste in .env file:
```
BOT_TOKEN=<your_bot_token>
DATABASE_HOST=<your_mongo_database_host>
DATABASE_PORT=<database_port> 
```
4. In your terminal run `pip install -r requirements.txt`
5. In terminal run `python main.py`
6. Write `/help` in chat to get know how to play.

## Documentation

### RouletteCog methods

- `check_wallet(user_id, value)`

    `user_id [int]` - Id of user

    `value [int]` - Number of coins bet by user

    Method checks if user has enough coins in wallet to place a bet. Raise error if they don't.


- `pre_spin_preparation(self, ctx, bet, value)`

    `ctx [ComponentContext]` - Component context

    `bet [int/string]` - Bet of user. Can be int (number) or string (color).
    
    `value [int]` - Number of coins bet by user

    Method retrieves `user_id`, run `check_wallet` function. After calculate number of the spin and put data about bet to database. In the end subtract from user's wallet `value` amount of coins and print user's bet.

    Return: `user_id [int]`


- `show_wallet(ctx, user_id)`

    `ctx [ComponentContext]` - Component context
    
    `user_id [int]` - Id of user
    
    Prints in chat current state of user's wallet.


- `roulette_spin(ctx)`

    `ctx [ComponentContext]` - Component context
    
    Makes roulette spin. Returns winning number and winning color.
    
    Return: `number [int]`, `color[str]`


- `roulette_bet_number(self, ctx, number, value)`

    `ctx [ComponentContext]` - Component context
    
    `number [int]` - Number on which user bet
    
    `value [int]` - Number of coins bet by user
    
    Discord command which allows user to place bet on number. Makes spin and checks if user won. Show proper prompt in chat and makes changes in user's wallet in database. In the end show to user their wallet.


- `roulette_bet_color(self, ctx, color, value)`

    `ctx [ComponentContext]` - Component context
    
    `color [str]` - Coloro on which user bet
    
    `value [int]` - Number of coins bet by user
    
    Discord command which allows user to place bet on color. Makes spin and checks if user won. Show proper prompt in chat and makes changes in user's wallet in database. In the end show to user their wallet.


- `start_game(self, ctx)`

    `ctx [ComponentContext]` - Component context

    Command which change user's `wallet` value in database to 100 or create new document in database, if user has never played before. After print prompt in chat with information for user.


- `bet_errors(self, ctx, error)`

    `ctx [ComponentContext]` - Component context

    `error [Exception]` - Raised error
    
    Handle error from `check_wallet` function and print information to user.


- `help(self, ctx)`

    `ctx [ComponentContext]` - Component context
    
    Command which print to user rules of the game and available commands.

### Database

- `initialize_database()`

    Initializes database. Put document in `spins_collection` what will allow to track spins.


### Bot

- `initialize_bot()`

  Initializes bot. Need `.env` file. Load commands and print `BOT IS ACTIVE` after bot started.


### Roulette

- `spin()`

  Draw random number from 0 to 36. Save spin in database. Returns drawn number.
  
  Return: `winning_number [int]`


- `winner(number)`

  Connect winning number with its color.
  
  Return: `winning_number [int]`, `color [str]`