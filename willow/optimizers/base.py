import logging
import subprocess
from typing import ClassVar

logger = logging.getLogger("willow")


class OptimizerBase:
    library_name: ClassVar[str] = ""
    image_format: ClassVar[str] = ""
    # Exit codes that mean the library chose not to change the file rather than failed
    ignored_return_codes: ClassVar[frozenset[int]] = frozenset()

    class Meta:
        abstract = True

    @classmethod
    def applies_to(cls, image_format: str) -> bool:
        return image_format.lower() == cls.image_format.lower()

    @classmethod
    def get_check_library_arguments(cls) -> list[str]:
        """
        Return a list of arguments to check if the library exists.

        Note: using --help by default as that usually returns a zero exit code
        """
        return ["--help"]

    @classmethod
    def check_library(cls) -> bool:
        args = [cls.library_name] + cls.get_check_library_arguments()
        try:
            subprocess.check_output(args, stderr=subprocess.STDOUT)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    @classmethod
    def get_command_arguments(cls, file_path: str) -> list[str]:
        """Return a list of arguments for the given optimizer library."""
        return []

    @classmethod
    def process(cls, file_path: str):
        args = [cls.library_name] + cls.get_command_arguments(file_path)
        try:
            subprocess.check_output(args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            output = (exc.output or b"").decode(errors="replace").strip() or "no output"
            if exc.returncode in cls.ignored_return_codes:
                logger.debug(
                    "Skipped optimizing %s with the '%s' library (exit status %s): %s",
                    file_path,
                    cls.library_name,
                    exc.returncode,
                    output,
                )
                return
            logger.error(
                "Error optimizing %s with the '%s' library (exit status %s): %s",
                file_path,
                cls.library_name,
                exc.returncode,
                output,
            )
        except OSError as exc:
            logger.error(
                "Error optimizing %s with the '%s' library: %s",
                file_path,
                cls.library_name,
                exc,
            )
