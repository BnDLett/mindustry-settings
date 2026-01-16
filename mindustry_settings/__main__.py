from pathlib import Path

from mindustry_settings.settings import MindustrySettings

if __name__ == "__main__":
    settings = MindustrySettings(Path("../settings.bin"))
    print(settings.get_string("uuid"))
