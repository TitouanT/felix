"""This is a cog for a discord.py bot.
It will add some responses to a bot

Commands:
    N/A

Load the cog by calling client.load_extension with the name of this python file
as an argument (without the file-type extension)
    example:    bot.load_extension('duckresponse')
or by calling it with the path and the name of this python file
    example:    bot.load_extension('cogs.duckresponse')
"""

from discord.ext import commands
from discord import Embed
from datetime import datetime as dt
import random
import re
import requests
import json

with open("../config.json", "r") as conffile:
    config = json.load(conffile)


class Responses(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_quack_string(self):
        intro = ['Ghost of duckie... Quack', 'Ghost of duckie... QUACK',
                 'Ghost of duckie... Quaaack']
        body = ['quack', 'quuuaaack', 'quack quack', 'qua...', 'quaack']
        ending = ['qua...', 'quack!', 'quack!!', 'qua..?', '..?', 'quack?',
                  '...Quack?', 'quack :slight_smile:', 'Quack??? :thinking:',
                  'QUAACK!! :angry:']
        ret = [random.choice(intro)]
        for _ in range(random.randint(1, 5)):
            ret.append(random.choice(body))
        ret.append(random.choice(3 * ending[:-1] + ending[-1:]))
        return ' '.join(ret)

    def get_year_string(self):
        now = dt.now()
        year_end = dt(now.year+1, 1, 1)
        year_start = dt(now.year, 1, 1)
        year_percent = (now - year_start) / (year_end - year_start) * 100
        return f'For your information, the year is {year_percent:.1f}% over!'

    def gif_url(self, terms):
        try:
            gifs = requests.get(f'http://api.giphy.com/v1/gifs/search?api_key={config["giphy_key"]}&q=\
                {terms}&limit=20&rating=R&lang=en').json()  # offset is 0 by default

            gif = random.choice(gifs['data'])['images']['original']['url']
            return gif
        except IndexError:  # for when no results are returned
            pass


    @commands.Cog.listener()
    async def on_message(self, msg):
        # Ignore messages sent by bots
        if msg.author.bot:
            return

        if re.search(r'(?i).*quack.*', msg.content):
            await msg.channel.send(self.get_quack_string())

        if re.search(r'(?i).*what a twist.*', msg.content):
            await msg.channel.send('` - directed by M. Night Shyamalan.`')

        if re.search(
            r'(?i)(the|this) (current )?year is ' +
            r'((almost|basically) )?(over|done|finished)',
            msg.content
        ):
            await msg.channel.send(self.get_year_string())

        if re.search(
            r'(?i)send bobs and vagene',
            msg.content
        ):
            await msg.channel.send('😏 *sensible chuckle*')

    @commands.command(
        name='source',
        brief='Links to source code',
        description='Show all links to EMKC github repos',
        aliases=['code', 'sauce', 'repo', 'repos'],
        hidden=False,
    )
    async def source(self, ctx):
        await ctx.send('Youtube : <https://github.com/engineer-man/youtube-code>' +
        '\nEMKC: <https://github.com/engineer-man/emkc>' +
        '\nFelix: <https://github.com/engineer-man/felix>' +
        '\nPiston a.k.a. Felix run: <https://github.com/engineer-man/piston>')

    @commands.command(
        name='gif-embed',
        brief='Dispalys a specified gif',
        aliases=['jif', 'embed-gif'],
        hidden=True
    )
    async def gif_embed(self, ctx, *, gif):
        g = self.gif_url(gif)
        if g is None:
            await ctx.send(f'Sorry {ctx.author.mention}, no gifs found 😔')
            await ctx.message.add_reaction('❌')
        else:
            e = Embed(title='Your **gif** boss', color=0x000000)
            e.set_image(url=g)
            e.set_footer(text=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)

            await ctx.send(embed=e)
            await ctx.message.add_reaction('✅')

    @gif_embed.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Name the gif you want next time pls')
            await ctx.message.add_reaction('❌')


    @commands.group(
        invoke_without_command=True,
        name='how-to',
        brief='Shows useful information for newcomers',
        description='A group of commands that help newcomers',
        aliases=['howto', 'info']
    )
    async def how_to(self, ctx):
        await self.client.help_command.command_callback(ctx, command='how-to')

    @how_to.command(
        name='codeblocks',
        brief='How to use code blocks to paste code',
        description='Instructions on how to properly paste code',
        aliases=['codeblock', 'code-blocks', 'code-block', 'code']
    )
    async def codeblocks(self, ctx):
        code_instructions = (
            '''Discord has an awesome feature called **Text Markdown**\
            which supports code with full syntax highlighting using codeblocks.\
            To use codeblocks all you need to do is properly place the backtick\
            characters (not single quotes) and specify your\
            language *(optional, but preferred)*.\n
            **This is what your message should look like:**
            *\\`\\`\\`[programming language]\nYour code here\n\\`\\`\\`*\n
            **Here's an example:**
            *\\`\\`\\`python\nprint('Hello world!')\n\\`\\`\\`*\n
            **This will result in the following:**
            ```python\nprint('Hello world!')\n```\n
            **NOTE:** Codeblocks are also used to run code via `felix run`.'''
        )
        link = '210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-'

        e = Embed(title='Text markdown',
                  url=f'https://support.discordapp.com/hc/en-us/articles/{link}',
                  description=code_instructions,
                  color=0x2ECC71)
        await ctx.send(embed=e)

    @how_to.command(
        name='ask',
        brief='How to properly ask a question',
        description='Instructions on how to properly ask a question',
        aliases=['questions', 'question']
    )
    async def ask(self, ctx):
        ask_instructions = (
            """From time to time you'll stumble upon a question like this:
            *Is anyone good at [this] or [that]?* / *Does anyone know [topic]?*
            Please **just ask** your question.\n
            • Make sure your question is easy to understand.
            • Use the appropriate channel to ask your question.
            • Always search before you ask (the internet is a big place).
            • Be patient (someone will eventually try to answer your question)."""
        )

        e = Embed(title='Just ask',
                  description=ask_instructions,
                  color=0x2ECC71)
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Responses(client))
