from environs import Env
env = Env()
env.read_env()
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
DB = env.str("DB")
min_priority = 3
max_priority = 6
CHAT = env.int("CHAT")
TEST_CHAT = env.int("TEST_CHAT")
