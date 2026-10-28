from typing import ClassVar

from .base import OptimizerBase

__all__ = ["Pngquant"]


class Pngquant(OptimizerBase):
    """https://pngquant.org/"""

    library_name: ClassVar[str] = "pngquant"
    image_format: ClassVar[str] = "png"
    # 98: --skip-if-larger left the file as is because the result would be larger
    ignored_return_codes: ClassVar[frozenset[int]] = frozenset({98})

    @classmethod
    def get_command_arguments(
        cls, file_path: str, progressive: bool = False
    ) -> list[str]:
        return [
            "--force",  # allow overwriting existing files
            "--strip",  # remove optional metadata
            "--skip-if-larger",
            file_path,  # the file as input
            "--output",
            file_path,  # the file as output
        ]
