# on_button_click -> ボタン検知
# on_select_click -> セレクト検知
# splitしてるのはなぜ？ -> message.idとかをcustom idに入れてるからそれを引き抜くため

import discord
from discord.ext import commands


def setReason(reasonid: str):
    """通報内容の理由をIDから設定する"""

    if (reasonid == "dont-like"):
        return "内容が気に入らない"
    elif (reasonid == "harass"):
        return "脅迫と思える内容"
    elif (reasonid == "nsfw"):
        return "暴力的・卑猥な内容"
    elif (reasonid == "exposing-information"):
        return "個人情報の漏洩"
    else:
        return "❓設定理由が見つかりません"


class EventListener(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        try:
            if interaction.data['component_type'] == 3:
                await on_select_click(interaction)
            elif interaction.data['component_type'] == 2:
                await on_button_click(interaction)

        except KeyError:
            pass


async def on_button_click(interaction: discord.Interaction):
    custom_id = interaction.data["custom_id"]
    split = custom_id.split(".")


async def on_select_click(interaction: discord.Interaction):
    custom_id = interaction.data["custom_id"]
    values = interaction.data["values"]
    split = custom_id.split(".")

    if (split[0] == "reportuser"):
        if (len(split) == 2):
            await interaction.response.defer()

            try:
                message = await interaction.channel.fetch_message(split[1])
            except (discord.Forbidden, discord.NotFound, discord.HTTPException):
                await interaction.edit_original_response(content="エラーが発生しました。", embed=None, view=None)
                return

            reason_id = values[0]
            reason = setReason(reason_id)

            partialmsg = interaction.channel.get_partial_message(int(split[1]))

            embed = discord.Embed(description=f'メッセージ送信者: {message.author.mention}\nメッセージURL: {partialmsg.jump_url}\n \n```{message.content}```\n \n通報理由: {reason}', color=0x242429)

            view = discord.ui.View()
            button = discord.ui.Button(label="通報する", style=discord.ButtonStyle.danger, custom_id=f'report.{message.id}.{interaction.user.id}.{reason_id}')

            view.add_item(button)

            await interaction.edit_original_response(content="以下の内容で通報します。よろしいですか？\n`もし通報しない場合はこのメッセージを削除してください。`", embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(EventListener(bot))
