import pytest

from stifle import file_line_count
from stifle._cli import main

LONG_SRC = "x = 1\n\ny = 2\n"


@pytest.mark.parametrize(
    "src, expected",
    [
        ("", 0),
        ("x = 1\n", 1),
        ("x = 1", 1),
        ("x = 1\ny = 2", 2),
        ("\n\n\n", 3),
        ("# only a comment\n\nx = 1\n", 3),
        ('"""doc\n\nmore"""\n', 3),
        ("x = 1\r\ny = 2\r\n", 2),
    ],
)
def test_file_line_count_counts_physical_lines(src, expected):
    assert file_line_count(src) == expected


def _project(tmp_path, raw_max_file_lines, src=LONG_SRC):
    (tmp_path / "pyproject.toml").write_text(
        "[tool.stifle]\nmax-file-lines = %s\n" % raw_max_file_lines
    )
    f = tmp_path / "a.py"
    f.write_text(src)
    return f


def test_cli_max_file_lines_reports_and_exits_1(tmp_path, capsys):
    f = tmp_path / "a.py"
    f.write_text(LONG_SRC)
    assert main(["check", "--max-file-lines", "2", str(f)]) == 1
    out, err = capsys.readouterr()
    assert "%s: 3 lines (limit 2)" % f in out.splitlines()
    assert "1 file-length violations" in err


def test_cli_max_file_lines_exact_limit_passes(tmp_path, capsys):
    f = tmp_path / "a.py"
    f.write_text(LONG_SRC)
    assert main(["check", "--max-file-lines", "3", str(f)]) == 0
    out, err = capsys.readouterr()
    assert out == ""
    assert "0 file-length violations" in err


def test_cli_max_file_lines_measures_source_before_stripping(tmp_path):
    src = "# one\n# two\nx = 1\n"
    f = tmp_path / "a.py"
    f.write_text(src)
    assert main(["format", "--max-file-lines", "2", str(f)]) == 1
    assert f.read_text() == "x = 1\n"


def test_cli_max_file_lines_never_rewrites_clean_file(tmp_path):
    f = _project(tmp_path, 2)
    assert main(["format", str(f)]) == 1
    assert f.read_text() == LONG_SRC


def test_cli_config_max_file_lines_matches_flag(tmp_path, capsys):
    f = _project(tmp_path, 2)
    assert main(["check", str(f)]) == 1
    from_config = capsys.readouterr()
    assert main(["check", "--isolated", "--max-file-lines", "2", str(f)]) == 1
    assert capsys.readouterr() == from_config


def test_cli_max_file_lines_flag_beats_config(tmp_path):
    f = _project(tmp_path, 2)
    assert main(["check", "--max-file-lines", "3", str(f)]) == 0
    f = _project(tmp_path, 3)
    assert main(["check", "--max-file-lines", "2", str(f)]) == 1


def test_cli_isolated_ignores_config_max_file_lines(tmp_path, capsys):
    f = _project(tmp_path, 2)
    assert main(["check", "--isolated", str(f)]) == 0
    assert "file-length violations" not in capsys.readouterr().err


def test_cli_explicit_config_max_file_lines(tmp_path):
    cfg = tmp_path / "other.toml"
    cfg.write_text("[stifle]\nmax-file-lines = 2\n")
    f = tmp_path / "a.py"
    f.write_text(LONG_SRC)
    assert main(["check", "--config", str(cfg), str(f)]) == 1


@pytest.mark.parametrize(
    "value, message",
    [
        ('"7"', "max-file-lines must be an integer"),
        ("true", "max-file-lines must be an integer"),
        ("0", "max-file-lines must be at least 1, got 0"),
        ("-3", "max-file-lines must be at least 1, got -3"),
    ],
)
def test_cli_invalid_config_max_file_lines_errors(
    tmp_path, capsys, value, message
):
    f = _project(tmp_path, value)
    with pytest.raises(SystemExit) as exc:
        main(["check", str(f)])
    assert exc.value.code == 2
    assert message in capsys.readouterr().err


def test_cli_max_file_lines_invalid_value_rejected(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["check", "--max-file-lines", "0", "."])
    assert exc.value.code == 2
    assert "--max-file-lines must be at least 1" in capsys.readouterr().err


def test_cli_max_file_lines_flag_before_command(tmp_path):
    f = tmp_path / "a.py"
    f.write_text(LONG_SRC)
    assert main(["--max-file-lines", "2", "check", str(f)]) == 1


def test_cli_summary_counts_both_caps_separately(tmp_path, capsys):
    f = tmp_path / "a.py"
    f.write_text('def f():\n    """a\n    b\n    c"""\n')
    g = tmp_path / "b.py"
    g.write_text(LONG_SRC)
    argv = ["check", "--max-doc-lines", "2", "--max-file-lines", "3"]
    assert main([*argv, str(tmp_path)]) == 1
    out, err = capsys.readouterr()
    assert "%s: 4 lines (limit 3)" % f in out
    assert str(g) not in out
    assert "1 docstring violations, 1 file-length violations" in err


def test_cli_max_file_lines_reported_for_unparsable_file(tmp_path, capsys):
    f = tmp_path / "a.py"
    f.write_text("def f(:\n\n\n")
    assert main(["check", "--max-file-lines", "2", str(f)]) == 2
    out, err = capsys.readouterr()
    assert "%s: 3 lines (limit 2)" % f in out
    assert "cannot parse" in err
    assert "1 file-length violations" in err


def test_cli_max_file_lines_skips_excluded_paths(tmp_path, capsys):
    (tmp_path / "gen").mkdir()
    (tmp_path / "gen" / "big.py").write_text(LONG_SRC)
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "big.py").write_text(LONG_SRC)
    (tmp_path / "ok.py").write_text("x = 1\n")
    argv = ["check", "--max-file-lines", "2", "--exclude", "gen"]
    assert main([*argv, str(tmp_path)]) == 0
    assert "0 file-length violations" in capsys.readouterr().err
