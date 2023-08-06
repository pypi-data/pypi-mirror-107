"""Siemens MR spectroscopy / RDA file format (.rda files)."""
import io
import re
import typing as t

import yaml
from fw_meta import MetaExtractor
from fw_utils import AnyFile, BinFile

from .common import FieldsMixin
from .dicom import utils
from .file import File

HEADER_START = b">>> Begin of header <<<"
HEADER_END = b">>> End of header <<<"
FIELD_RE = r"^(?P<name>\w+)(?P<index>\[[^\]]+\])?:\s*(?P<value>.*?)?\s*$"


class RDA(FieldsMixin, File):  # pylint: disable=too-many-ancestors
    """Siemens MR spectroscopy / RDA file class."""

    def __init__(
        self,
        file: t.Union[AnyFile, BinFile],
        extractor: t.Optional[MetaExtractor] = None,
    ) -> None:
        """Read and parse a Siemens MR spectroscopy-/ RDA file.

        Args:
            file (str|Path|file): Filepath (str|Path) or open file to read from.
            extractor (MetaExtractor, optional): MetaExtractor instance to
                customize metadata extraction with if given. Default: None.
        """
        super().__init__(file)
        with self.file as rfile:
            object.__setattr__(self, "fields", read_header(rfile))
            object.__setattr__(self, "offset", rfile.tell())

    @property
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata for the RDA file."""
        firstname, lastname = utils.get_patient_name(self)
        defaults: t.Dict[str, t.Any] = {
            "subject.label": self.get("PatientID"),
            "subject.firstname": firstname,
            "subject.lastname": lastname,
            "subject.sex": self.get("PatientSex"),
            "session.label": utils.get_session_label(self),
            "session.age": utils.get_session_age(self),
            "session.weight": self.get("PatientWeight"),
            "session.timestamp": utils.get_session_timestamp(self),
            "acquisition.label": utils.get_acquisition_label(self),
            "acquisition.timestamp": utils.get_acquisition_timestamp(self),
            "file.type": "spectroscopy",  # TODO add core filetype
        }
        return {k: v for k, v in defaults.items() if v is not None and v != ""}

    def save(self, file: t.Optional[AnyFile] = None, **kwargs: t.Any) -> None:
        """Save RDA file."""
        bytesio = io.BytesIO()
        bytesio.write(dump_header(self.fields))
        with self.file as rfile:
            rfile.seek(self.offset)
            bytesio.write(rfile.read())
        with self.open_dst(file) as wfile:
            wfile.write(bytesio.getvalue())


def read_header(file: BinFile) -> t.Dict[str, t.Any]:
    """Read and parse RDA file header fields."""
    fields: t.Dict[str, t.Any] = {}
    first_line = file.readline()
    if not first_line.startswith(HEADER_START):
        raise ValueError("Invalid RDA: cannot find header start")
    for line in file:
        if line.startswith(HEADER_END):
            break
        line = line.decode().strip()
        match = re.match(FIELD_RE, line)
        if not match:
            raise ValueError(f"Invalid RDA: cannot parse line {line!r}")
        name, index, value = match.groups()
        try:
            value = yaml.safe_load(value)
        except yaml.composer.ComposerError:
            pass
        if index:
            field = fields.setdefault(name, {})
            key = tuple(yaml.safe_load(i) for i in index[1:-1].split(","))
            field[key[0] if len(key) == 1 else key] = value
        else:
            fields[name] = value
    else:
        raise ValueError("Invalid RDA: cannot find header end")
    return fields


def dump_header(fields: t.Dict[str, t.Any]) -> bytes:
    """Dump RDA header fields to a bytestring."""
    header = io.BytesIO()
    header.write(HEADER_START + b"\r\n")
    for name, value in fields.items():
        if isinstance(value, dict):
            for key, subval in value.items():
                index = key
                if isinstance(index, tuple):
                    index = ",".join([str(i) for i in key])
                header.write(f"{name}[{index}]: {subval}\r\n".encode())
        else:
            header.write(f"{name}: {value}\r\n".encode())
    header.write(HEADER_END + b"\r\n")
    return header.getvalue()
