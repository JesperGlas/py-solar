import pathlib as pl

class FileUtils(object):

    @classmethod
    def setProjectRoot(cls) -> None:
        cls._ProjectRoot: str = pl.Path(__file__).resolve().parent.parent
        print(f"Project root dir is set to: {cls._ProjectRoot}")

    @classmethod
    def pathRoot(cls) -> str:
        return cls._ProjectRoot

    @classmethod
    def pathAssetsRoot(cls) -> str:
        return f"{cls._ProjectRoot}/assets"

    @classmethod
    def pathShadersRoot(cls) -> str:
        return f"{cls._ProjectRoot}/shaders"

    @classmethod
    def getAsset(cls, file_name: str) -> str:
        return f"{FileUtils.pathAssetsRoot()}/{file_name}"

    @classmethod
    def getShaderDir(cls, shader_name: str) -> str:
        return f"{FileUtils.pathShadersRoot()}/{shader_name}"