class SharedCalendarCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._hass = null;
    this._config = null;
    this._events = [];
    this._loading = false;
    this._error = null;
  }

  static getConfigElement() {
    return document.createElement('div');
  }

  setConfig(config) {
    if (!config.calendar_entity) {
      throw new Error('You must define a calendar_entity');
    }

    this._config = {
      title: 'Shared Calendar',
      days: 7,
      max_events: 10,
      ...config,
    };
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
    this._updateEvents();
  }

  getCardSize() {
    return 4;
  }

  async _updateEvents() {
    if (!this._hass || !this._config || this._loading) {
      return;
    }

    this._loading = true;
    this._error = null;

    const start = new Date();
    const end = new Date();
    end.setDate(start.getDate() + this._config.days);

    try {
      const response = await this._hass.callApi(
        'GET',
        `/api/calendars/${encodeURIComponent(this._config.calendar_entity)}`,
        {
          start_time: start.toISOString(),
          end_time: end.toISOString(),
        }
      );

      this._events = Array.isArray(response) ? response : [];
    } catch (err) {
      this._error = err.message || String(err);
      this._events = [];
    } finally {
      this._loading = false;
      this._render();
    }
  }

  _render() {
    if (!this.shadowRoot) {
      return;
    }

    const title = this._config?.title || 'Shared Calendar';
    const loading = this._loading ? 'loading' : '';
    const events = this._events.slice(0, this._config?.max_events || 10);

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          font-family: var(--ha-card-font-family, inherit);
        }
        ha-card {
          padding: 16px;
          box-sizing: border-box;
        }
        .header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 16px;
        }
        .title {
          font-size: 1.1em;
          font-weight: 600;
          color: var(--primary-text-color);
        }
        .subtitle {
          color: var(--secondary-text-color);
          font-size: 0.9em;
        }
        .event {
          margin-bottom: 12px;
          padding-bottom: 12px;
          border-bottom: 1px solid var(--divider-color);
        }
        .event:last-child {
          border-bottom: none;
          margin-bottom: 0;
          padding-bottom: 0;
        }
        .event-title {
          font-weight: 600;
          color: var(--primary-text-color);
          margin: 0 0 4px 0;
        }
        .event-time,
        .event-location,
        .event-description {
          margin: 0;
          color: var(--secondary-text-color);
          font-size: 0.95em;
        }
        .error {
          color: var(--error-color);
          margin: 0;
          font-size: 0.95em;
        }
      </style>
      <ha-card>
        <div class="header">
          <div>
            <div class="title">${title}</div>
            <div class="subtitle">${this._config.calendar_entity}</div>
          </div>
          <div>${loading ? '⏳ Aktualisiere...' : ''}</div>
        </div>
        ${this._error ? `<p class="error">Fehler: ${this._error}</p>` : ''}
        ${events.length === 0 && !this._error ? '<p class="subtitle">Keine Termine gefunden.</p>' : ''}
        ${events
          .map((event) => {
            const start = new Date(event.start);
            const end = new Date(event.end);
            const time = `${start.toLocaleString()} – ${end.toLocaleTimeString()}`;
            return `
              <div class="event">
                <p class="event-title">${event.summary || 'Termin'}</p>
                <p class="event-time">${time}</p>
                ${event.location ? `<p class="event-location">📍 ${event.location}</p>` : ''}
                ${event.description ? `<p class="event-description">${event.description}</p>` : ''}
              </div>
            `;
          })
          .join('')}
      </ha-card>
    `;
  }
}

customElements.define('shared-calendar-card', SharedCalendarCard);
