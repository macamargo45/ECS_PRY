import pygame


class TextsService:
    def __init__(self) -> None:
        self.texts = {}

    def get(self, path: str, size: int) -> pygame.font.Font:
        if path not in self.texts:
            self.texts[(path, size)] = pygame.font.Font(path, size)
        return self.texts[(path, size)]
