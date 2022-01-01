from .nukeopscog import NukeOpsCog


def setup(bot):
    bot.add_cog(NukeOpsCog(bot))
