import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Modal, TextInput

class WhisperView(View):
    def __init__(self, sender, target_user, message):
        super().__init__(timeout=None)
        self.sender = sender
        self.target_user = target_user
        self.message = message

    @discord.ui.button(label="Reveal Whisper", style=discord.ButtonStyle.primary)
    async def reveal_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.target_user.id:
            await interaction.response.send_message("This whisper is not for you.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Whisper Revealed",
            color=discord.Color.blue()
        )
        embed.add_field(name="From", value=self.sender.mention, inline=False)
        embed.add_field(name="Message", value=self.message, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

class WhisperModal(Modal, title="Send a Whisper"):
    def __init__(self, target_user, cog_instance):
        super().__init__()
        self.target_user = target_user
        self.cog_instance = cog_instance

    message_input = TextInput(
        label="Your Message",
        style=discord.TextStyle.paragraph,
        placeholder="Type your secret message here...",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        await self.cog_instance.send_whisper_embed(
            interaction, 
            interaction.user, 
            self.target_user, 
            self.message_input.value
        )

class Whispers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_whisper_embed(self, ctx_or_interaction, sender, target, message_content):
        embed = discord.Embed(
            description=f"{target.mention}, you have a whisper from someone!",
            color=discord.Color.default()
        )
        
        view = WhisperView(sender, target, message_content)

        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message("Whisper sent secretly.", ephemeral=True)
            await ctx_or_interaction.channel.send(embed=embed, view=view)
        else:
            await ctx_or_interaction.send(embed=embed, view=view)

    @commands.command()
    async def whisper(self, ctx, member: discord.Member, *, message: str):
        await ctx.message.delete()
        await self.send_whisper_embed(ctx, ctx.author, member, message)

    @app_commands.command(name="whisper", description="Send a secret whisper to a user")
    async def slash_whisper(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.send_modal(WhisperModal(user, self))

async def setup(bot):
    await bot.add_cog(Whispers(bot))
