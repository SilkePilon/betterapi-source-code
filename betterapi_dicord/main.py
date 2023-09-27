import discord,os,requests,time,json
from discord import app_commands
import glob
from io import BytesIO
import os, shutil
from PIL import Image
from discord.ui import Button, View
from typing import List
class LinkButton(View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(Button(label='Download image', url=url))
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="youchat", description="Talk to YouChat")
async def first_command(interaction, message:str = "hi there"):
    url = f"https://api.betterapi.net/youchat?inputs={message}&stream=True&key=site"
    msg = await interaction.send(f"Please wait...")
    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(1024):  # or, for line in r.iter_lines():
            await msg.edit(content=f'{chunk.decode("utf-8")}')
    
    
    
    
# The photograph captures a breathtaking panoramic view of majestic snow-capped mountains towering over a lush valley. The intricate details of the landscape are vividly portrayed, with each craggy peak and rocky outcrop etched in sharp relief against the clear blue sky. The interplay of light and shadow creates a stunning contrast between the sun-kissed slopes and the shaded valleys below. In the foreground, verdant forests and meadows add a splash of vibrant color to the serene landscape, inviting the viewer to immerse themselves in the natural beauty of this awe-inspiring mountain vista.
# fantastic scenery landscape from the top of the mountain, pine trees, green valleys, magic fog and lightning, epic composition, fibonacci ratio, golden ratio, fancy, incredible detailed game artwork, sharpen and ultra quality, trending, artstation, behance, wikiart, 8 k
    
async def rps_autocomplete(
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        styles = ['Realistic v2', 'Abstract Fluid v2', 'Buliojourney v2', 'Illustrated v2', 'Dreamwave v2', 'The Bulio Cut', 'The Cut', 'Gloomy', 'Spectral v2', 'Anime v2', 'Flora v2', 'Watercolor v2', 'Blues v2', 'Figure', 'Expressionism', 'HDR', 'Spectral', 'Comic' ,'Winter', 'Festive', 'Soft Touch', 'Splatter', 'Realistic', 'Flora', 'Abstract', 'Diorama', 'Vector', 'Fantastical', 'Bad Trip', 'Cartoonist', 'Isometric', 'Analogue', 'Retro-Futurism', 'Paint', 'Polygon', 'Gouache', 'Ink', 'Line-Art', 'Anime', 'Malevolent', 'Surreal', 'Unrealistic', 'Throwback', 'Street Art', 'No Style', 'Ghibli', 'Melancholic', 'Pandora', 'Daydream', 'Provenance', 'Arcane', 'Toasty', 'Psychic', 'Wuhtercuhler', 'Rose Gold', 'Etching']
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in styles if current.lower() in choice.lower()
        ]
    
    
@tree.command(name="imagine", description="make ai images")
async def Imagine(interaction: discord.Interaction, style:str, prompt:str="forest"):
    
    await interaction.response.defer()
    style = style.lower()
    
    
    if style == "realistic v2":
        style = 78
    if style == "buliojourney v2":
        style = 84
    if style == "abstract fluid v2":
        style = 99
    if style == "illustrated v2":
        style = 98
    if style == "dreamwave v2":
        style = 97
    if style == "the bulio cut":
        style = 96
    if style == "the cut":
        style = 95
    if style == "gloomy":
        style = 94
    if style == "spectral v2":
        style = 92
    if style == "anime v2":
        style = 80
    if style == "flora v2":
        style = 81
    if style == "watercolor v2":
        style = 91
    if style == "blues v2":
        style = 88
    if style == "figure":
        style = 76
    if style == "expressionism":
        style = 77
    if style == "hdr":
        style = 52
    if style == "Spectral":
        style = 63
    if style == "comic":
        style = 45
    if style == "winter":
        style = 72
    if style == "festive":
        style = 73
    if style == "soft touch":
        style = 71
    if style == "splatter":
        style = 74
    if style == "realistic":
        style = 32
    if style == "flora":
        style = 68
    if style == "abstract":
        style = 67
    if style == "diorama":
        style = 65
    if style == "vector":
        style = 60
    if style == "fantastical":
        style = 61
    if style == "bad trip":
        style = 57
    if style == "cartoonist":
        style = 58
    if style == "isometric":
        style = 55
    if style == "analogue":
        style = 53
    if style == "retro-futurism":
        style = 54
    if style == "paint":
        style = 50
    if style == "polygon":
        style = 49
    if style == "gouache":
        style = 48
    if style == "ink":
        style = 38
    if style == "line-art":
        style = 47
    if style == "anime":
        style = 46
    if style == "malevolent":
        style = 40
    if style == "surreal":
        style = 37
    if style == "unrealistic":
        style = 42
    if style == "throwback":
        style = 35
    if style == "street art":
        style = 41
    if style == "no style":
        style = 3
    if style == "ghibli":
        style = 22
    if style == "melancholic":
        style = 28
    if style == "pandora":
        style = 39
    if style == "daydream":
        style = 36
    if style == "provenance":
        style = 17
    if style == "arcane":
        style = 34
    if style == "toasty":
        style = 31
    if style == "psychic":
        style = 9
    if style == "wuhtercuhler":
        style = 16
    if style == "rose gold":
        style = 18
    if style == "etching":
        style = 14
    
    
    
    
    
    
    print(prompt)
    while True:
        data = requests.get(f"https://api.betterapi.net/imagine/gen?prompt={prompt}&key=9411O936ZW19CENQ3IZGX3Z42MBZI8KKM6I&style={style}").json()
        try: 
            msg = data['url']
            stages = data['stages']
            break
        except:
            msg = "got an error!"
        time.sleep(3)
    if msg == "":
        msg = "I'm sorry i've run into an error."
    
        
    stages = eval(stages)
    
    stage_index = 1
    embed=discord.Embed(title="Stable Diffusion")
    # for stage in stages:
    #     embed.add_field(name=f"Stage {stage_index}", value=f"[show]({stage})", inline=True)
    #     stage_index += 1
        

    # frames = []
    # for image in stages[1:]:
    #     response = requests.get(image)
    #     img = Image.open(BytesIO(response.content))
    #     frames.append(img)
    # # frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.JPG")]
    # frame_one = frames[0]
    # frame_one.save("my_awesome.gif", format="GIF", append_images=frames,
    #         save_all=True, duration=800, loop=0)
    # file = discord.File("my_awesome.gif")
    
    # folder = '/home/pi/you.com/betterapi/downloads'
    # for filename in os.listdir(folder):
    #     file_path = os.path.join(folder, filename)
    #     try:
    #         if os.path.isfile(file_path) or os.path.islink(file_path):
    #             os.unlink(file_path)
    #         elif os.path.isdir(file_path):
    #             shutil.rmtree(file_path)
    #     except Exception as e:
    #         print('Failed to delete %s. Reason: %s' % (file_path, e))
    

        
        
    embed.set_image(url=f"{msg}")
    embed.set_footer(text="BetterAPI")
    button_view = LinkButton(url=msg)
    await interaction.followup.send(embed=embed, view=button_view)
    
    
@Imagine.autocomplete('style')
async def fruits_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    fruits = ['Realistic v2', 'Abstract Fluid v2', 'Buliojourney v2', 'Illustrated v2', 'Dreamwave v2', 'The Bulio Cut', 'The Cut', 'Gloomy', 'Spectral v2', 'Anime v2', 'Flora v2', 'Watercolor v2', 'Blues v2', 'Figure', 'Expressionism', 'HDR', 'Spectral', 'Comic' ,'Winter', 'Festive', 'Soft Touch', 'Splatter', 'Realistic', 'Flora', 'Abstract', 'Diorama', 'Vector', 'Fantastical', 'Bad Trip', 'Cartoonist', 'Isometric', 'Analogue', 'Retro-Futurism', 'Paint', 'Polygon', 'Gouache', 'Ink', 'Line-Art', 'Anime', 'Malevolent', 'Surreal', 'Unrealistic', 'Throwback', 'Street Art', 'No Style', 'Ghibli', 'Melancholic', 'Pandora', 'Daydream', 'Provenance', 'Arcane', 'Toasty', 'Psychic', 'Wuhtercuhler', 'Rose Gold', 'Etching']
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


@tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    if interaction.user.id == 848631452638642198:
        await tree.sync()
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')
client.run("") # paste your token here.
