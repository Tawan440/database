from environs import Env

class BotConfig:
    _env = Env()
    
    def __init__(self, env_path:str | None = None):
        self._env.read_env(env_path)
        self.token: str = self._env('BOT_TOKEN')
        self.admin_ids: list = self._env('ADMIN_IDS')