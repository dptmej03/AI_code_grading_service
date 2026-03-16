import json
import zipfile
import tempfile
import os
import re
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from typing import List, Dict, Any, Optional, Tuple


def extract_notebooks_from_zip(zip_bytes: bytes) -> List[Tuple[str, bytes]]:
    """ZIP에서 모든 .ipynb 파일 추출. (filename, content_bytes) 리스트 반환."""
    result = []
    with zipfile.ZipFile(__import__('io').BytesIO(zip_bytes)) as zf:
        for info in zf.infolist():
            # Decode filename (handle encoding issues)
            try:
                name = info.filename.encode('cp437').decode('utf-8')
            except Exception:
                name = info.filename
            if name.endswith('.ipynb') and not name.startswith('__MACOSX'):
                content = zf.read(info.filename)
                # Use just the basename
                basename = os.path.basename(name)
                result.append((basename, content))
    return result


def parse_notebook(content: bytes) -> nbformat.NotebookNode:
    """ipynb 바이트를 파싱하여 노트북 객체 반환."""
    nb_str = content.decode('utf-8', errors='replace')
    return nbformat.reads(nb_str, as_version=4)


def extract_cell_outputs(nb: nbformat.NotebookNode) -> List[Dict[str, Any]]:
    """각 코드 셀의 출력값 추출."""
    cell_outputs = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            outputs = []
            for output in cell.get('outputs', []):
                output_type = output.get('output_type', '')
                if output_type == 'stream':
                    outputs.append({
                        'type': 'stream',
                        'name': output.get('name', ''),
                        'text': ''.join(output.get('text', []))
                    })
                elif output_type in ('display_data', 'execute_result'):
                    data = output.get('data', {})
                    text_repr = data.get('text/plain', '')
                    if isinstance(text_repr, list):
                        text_repr = ''.join(text_repr)
                    outputs.append({
                        'type': output_type,
                        'text': text_repr
                    })
                elif output_type == 'error':
                    outputs.append({
                        'type': 'error',
                        'ename': output.get('ename', ''),
                        'evalue': output.get('evalue', '')
                    })
            cell_outputs.append({
                'cell_index': i,
                'source': cell.source,
                'outputs': outputs
            })
    return cell_outputs


def execute_notebook(nb: nbformat.NotebookNode, timeout: int = 60) -> Tuple[nbformat.NotebookNode, Optional[str]]:
    """노트북을 실행하고 실행된 노트북과 에러 메시지 반환."""
    ep = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
    try:
        ep.preprocess(nb)
        return nb, None
    except Exception as e:
        return nb, str(e)


def extract_code_cells(nb: nbformat.NotebookNode) -> List[Dict[str, Any]]:
    """코드 셀 소스만 추출 (문제별 분리 없이 전체)."""
    cells = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and cell.source.strip():
            cells.append({
                'index': i,
                'source': cell.source
            })
    return cells


def parse_student_id_from_filename(filename: str) -> str:
    """파일명에서 학번/이름 파싱. 예: '20210001_홍길동.ipynb' → '20210001_홍길동'"""
    name = os.path.splitext(filename)[0]
    return name


def split_notebook_by_problems(nb: nbformat.NotebookNode) -> Dict[int, List[Dict[str, Any]]]:
    """
    마크다운 셀의 '## 문제 N' 또는 '# 문제 N' 패턴으로 문제별 셀 분리.
    반환: {problem_id: [cell_dict, ...]}
    """
    problems = {}
    current_problem = 0
    problem_cells = []

    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            m = re.search(r'(?:문제|Problem|Q|question)\s*[:#\s]*(\d+)', cell.source, re.IGNORECASE)
            if m:
                if current_problem > 0:
                    problems[current_problem] = problem_cells
                current_problem = int(m.group(1))
                problem_cells = []
            continue
        if cell.cell_type == 'code' and cell.source.strip():
            if current_problem > 0:
                problem_cells.append({
                    'source': cell.source,
                    'outputs': cell.get('outputs', [])
                })

    if current_problem > 0 and problem_cells:
        problems[current_problem] = problem_cells

    return problems
