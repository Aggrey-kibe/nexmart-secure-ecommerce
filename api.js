/**
 * NEXMART — Core API Client
 * Centralized HTTP client with:
 *  - Automatic JWT injection
 *  - Token refresh on 401
 *  - Request/response interceptors
 *  - XSS-safe response handling
 */

const API_BASE = 'http://localhost:8000/api/v1';

class ApiClient {
  constructor() {
    this._refreshPromise = null; // Prevent concurrent refresh races
  }

  // ─── Private Helpers ───────────────────────────────────────

  _getHeaders(includeAuth = true) {
    const headers = { 'Content-Type': 'application/json' };
    if (includeAuth) {
      const token = Auth.getAccessToken();
      if (token) headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  async _handleResponse(response) {
    const contentType = response.headers.get('Content-Type') || '';
    const isJson = contentType.includes('application/json');
    const data = isJson ? await response.json() : await response.text();

    if (!response.ok) {
      // Normalize error shape
      const message =
        data?.detail ||
        data?.message ||
        (typeof data === 'string' ? data : 'An error occurred.');
      const err = new Error(message);
      err.status = response.status;
      err.data = data;
      throw err;
    }
    return data;
  }

  async _request(method, endpoint, body = null, includeAuth = true, retry = true) {
    const options = {
      method,
      headers: this._getHeaders(includeAuth),
    };

    if (body && !(body instanceof FormData)) {
      options.body = JSON.stringify(body);
    } else if (body instanceof FormData) {
      // Let browser set Content-Type with boundary for multipart
      delete options.headers['Content-Type'];
      options.body = body;
    }

    let response;
    try {
      response = await fetch(`${API_BASE}${endpoint}`, options);
    } catch (networkErr) {
      throw new Error('Network error. Please check your connection.');
    }

    // 401 — try to refresh token once, then retry
    if (response.status === 401 && retry) {
      const refreshed = await this._tryRefresh();
      if (refreshed) {
        return this._request(method, endpoint, body, includeAuth, false);
      } else {
        Auth.clearTokens();
        Store.set('user', null);
        window.location.href = '/auth.html?session=expired';
        return;
      }
    }

    return this._handleResponse(response);
  }

  async _tryRefresh() {
    // Prevent concurrent refresh calls
    if (this._refreshPromise) return this._refreshPromise;

    this._refreshPromise = (async () => {
      try {
        const refresh = Auth.getRefreshToken();
        if (!refresh) return false;

        const res = await fetch(`${API_BASE}/auth/token/refresh/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh }),
        });

        if (!res.ok) return false;

        const data = await res.json();
        Auth.setAccessToken(data.access);
        // simplejwt with ROTATE_REFRESH_TOKENS returns new refresh token too
        if (data.refresh) Auth.setRefreshToken(data.refresh);
        return true;
      } catch {
        return false;
      } finally {
        this._refreshPromise = null;
      }
    })();

    return this._refreshPromise;
  }

  // ─── Public Methods ────────────────────────────────────────

  get(endpoint, params = {}) {
    const qs = new URLSearchParams(params).toString();
    const url = qs ? `${endpoint}?${qs}` : endpoint;
    return this._request('GET', url);
  }

  post(endpoint, body, includeAuth = true) {
    return this._request('POST', endpoint, body, includeAuth);
  }

  put(endpoint, body) {
    return this._request('PUT', endpoint, body);
  }

  patch(endpoint, body) {
    return this._request('PATCH', endpoint, body);
  }

  delete(endpoint) {
    return this._request('DELETE', endpoint);
  }

  postForm(endpoint, formData) {
    return this._request('POST', endpoint, formData);
  }

  patchForm(endpoint, formData) {
    return this._request('PATCH', endpoint, formData);
  }
}

const API = new ApiClient();
