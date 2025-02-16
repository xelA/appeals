import os

from dotenvplus import DotEnv
from quart import Quart, redirect, url_for, render_template
from quart_discord import DiscordOAuth, NotSignedIn

from utils.xela import xelAAPI

config = DotEnv(".env")
app = Quart(__name__)
app.config["SECRET_KEY"] = config["DISCORD_CLIENT_SECRET"]
xela = xelAAPI(config)

if "http://" in config["DISCORD_REDIRECT_URI"]:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"


discord = DiscordOAuth(
    app,
    config["DISCORD_CLIENT_ID"],
    config["DISCORD_CLIENT_SECRET"],
    config["DISCORD_REDIRECT_URI"],
    debug=config["HTTP_DEBUG"]
)


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/login")
async def login():
    return discord.prepare_login("identify")


@app.route("/logout")
async def logout():
    discord.clear_session()
    return redirect(url_for(".index"))


@app.route("/callback")
async def callback():
    return discord.callback(".me")


@app.errorhandler(NotSignedIn)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/profile")
@discord.require_discord_oauth
async def me():
    user = discord.user()

    return await render_template("profile.html", user=user)


app.run(
    host="127.0.0.1",
    port=config["HTTP_PORT"]
)
