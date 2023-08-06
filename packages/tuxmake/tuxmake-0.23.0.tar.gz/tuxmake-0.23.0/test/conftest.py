import os
import pathlib
import pytest
import shutil


from tuxmake.arch import Architecture


if pytest.__version__ < "3.9":

    @pytest.fixture()
    def tmp_path(tmpdir):
        return pathlib.Path(tmpdir)


@pytest.fixture(scope="session", autouse=True)
def session_home(tmpdir_factory):
    os.environ["HOME"] = str(tmpdir_factory.mktemp("HOME"))


@pytest.fixture(autouse=True)
def home(monkeypatch, tmp_path):
    h = tmp_path / "HOME"
    monkeypatch.setenv("HOME", str(h))
    return h


@pytest.fixture(scope="session")
def linux(tmpdir_factory):
    src = pathlib.Path(__file__).parent / "fakelinux"
    dst = tmpdir_factory.mktemp("source") / "linux"
    shutil.copytree(src, dst)
    return dst


@pytest.fixture(autouse=True, scope="session")
def fake_cross_compilers(tmpdir_factory):
    missing = {}
    for a in Architecture.supported():
        arch = Architecture(a)
        for tool in ["gcc", "ld"]:
            binary = arch.makevars["CROSS_COMPILE"] + tool
            if not shutil.which(binary):
                missing[binary] = tool
    if missing:
        testbin = tmpdir_factory.mktemp("bin")
        for p, real in missing.items():
            os.symlink(f"/usr/bin/{real}", testbin / p)
        os.environ["PATH"] = f"{testbin}:" + os.environ["PATH"]
