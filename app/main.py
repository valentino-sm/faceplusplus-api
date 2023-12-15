from core.services.image import ABCImageService, ImageService
from core.services.main import MainService
from infrastructure.cognitive_service import (ABCCognitiveService,
                                              FacePlusPlusCognitiveService)
from infrastructure.container import Container
from infrastructure.db.abc_repository import BaseRepository
from infrastructure.db.engine import ABCDatabaseEngine
from infrastructure.db.repositories.image import ImageRepository
from infrastructure.db.session_manager import ABCSessionManager, SessionManager
from infrastructure.db.sqlalchemy.engine import SQLAlchemyEngine
from infrastructure.db.sqlalchemy.repository import SQLAlchemyRepository
from infrastructure.db.unitofwork import ABCUnitOfWork, SQLAlchemyUnitOfWork
from infrastructure.http import ABCHTTPClient, HTTPXClient
from infrastructure.lifespan import ABCLifespan, EmptyLifespan
from presentation.asgi.abc_builder import ASGIApp, ASGIAppBuilder
from presentation.asgi.fastapi.abc_router import ABCRouterBuilder
from presentation.asgi.fastapi.builder import FastAPIAppBuilder
from presentation.asgi.routes.api import APIRouterBuilder
from utils.logging import Logging
from utils.settings import Settings


def build_container() -> Container:
    settings = Settings()

    logging = Logging(is_debug=settings.debug)
    logger = logging.get_logger(__name__)
    logger.info("Starting building container")

    container = Container()

    # INFRASTRUCTURE
    container.register(Logging, instance=logging)
    container.register(ABCLifespan, EmptyLifespan)
    container.register(ABCHTTPClient, HTTPXClient)
    container.register(
        ABCCognitiveService,
        FacePlusPlusCognitiveService,
        api_key=settings.faceplusplus_api_key,
        api_secret=settings.faceplusplus_api_secret,
    )

    # SERVICES
    container.register(ABCImageService, ImageService)
    container.register(MainService)

    # REPOSITORIES
    container.register(ImageRepository)

    # DATABASE
    container.register(BaseRepository, SQLAlchemyRepository)
    container.register(ABCUnitOfWork, SQLAlchemyUnitOfWork)
    container.register(ABCSessionManager, SessionManager)
    container.register(ABCDatabaseEngine, SQLAlchemyEngine, url=settings.db_url)

    # ROUTES
    container.register(ABCRouterBuilder, APIRouterBuilder)

    # ASGI App
    container.register(ASGIAppBuilder, FastAPIAppBuilder)
    return container


def create_app() -> ASGIApp:
    container = build_container()
    app_builder: ASGIAppBuilder = container.resolve(ASGIAppBuilder)
    return app_builder.create_app()
