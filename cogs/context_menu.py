import discord
from discord.ext import commands
from discord import app_commands


class ContextMenu(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="通報する",
            callback=self.send_msg
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def send_msg(self, interaction: discord.Interaction, message: discord.Message) -> None:

        embed = discord.Embed(description="通報内容を以下の選択肢から選んでください。", color=0x26262a)
        options = discord.ui.Select(
            custom_id=f'reportuser.{message.id}',
            options=[
                discord.SelectOption(label="内容が気に入らない", value="dont-like"),
                discord.SelectOption(label="脅迫と思える内容", value="harass"),
                discord.SelectOption(label="暴力的・卑猥な内容", value="nsfw"),
                discord.SelectOption(label="個人情報の漏洩", description="通報するユーザー自身の情報も対象となる", value="exposing-information")
            ],
            placeholder="こちらから選択してください"
        )

        view = discord.ui.View()
        view.add_item(options)

        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(ContextMenu(bot))
