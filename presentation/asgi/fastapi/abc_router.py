from fastapi import APIRouter


class ABCRouterBuilder:
    def create_router(self) -> APIRouter:
        raise NotImplementedError
