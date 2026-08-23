from scripts.release.certify_laptop import peak_rss


def test_peak_rss_parses_darwin_and_linux_time_formats() -> None:
    assert peak_rss("  12345  maximum resident set size\n","Darwin")==12345
    assert peak_rss("Maximum resident set size (kbytes): 12345\n","Linux")==12345*1024
