const DEMO_TOKEN = 'fake-token';

const output = (selector, value) => {
    const element = document.querySelector(selector);
    if (element) {
        element.textContent = typeof value === 'string' ? value : JSON.stringify(value, null, 2);
    }
};

const setBusy = (button, busy) => {
    if (!button) {
        return;
    }
    button.disabled = busy;
    button.dataset.originalText = button.dataset.originalText || button.textContent;
    button.textContent = busy ? 'Loading...' : button.dataset.originalText;
};

const requestJson = async (url, options = {}) => {
    const response = await fetch(url, {
        headers: {
            Accept: 'application/json',
            ...(options.auth ? { Authorization: `Bearer ${DEMO_TOKEN}` } : {}),
            ...options.headers,
        },
        ...options,
    });

    if (!response.ok) {
        let message = `Request failed: ${response.status}`;
        try {
            const body = await response.json();
            message = body.detail || message;
        } catch {
            message = await response.text() || message;
        }
        throw new Error(message);
    }

    return response.json();
};

const bindApiButton = (selector, outputSelector, requestFactory) => {
    const button = document.querySelector(selector);
    button?.addEventListener('click', async () => {
        setBusy(button, true);
        try {
            output(outputSelector, await requestFactory());
        } catch (error) {
            output(outputSelector, { error: error.message });
        } finally {
            setBusy(button, false);
        }
    });
};

const initNavigation = () => {
    const navItems = Array.from(document.querySelectorAll('.course-nav-item'));

    navItems.forEach((item) => {
        item.addEventListener('click', () => {
            navItems.forEach((navItem) => navItem.classList.remove('active'));
            item.classList.add('active');
        });
    });
};

const initPracticeLab = () => {
    bindApiButton('#btn-current-user', '#current-user-output', () => {
        return requestJson('/users/me', { auth: true });
    });

    bindApiButton('#btn-user-id', '#user-id-output', () => {
        const userId = document.querySelector('#user-id-input')?.value?.trim() || '1';
        return requestJson(`/users/${encodeURIComponent(userId)}`, { auth: true });
    });

    bindApiButton('#btn-all-users', '#all-users-output', () => {
        return requestJson('/users');
    });

    bindApiButton('#btn-model', '#model-output', () => {
        const model = document.querySelector('#model-select')?.value || 'alexnet';
        return requestJson(`/models/${encodeURIComponent(model)}`);
    });

    bindApiButton('#btn-health', '#health-output', () => {
        return requestJson('/status');
    });
};

const init = () => {
    initNavigation();
    initPracticeLab();
    output('#current-user-output', 'Click the button to call /users/me with the demo bearer token.');
    output('#user-id-output', 'Tip: user id 1 succeeds, other ids show a 404 validation lesson.');
    output('#all-users-output', 'Click the button to list the sample learner records.');
    output('#model-output', 'Choose a model name to see path parameter validation in action.');
    output('#health-output', 'Click the button to confirm the FastAPI app is running.');
};

if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
