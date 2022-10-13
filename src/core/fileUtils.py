from pathlib import Path

class FileUtils(object):

    @classmethod
    def setProjectRoot(cls) -> None:
        cls._ProjectRoot: str = Path(__file__).resolve().parent.parent
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
        file_path: str = f"{FileUtils.pathAssetsRoot()}/{file_name}"
        # check if file exisits
        if not Path(file_path).is_file():
            raise Exception(f"Cant locate asset file at {file_path}")
        return file_path

    @classmethod
    def getShaderDir(cls, shader_name: str) -> str:
        file_path: str = f"{FileUtils.pathShadersRoot()}/{shader_name}"
        if not Path(file_path).is_dir():
            raise Exception(f"No directory called {shader_name} in shader directory..")
        elif not Path(f"{file_path}/{shader_name}.vert").is_file():
            raise Exception(f"No {shader_name}.vert in.. {file_path}")
        elif not Path(f"{file_path}/{shader_name}.frag").is_file():
            raise Exception(f"No {shader_name}.frag in.. {file_path}")
        return file_path