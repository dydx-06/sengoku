import discord
from discord.ext import commands

class Carpool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ride_messages: dict[int, dict] = {}

    @commands.command()
    async def newride(self, ctx, destination: str, date: str, t: str, total: int):

        embed = discord.Embed(title=f"Ride by {ctx.author.display_name}")
        embed.add_field(name="Destination", value=destination, inline=True)
        embed.add_field(name="Date", value=date, inline=True)
        embed.add_field(name="Time", value=t, inline=True)
        embed.add_field(name="Seats", value=f"0/{total}", inline=True)

        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")

        self.ride_messages[message.id] = {
            "seats_total": total,
            "seats_booked": 0,
            "message": message,
            "users": set()
        }

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        message_id = reaction.message.id
        if reaction.emoji != "✅":
            return

        if message_id in self.ride_messages:
            ride = self.ride_messages[message_id]

            if user.id in ride["users"]:
                return
            if ride["seats_booked"] >= ride["seats_total"]:
                await reaction.message.channel.send(f"Sorry {user.mention}, this ride is full!")
                return

            ride["seats_booked"] += 1
            ride["users"].add(user.id)

            embed = reaction.message.embeds[0]
            for i, field in enumerate(embed.fields):
                if field.name == "Seats":
                    embed.set_field_at(i, name="Seats", value=f"{ride['seats_booked']}/{ride['seats_total']}", inline=True)
                    break
            await ride["message"].edit(embed=embed)

def setup(bot):
    bot.add_cog(Carpool(bot))
