"""Nifti file module."""
import typing as t
from pathlib import Path

import nibabel
from fw_utils import AnyFile, BinFile

from .file import File


class Nifti(File):  # pylint: disable=too-many-ancestors
    """NIfTI data-file class."""

    def __init__(
        self,
        file: t.Union[AnyFile, BinFile],
    ) -> None:
        """Load and parse NIfTI1 and NIfTI2 files.

        Args:
            file (t.Union[AnyFile, BinFile]): File to load.

        Raises:
            ValueError: If file is not a valid NIfTI1 or NIfTI2 file.
        """
        if not isinstance(file, (str, Path)):
            raise ValueError("Nifti doesn't support open files.")
        super().__init__(file)
        try:
            img = nibabel.load(self.localpath)
        except nibabel.filebasedimages.ImageFileError as e:
            raise ValueError("Invalid NIfTI file.") from e

        object.__setattr__(self, "nifti", img)

    @property
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata."""
        defaults: t.Dict[str, t.Any] = {
            "file.type": "nifti",
            "file.name": Path(self.localpath).name,
        }
        return defaults

    def save(self, file: t.Optional[AnyFile] = None, **kwargs: t.Any) -> None:
        """Save nifti image."""
        if not isinstance(file, (str, Path)):
            raise ValueError("Nifti doesn't support open files.")
        nibabel.save(self.nifti, file)

    def __getitem__(self, key: str) -> t.Any:
        """Get header value by name."""
        return self.nifti.header[key]

    def __setitem__(self, key: str, value: t.Any) -> None:
        """Set header value by name and value."""
        self.nifti.header[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete header value."""
        raise NotImplementedError("Cannot remove field from NIfTI header.")

    def __iter__(self):
        """Return iterator over nifti header."""
        return iter(self.nifti.header)

    def __len__(self) -> int:
        """Return length of nifti header."""
        return len(list(self.nifti.header.items()))
