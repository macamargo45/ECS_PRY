from src.engine.services.fonts_service import FontsService
from src.engine.services.images_service import ImagesService
from src.engine.services.sounds_service import SoundsService
from src.engine.services.texts_services import TextsService

class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsService()
    texts_service = TextsService()    
    fonts_service = FontsService()