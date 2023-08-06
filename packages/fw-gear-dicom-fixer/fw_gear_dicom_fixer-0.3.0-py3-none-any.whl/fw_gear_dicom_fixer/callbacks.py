import logging
import typing as t

from fw_file.dicom import DICOM
from fw_file.dicom.fixer import raw_elem_tracker
from pydicom import values
from pydicom.charset import decode_element
from pydicom.datadict import keyword_for_tag, tag_for_keyword
from pydicom.dataelem import DataElement, RawDataElement
from pydicom.dataset import Dataset

log = logging.getLogger(__name__)


def handle_incorrect_unit(
    raw_elem: RawDataElement,
    data_element_callback: t.Callable[..., RawDataElement] = None,
    **kwargs: t.Dict
) -> RawDataElement:  # pylint: disable=invalid-name
    """Callback to fix known incorrect units.

    Args:
        raw_elem (RawDataElement): Data element to be corrected.
        data_element_callback (t.Callable[..., RawDataElement], optional): other clalback. Defaults to None.

    Returns:
        RawDataElement: Corrected callback
    """
    if data_element_callback and callable(data_element_callback):
        raw_elem = data_element_callback(raw_elem, **kwargs)
    # Check for incorrect unit on MagneticFieldStrength
    encoding = (kwargs.get("encoding", ["iso8859"]) or ["iso8859"])[0]
    if raw_elem.tag.real == tag_for_keyword("MagneticFieldStrength"):
        try:
            mfs = values.convert_value("DS", raw_elem, encoding)
            mfs = float(mfs)
        except:  # pragma: no cover
            log.error(
                "Uncaught exception, not attempting to change value.", exc_info=True
            )
            return raw_elem
        if mfs:
            if mfs > 30:
                mfs /= 1000
                # DS "decimal string" VR, cast to string.
                raw_elem = raw_elem._replace(value=bytes(str(mfs).encode(encoding)))
    return raw_elem


def decode_dcm(dcm: DICOM) -> None:
    """Decode dicom.

       Mirrors pydicom.dataset.Dataset.decode, except it ignores decoding the
       OriginalAttributesSequence tag.

    Args:
        dcm (DICOM): dicom file.
    """
    dicom_character_set = dcm.dataset.raw._character_set

    def decode(dataset: Dataset, data_element: DataElement) -> None:
        """Callback to decode data element, but ignore OriginalAttributesSequence."""

        if data_element.VR == "SQ":
            if data_element.tag == tag_for_keyword("OriginalAttributesSequence"):
                return
            for dset in data_element.value:
                dset._parent_encoding = dicom_character_set
                dset.decode()
        else:
            decode_element(data_element, dicom_character_set)

    with raw_elem_tracker(dcm.tracker):
        dcm.walk(decode, recursive=False)
