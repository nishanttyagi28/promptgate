import os
from pathlib import Path

def write_html(results, path):
    """Generate an HTML report from evaluation results."""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Evaluation Report</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <h1>Evaluation Report</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Passed</th>
            <th>Expect</th>
            <th>Snippet</th>
        </tr>
    """
    
    for result in results:
        html += f"""
        <tr>
            <td>{result['id']}</td>
            <td>{result['passed']}</td>
            <td>{result['expect']}</td>
            <td>{result['snippet']}</td>
        </tr>
        """
    
    html += """
    </table>
</body>
</html>
    """
    
    # Ensure the reports directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Write the HTML report
    with open(path, 'w') as f:
        f.write(html)