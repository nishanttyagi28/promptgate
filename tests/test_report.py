import pytest
from pathlib import Path
from app.report import write_html

def test_write_html(tmp_path):
    """Test that write_html creates a valid HTML file with the expected content."""
    results = [
        {"id": "1", "passed": True, "expect": "Expected output", "snippet": "Output snippet"},
        {"id": "2", "passed": False, "expect": "Another expected output", "snippet": "Another snippet"}
    ]
    report_path = tmp_path / "report.html"
    
    write_html(results, report_path)
    
    assert report_path.exists()
    content = report_path.read_text()
    assert "<title>Evaluation Report</title>" in content
    assert "<td>1</td>" in content
    assert "<td>True</td>" in content
    assert "<td>Expected output</td>" in content
    assert "<td>Output snippet</td>" in content
    assert "<td>2</td>" in content
    assert "<td>False</td>" in content
    assert "<td>Another expected output</td>" in content
    assert "<td>Another snippet</td>" in content