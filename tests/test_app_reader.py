"""
Unit tests for app reader/writer classes.
Ported from legacy-tests/test_unit_apps.py
"""
import pytest


class TestINIReader:
    """Tests for the INI format reader/writer."""

    def test_read_params(self, app):
        """Test reading INI parameters for DNA app."""
        from spc.app_reader_writer import INI

        reader = INI('dna')
        params, blockmap, blockorder = reader.read_params()

        # Should have read some parameters
        assert len(params) > 0
        assert len(blockmap) > 0
        assert len(blockorder) > 0

    def test_params_contain_dna(self, app):
        """Test that DNA app has a 'dna' parameter."""
        from spc.app_reader_writer import INI

        reader = INI('dna')
        params, _, _ = reader.read_params()

        # DNA app should have a 'dna' parameter
        assert 'dna' in params


class TestJSONReader:
    """Tests for the JSON format reader/writer."""

    def test_read_params(self, app):
        """Test reading JSON parameters for DNA app."""
        from spc.app_reader_writer import JSON

        reader = JSON('dna')
        params, blockmap, blockorder = reader.read_params()

        assert len(params) > 0
        assert len(blockmap) > 0
        assert len(blockorder) > 0


class TestYAMLReader:
    """Tests for the YAML format reader/writer."""

    def test_read_params(self, app):
        """Test reading YAML parameters for DNA app."""
        from spc.app_reader_writer import YAML

        reader = YAML('dna')
        params, blockmap, blockorder = reader.read_params()

        assert len(params) > 0


class TestNamelistReader:
    """Tests for the Namelist format reader/writer."""

    def test_read_params(self, app):
        """Test reading Namelist parameters for DNA app."""
        from spc.app_reader_writer import Namelist

        reader = Namelist('dna')
        params, blockmap, blockorder = reader.read_params()

        assert len(params) > 0
        assert len(blockmap) > 0
        assert len(blockorder) > 0


class TestAppClass:
    """Tests for the base App class."""

    def test_app_init(self, app):
        """Test App class initialization."""
        from spc.app_reader_writer import App

        myapp = App('dna')
        assert myapp.appname == 'dna'
