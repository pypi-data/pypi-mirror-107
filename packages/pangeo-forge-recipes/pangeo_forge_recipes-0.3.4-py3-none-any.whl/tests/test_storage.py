import pytest
from pytest_lazyfixture import lazy_fixture

from pangeo_forge_recipes.storage import file_opener


def test_target(tmp_target):
    mapper = tmp_target.get_mapper()
    mapper["foo"] = b"bar"
    with open(tmp_target.root_path + "/foo") as f:
        res = f.read()
    assert res == "bar"
    with pytest.raises(FileNotFoundError):
        tmp_target.rm("baz")
    with pytest.raises(FileNotFoundError):
        with tmp_target.open("baz"):
            pass


def test_cache(tmp_cache):
    assert not tmp_cache.exists("foo")
    with tmp_cache.open("foo", mode="w") as f:
        f.write("bar")
    assert tmp_cache.exists("foo")
    assert tmp_cache.size("foo") == 3
    with tmp_cache.open("foo", mode="r") as f:
        assert f.read() == "bar"
    tmp_cache.rm("foo")
    assert not tmp_cache.exists("foo")


def test_metadata_target(tmp_metadata_target):
    data = {"foo": 1, "bar": "baz"}
    tmp_metadata_target["key1"] = data
    assert tmp_metadata_target["key1"] == data
    assert tmp_metadata_target.getitems(["key1"]) == {"key1": data}


@pytest.mark.parametrize(
    "file_paths", [lazy_fixture("netcdf_local_paths"), lazy_fixture("netcdf_http_paths")]
)
@pytest.mark.parametrize("copy_to_local", [False, True])
@pytest.mark.parametrize("use_cache, cache_first", [(False, False), (True, False), (True, True)])
def test_file_opener(file_paths, tmp_cache, copy_to_local, use_cache, cache_first):
    all_paths, _ = file_paths
    path = str(all_paths[0])

    cache = tmp_cache if use_cache else None
    if cache_first:
        cache.cache_file(path)
        assert cache.exists(path)
        details = cache.fs.ls(cache.root_path, detail=True)
        cache.cache_file(path)
        # check that nothing happened
        assert cache.fs.ls(cache.root_path, detail=True) == details
    opener = file_opener(path, cache, copy_to_local=copy_to_local)
    if use_cache and not cache_first:
        with pytest.raises(FileNotFoundError):
            with opener as fp:
                pass
    else:
        with opener as fp:
            if copy_to_local:
                assert isinstance(fp, str)
                with open(fp, mode="rb") as fp2:
                    _ = fp2.read()
            else:
                _ = fp.read()
