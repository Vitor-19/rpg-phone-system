import discord
from discord import app_commands


PHONE_ROLE_NAME = "Has Phone"
GM_ROLE_NAME = "Phone GM"
LOG_CHANNEL_NAME = "phone-log"


def setup_phone(bot: discord.Client):

    # -------- SETUP AUTOMÁTICO --------
    @bot.tree.command(description="Setup the RPG Phone System (admin only).")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_phone_system(interaction: discord.Interaction):

        guild = interaction.guild

        # ---- roles ----
        phone_role = discord.utils.get(guild.roles, name=PHONE_ROLE_NAME)
        if not phone_role:
            phone_role = await guild.create_role(name=PHONE_ROLE_NAME)

        gm_role = discord.utils.get(guild.roles, name=GM_ROLE_NAME)
        if not gm_role:
            gm_role = await guild.create_role(
                name=GM_ROLE_NAME,
                permissions=discord.Permissions(manage_roles=True)
            )

        # ---- channel (PRIVATE GM ONLY) ----
        log_channel = discord.utils.get(guild.channels, name=LOG_CHANNEL_NAME)

        if not log_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                gm_role: discord.PermissionOverwrite(view_channel=True),
            }

            log_channel = await guild.create_text_channel(
                LOG_CHANNEL_NAME,
                overwrites=overwrites
            )

        # ---- AUTO GIVE GM ROLE ----
        if gm_role not in interaction.user.roles:
            await interaction.user.add_roles(gm_role)

        await interaction.response.send_message(
            "Phone system initialized! You are now the Phone GM.",
            ephemeral=True
        )

    # -------- GIVE PHONE --------
    @bot.tree.command(description="Give a phone to a player.")
    @app_commands.checks.has_role(GM_ROLE_NAME)
    async def give_phone(interaction: discord.Interaction, user: discord.Member):

        role = discord.utils.get(interaction.guild.roles, name=PHONE_ROLE_NAME)

        if role not in user.roles:
            await user.add_roles(role)
            await interaction.response.send_message(f"{user.display_name} now has a phone!")
        else:
            await interaction.response.send_message(f"{user.display_name} already has a phone.")

    # -------- REMOVE PHONE --------
    @bot.tree.command(description="Remove a phone from a player.")
    @app_commands.checks.has_role(GM_ROLE_NAME)
    async def rem_phone(interaction: discord.Interaction, user: discord.Member):

        role = discord.utils.get(interaction.guild.roles, name=PHONE_ROLE_NAME)

        if role in user.roles:
            await user.remove_roles(role)
            await interaction.response.send_message(f"{user.display_name} no longer has a phone.")
        else:
            await interaction.response.send_message(f"{user.display_name} doesn't have a phone.")

    # -------- PHONE CALL --------
    @bot.tree.command(description="Send an in-game message via phone system.")
    @app_commands.checks.has_role(GM_ROLE_NAME)
    async def phone_call(
        interaction: discord.Interaction,
        user: discord.Member,
        to: str,
        msg: str
    ):

        role = discord.utils.get(interaction.guild.roles, name=PHONE_ROLE_NAME)

        if role in user.roles:
            channel = discord.utils.get(interaction.guild.channels, name=LOG_CHANNEL_NAME)

            await channel.send(
                f"☎️ NEW MESSAGE\nFrom: {user.display_name}\nTo: {to}\n\n{msg}"
            )

            await interaction.response.send_message(
                f"Message sent to {to}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "User does not have a phone.",
                ephemeral=True
            )

    # -------- GM RESPONSE --------
    @bot.tree.command(description="Respond to a player's phone message.")
    @app_commands.checks.has_role(GM_ROLE_NAME)
    async def phone_res(
        interaction: discord.Interaction,
        user: discord.Member,
        from_: str,
        msg: str
    ):

        await user.send(
            f"From: {from_} | Message: {msg}"
        )

        await interaction.response.send_message(
            "Message delivered.",
            ephemeral=True
        )