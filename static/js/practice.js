function getEditorValue() {
  const hidden = document.getElementById('code-editor-value');
  if (window.monacoEditor) {
    return window.monacoEditor.getValue();
  }
  return hidden ? hidden.value : '';
}

function setEditorValue(value) {
  const hidden = document.getElementById('code-editor-value');
  const nextValue = value || '';

  if (window.monacoEditor) {
    window.monacoEditor.setValue(nextValue);
  }
  if (hidden) {
    hidden.value = nextValue;
  }
}

function getSafePythonPreview(code) {
  const nameAssignment = code.match(/^\s*name\s*=\s*(['"])(.*?)\1\s*$/m);
  if (nameAssignment && /^\s*print\s*\(\s*name\s*\)\s*$/m.test(code)) {
    return [nameAssignment[2]];
  }

  const printMatches = Array.from(code.matchAll(/print\s*\(\s*(['"])(.*?)\1\s*\)/g));
  if (printMatches.length) {
    return printMatches.map((match) => match[2]);
  }

  return null;
}

function runCode() {
  const output = document.getElementById('code-output');
  const container = document.getElementById('code-editor');
  const code = getEditorValue().trim();

  if (!output || !container) {
    return;
  }
  if (!code) {
    output.textContent = 'Safe preview:\nWrite a solution before running the preview.';
    return;
  }

  const language = container.dataset.language;
  const preview = language === 'python' ? getSafePythonPreview(code) : null;
  if (preview) {
    output.textContent = `Safe preview (not executed):\n${preview.join('\n')}`;
    return;
  }

  output.textContent = 'Safe preview:\nThis example is not supported by the preview. Submit it to check your answer; code is not executed on the server.';
}

function resetCode() {
  const container = document.getElementById('code-editor');
  if (container) {
    setEditorValue(container.dataset.default || '');
  }
}

function showHint() {
  const container = document.getElementById('code-editor');
  if (container) {
    alert(container.dataset.hint || 'Review the lesson explanation and try a small change.');
  }
}

function showSolution() {
  const container = document.getElementById('code-editor');
  if (!container) {
    return;
  }

  if (container.dataset.solution) {
    setEditorValue(container.dataset.solution);
  } else {
    alert('Submit an attempt first to unlock the solution.');
  }
}

function markCodeAsUnverified() {
  const container = document.getElementById('code-editor');
  const feedback = document.getElementById('code-feedback');
  if (!container || !feedback) {
    return;
  }

  if (!container.classList.contains('code-check-error') && !container.classList.contains('code-check-success')) {
    return;
  }

  container.classList.remove('code-check-error', 'code-check-success');
  feedback.classList.remove('code-feedback-error', 'code-feedback-success');
  feedback.classList.add('code-feedback-neutral');
  feedback.textContent = 'Code changed. Submit again to re-check the required parts; code is not executed on the server.';
}

function initMonacoEditor() {
  const container = document.getElementById('code-editor');
  const hiddenField = document.getElementById('code-editor-value');
  if (!container || !hiddenField || typeof require !== 'function' || window.monacoEditor) {
    return;
  }

  const languages = {
    python: 'python',
    html: 'html',
    css: 'css',
    javascript: 'javascript',
    sql: 'sql',
    php: 'php',
    'linux-commands': 'shell',
    'git-and-github': 'shell',
  };
  require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.52.2/min/vs' } });
  require(['vs/editor/editor.main'], function () {
    window.monacoEditor = monaco.editor.create(container, {
      value: hiddenField.value,
      language: languages[container.dataset.language] || 'plaintext',
      theme: 'vs-dark',
      automaticLayout: true,
      minimap: { enabled: false },
      padding: { top: 16, bottom: 16 },
      fontSize: 14,
      lineNumbersMinChars: 3,
    });

    container.dataset.default = hiddenField.value;
    window.monacoEditor.onDidChangeModelContent(function () {
      hiddenField.value = window.monacoEditor.getValue();
      markCodeAsUnverified();
    });
  });
}

window.addEventListener('DOMContentLoaded', function () {
  const container = document.getElementById('code-editor');
  const hiddenField = document.getElementById('code-editor-value');
  if (container && hiddenField) {
    container.dataset.default = hiddenField.value;
  }
  if (hiddenField) {
    hiddenField.addEventListener('input', markCodeAsUnverified);
  }
  initMonacoEditor();
});
