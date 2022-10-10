import pathlib as pl

class FileUtils(object):

    @staticmethod
    def pathRoot() -> str:
        return pl.Path(__file__).resolve().parent.parent

    @staticmethod
    def pathAssets() -> str:
        return f"{FileUtils.pathRoot()}/assets"

    @staticmethod
    def pathShaders() -> str:
        return f"{FileUtils.pathRoot()}/shaders"

    @staticmethod
    def getAsset(file_name: str) -> str:
        return f"{FileUtils.pathAssets()}/{file_name}"