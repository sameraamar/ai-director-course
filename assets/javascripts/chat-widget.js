(function () {
  const config = window.__AI_DIRECTOR_CHAT_CONFIG__ || {};
  const apiUrl = config.apiUrl || 'http://127.0.0.1:8001/api/chat';
  const launcherLabel = config.launcherLabel || 'Ask the course assistant';
  const panelTitle = config.panelTitle || 'Course Assistant';
  const greeting = config.greeting || 'Ask about the current lesson, workflow, or sprint steps.';

  function buildWidget() {
    const root = document.createElement('div');
    root.className = 'ai-chat-widget';

    const panel = document.createElement('section');
    panel.className = 'ai-chat-widget__panel';
    panel.setAttribute('aria-label', panelTitle);

    const header = document.createElement('div');
    header.className = 'ai-chat-widget__header';

    const title = document.createElement('div');
    title.className = 'ai-chat-widget__title';
    title.textContent = panelTitle;

    const close = document.createElement('button');
    close.type = 'button';
    close.className = 'ai-chat-widget__close';
    close.setAttribute('aria-label', 'Close course assistant');
    close.textContent = '✕';

    const messages = document.createElement('div');
    messages.className = 'ai-chat-widget__messages';

    const form = document.createElement('form');
    form.className = 'ai-chat-widget__form';

    const input = document.createElement('input');
    input.className = 'ai-chat-widget__input';
    input.name = 'question';
    input.placeholder = 'Ask a question about the sprint';
    input.autocomplete = 'off';
    input.setAttribute('aria-label', 'Ask a question about the sprint');

    const submit = document.createElement('button');
    submit.type = 'submit';
    submit.className = 'ai-chat-widget__submit';
    submit.textContent = 'Send';

    const status = document.createElement('div');
    status.className = 'ai-chat-widget__status';
    status.textContent = '';

    const launcher = document.createElement('button');
    launcher.type = 'button';
    launcher.className = 'ai-chat-widget__launcher';
    launcher.textContent = launcherLabel;
    launcher.setAttribute('aria-expanded', 'false');

    header.append(title, close);
    form.append(input, submit);
    panel.append(header, messages, form, status);
    root.append(panel, launcher);
    document.body.append(root);

    return { root, panel, messages, form, input, submit, status, launcher, close };
  }

  function appendParagraph(container, text) {
    const paragraph = document.createElement('p');
    paragraph.textContent = text;
    container.appendChild(paragraph);
  }

  function renderAssistantBody(container, text) {
    const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
    const bulletLines = lines.filter((line) => line.startsWith('- '));
    const paragraphLines = lines.filter((line) => !line.startsWith('- '));

    paragraphLines.forEach((line) => appendParagraph(container, line));

    if (bulletLines.length) {
      const list = document.createElement('ul');
      bulletLines.forEach((line) => {
        const item = document.createElement('li');
        item.textContent = line.slice(2);
        list.appendChild(item);
      });
      container.appendChild(list);
    }
  }

  function slugifyHeading(text) {
    return text
      .toLowerCase()
      .normalize('NFKD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s-]/g, '')
      .trim()
      .replace(/\s+/g, '-');
  }

  function citationToUrl(citation) {
    const [path, heading] = citation.split('#');
    if (!path || !path.startsWith('course/')) {
      return null;
    }

    const page = path.replace(/^course\//, '').replace(/index\.md$/, '').replace(/\.md$/, '/');
    const href = '/' + page;
    if (!heading) {
      return href;
    }
    return href + '#' + slugifyHeading(heading);
  }

  function appendCitations(container, citations) {
    if (!citations || !citations.length) {
      return;
    }

    const wrapper = document.createElement('div');
    wrapper.className = 'ai-chat-widget__citations';

    citations.forEach((citation) => {
      const url = citationToUrl(citation);
      if (url) {
        const link = document.createElement('a');
        link.className = 'ai-chat-widget__citation';
        link.href = url;
        link.textContent = citation;
        wrapper.appendChild(link);
      } else {
        const label = document.createElement('span');
        label.className = 'ai-chat-widget__citation-label';
        label.textContent = citation;
        wrapper.appendChild(label);
      }
    });

    container.appendChild(wrapper);
  }

  function appendMessage(messages, role, text, citations) {
    const message = document.createElement('div');
    message.className = 'ai-chat-widget__message ai-chat-widget__message--' + role;

    if (role === 'assistant') {
      renderAssistantBody(message, text);
      appendCitations(message, citations || []);
    } else {
      appendParagraph(message, text);
    }

    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
  }

  async function sendQuestion(elements, question) {
    elements.submit.disabled = true;
    elements.status.textContent = 'Thinking…';

    appendMessage(elements.messages, 'user', question);

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question, user_mode: 'learner' })
      });

      if (!response.ok) {
        throw new Error('Request failed with status ' + response.status);
      }

      const payload = await response.json();
      appendMessage(elements.messages, 'assistant', payload.answer || 'No response received.', payload.citations || []);
      elements.status.textContent = payload.answer_source === 'gemini_grounded'
        ? 'Gemini grounded answer received.'
        : payload.answer_source === 'local_grounded'
          ? 'Local grounded answer received.'
          : payload.answer_source === 'gemini_scoped'
            ? 'Gemini scoped answer received without repository citations.'
            : 'The assistant could not ground that question in the current repository.';
    } catch (error) {
      appendMessage(
        elements.messages,
        'assistant',
        'The assistant is temporarily unavailable. Please try again or continue with the lesson content.',
        []
      );
      elements.status.textContent = 'Request failed. Try again in a moment.';
    } finally {
      elements.submit.disabled = false;
    }
  }

  function initializeWidget() {
    const elements = buildWidget();
    appendMessage(elements.messages, 'assistant', greeting, []);

    const setOpen = (open) => {
      elements.panel.classList.toggle('is-open', open);
      elements.launcher.setAttribute('aria-expanded', String(open));
      if (open) {
        elements.input.focus();
      }
    };

    elements.launcher.addEventListener('click', function () {
      setOpen(!elements.panel.classList.contains('is-open'));
    });

    elements.close.addEventListener('click', function () {
      setOpen(false);
    });

    elements.form.addEventListener('submit', function (event) {
      event.preventDefault();
      const question = elements.input.value.trim();
      if (!question) {
        elements.status.textContent = 'Enter a question before sending.';
        return;
      }
      elements.input.value = '';
      void sendQuestion(elements, question);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeWidget);
  } else {
    initializeWidget();
  }
})();
