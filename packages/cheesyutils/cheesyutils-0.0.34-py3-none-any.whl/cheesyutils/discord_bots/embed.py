import discord
from .constants import *
from typing import Any


class Embed(discord.Embed):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)

    def _check_integrety(self):
        if len(self) > MAX_EMBED_TOTAL_LENGTH:
            raise ValueError(f"Embed total length cannot exceed {MAX_EMBED_TOTAL_LENGTH} in length")
        elif len(self.title) > MAX_EMBED_TITLE_LENGTH:
            raise ValueError(f"Embed title cannot exceed {MAX_EMBED_TITLE_LENGTH} in length")
        elif len(self.description) > MAX_EMBED_DESCRIPTION_LENGTH:
            raise ValueError(f"Embed description cannot exceed {MAX_EMBED_DESCRIPTION_LENGTH} in length")
        elif len(self.fields) > MAX_EMBED_FIELD_COUNT:
            raise ValueError(f"Embed field count cannot exceed {MAX_EMBED_FIELD_COUNT}")

    def _check_embed_values(self, name: str, value: Any):
        if len(name) > MAX_EMBED_FIELD_NAME_LENGTH:
            raise ValueError(f"Embed field name length cannot exceed {MAX_EMBED_FIELD_NAME_LENGTH} in length")
        elif len(str(value)) > MAX_EMBED_FIELD_VALUE_LENGTH:
            raise ValueError(f"Embed field value length cannot exceed {MAX_EMBED_FIELD_VALUE_LENGTH} in length")
    
    def add_field(self, *, name: str, value: Any, inline: bool=True):
        self._che
        e = super().add_field(name, value, inline=inline)
        self._check_integrety()
        return e
    
    def insert_field_at(self, index, *, name, value, inline):
        e = super().insert_field_at(index, name, value, inline=inline)
        self._check_integrety()
        return e

    def set_author(self, *, name, url, icon_url):
        if len(name) > MAX_EMBED_AUTHOR_NAME_LENGTH:
            raise ValueError(f"Embed author name cannot exceed {MAX_EMBED_AUTHOR_NAME_LENGTH} characters in length")
    
        e = super().set_author(name, url=url, icon_url=icon_url)
        self._check_integrety()
        return e
    