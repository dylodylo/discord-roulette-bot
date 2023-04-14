import interactions
import pymongo
from interactions import ComponentContext

from database import bets_collection, spins_collection, users_collection
from roulette import spin, winner, ColorEnum


class RouletteCog(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @staticmethod
    def check_wallet(user_id, value):
        wallet_value = users_collection.find_one({"user_id": user_id})["wallet"]
        if value > wallet_value:
            raise Exception("You don't have enough money!")

    async def pre_spin_preparation(self, ctx, bet, value):
        user_id = int(ctx.user.id)
        self.check_wallet(user_id, value)
        spin_number = spins_collection.find_one(sort=[("_id", pymongo.DESCENDING)])
        insert_data = {
            "user_id": user_id,
            "number": bet,
            "value": value,
            "spin_number": spin_number,
        }
        bets_collection.insert_one(insert_data)

        await ctx.send(f"You bet on {bet} with {value} coins")
        users_collection.update_one({"user_id": user_id}, {"$inc": {"wallet": -value}})

        return user_id

    @staticmethod
    async def show_wallet(ctx, user_id):
        wallet_money = users_collection.find_one({"user_id": user_id})["wallet"]
        await ctx.send(f"You have {wallet_money} coins")

    @staticmethod
    async def roulette_spin(ctx: ComponentContext):
        winning_number = spin()
        number, color = winner(winning_number)
        await ctx.send(f"The winner is {number} {color}")
        return number, color

    @interactions.extension_command(
        name="bet_number",
        description="Place a bet on number from 0 to 36 and start spin!",
    )
    @interactions.option(
        min_value=0, max_value=36, description="Number you want to bet on, from 0 to 36"
    )
    @interactions.option(min_value=1, description="Number of coins you want to bet")
    async def roulette_bet_number(self, ctx: ComponentContext, number: int, value: int):
        user_id = await self.pre_spin_preparation(ctx, number, value)
        winning_number, _ = await self.roulette_spin(ctx)

        if number == winning_number:
            await ctx.send(f"You won {value*36} coins")
            users_collection.update_one(
                {"user_id": user_id}, {"$inc": {"wallet": value * 36}}
            )

        else:
            await ctx.send(f"You lost {value} coins")

        await self.show_wallet(ctx, user_id)

    @interactions.extension_command(
        name="bet_color",
        description="Place a bet on color (red or black) and start spin!",
    )
    @interactions.option(
        choices=[
            interactions.Choice(name=color.name, value=color.name)
            for color in ColorEnum
        ],
        description="Color you want to bet on, red or black",
    )
    @interactions.option(min_value=1, description="Number of coins you want to bet")
    async def roulette_bet_color(self, ctx: ComponentContext, color: str, value: int):
        user_id = await self.pre_spin_preparation(ctx, color, value)
        _, winning_color = await self.roulette_spin(ctx)

        if winning_color == color:
            await ctx.send(f"You won {value * 2} coins")
            users_collection.update_one(
                {"user_id": user_id}, {"$inc": {"wallet": value * 2}}
            )

        else:
            await ctx.send(f"You lost {value} coins")

        await self.show_wallet(ctx, user_id)

    @interactions.extension_command(
        name="start_game",
        description="It starts or restarts game and put 100 coins to your wallet",
    )
    async def start_game(self, ctx: ComponentContext):
        user_id = int(ctx.user.id)
        users_collection.replace_one(
            {"user_id": user_id}, {"user_id": user_id, "wallet": 100}
        )

        await ctx.send(
            'You can start game now! '
            'You have 100 coins in your account. '
            'Use "bet_color" or "bet_number" commands to bet and spin roulette!'
        )

    @roulette_bet_color.error
    @roulette_bet_number.error
    async def bet_errors(self, ctx: ComponentContext, error: Exception):
        await ctx.send(str(error))

    @interactions.extension_command(name="help", description="Get help")
    async def help(self, ctx: ComponentContext):
        await ctx.send(
            "It's roulette game. \n"
            "In the beginning you get 100 coins to you wallet. \n"
            "You can make one bet on every spin. Every spin draw number from 0 to 36. \n"
            "Numbers are grouped into colours. \n"
            "Red numbers are: 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, and 36.\n"
            "Black numbers are: 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, and 35 \n"
            "0 is green. \n"
            "You can make bet on number or on color. \n"
            "If you guess color correctly you'll win twice of your bet. \n"
            "If you guess number correctly, you'll win your bet stake multiply by 36! \n\n"
            "To start game write /start_game \n"
            "To bet on number write /bet_number \n"
            "To bet on color write /bet_color \n"
            "Good luck!"
        )


def setup(client):
    RouletteCog(client)
