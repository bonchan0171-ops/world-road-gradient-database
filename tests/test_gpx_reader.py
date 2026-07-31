from pathlib import Path

import pytest

from wrgd.io.gpx_reader import GPXReader


def test_read_gpx(tmp_path: Path) -> None:
    gpx = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1"
     creator="pytest"
     xmlns="http://www.topografix.com/GPX/1/1">

  <trk>
    <name>Sample Track</name>

    <trkseg>
      <trkpt lat="35.681236" lon="139.767125"/>
      <trkpt lat="35.681500" lon="139.768000"/>
    </trkseg>

  </trk>

</gpx>
"""

    filepath = tmp_path / "sample.gpx"
    filepath.write_text(gpx, encoding="utf-8")

    reader = GPXReader(filepath)

    coordinates = reader.read()

    assert len(coordinates) == 2

    assert coordinates[0].latitude == 35.681236
    assert coordinates[0].longitude == 139.767125

    assert coordinates[1].latitude == 35.681500
    assert coordinates[1].longitude == 139.768000


def test_invalid_xml(tmp_path: Path) -> None:
    filepath = tmp_path / "invalid.gpx"

    filepath.write_text(
        "<gpx><trk></gpx>",
        encoding="utf-8",
    )

    reader = GPXReader(filepath)

    with pytest.raises(ValueError):
        reader.read()


def test_track_not_found(tmp_path: Path) -> None:
    filepath = tmp_path / "no_track.gpx"

    filepath.write_text(
        """<?xml version="1.0"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1">
</gpx>
""",
        encoding="utf-8",
    )

    reader = GPXReader(filepath)

    with pytest.raises(ValueError):
        reader.read()


def test_tracksegment_not_found(tmp_path: Path) -> None:
    filepath = tmp_path / "no_segment.gpx"

    filepath.write_text(
        """<?xml version="1.0"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1">
<trk></trk>
</gpx>
""",
        encoding="utf-8",
    )

    reader = GPXReader(filepath)

    with pytest.raises(ValueError):
        reader.read()


def test_trackpoint_not_found(tmp_path: Path) -> None:
    filepath = tmp_path / "no_point.gpx"

    filepath.write_text(
        """<?xml version="1.0"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1">
<trk>
<trkseg>
</trkseg>
</trk>
</gpx>
""",
        encoding="utf-8",
    )

    reader = GPXReader(filepath)

    with pytest.raises(ValueError):
        reader.read()
