/**
 * Shared Family Calendar Card
*/

class SharedFamilyCalendarCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });

    this._hass = null;
    this._config = null;
    this._initialized = false;
  }

  static getStubConfig() {
    return {
      title: "Shared Family Calendar",
      calendar_entity: "calendar.shared_family_calendar",
    };
  }

  setConfig(config) {
    this._config = {
      title: "Shared Family Calendar",
      ...config,
    };
  }

  set hass(hass) {
    this._hass = hass;

    if (!this._initialized) {
      this._initialized = true;
      this._render();
    }

    this._render();
  }

  getCardSize() {
    return 4;
  }

  _render() {
    if (!this.shadowRoot || !this._hass || !this._config) {
      return;
    }

    const entityId = this._config.calendar_entity;
    const stateObj = this._hass.states[entityId];

    let content = "";

    if (!entityId) {
      content = `
        <div class="error">
          Keine Kalender-Entity konfiguriert.
        </div>
      `;
    } else if (!stateObj) {
      content = `
        <div class="error">
          Kalender nicht gefunden:<br>
          ${entityId}
        </div>
      `;
    } else {
      const message =
        stateObj.attributes.message ||
        stateObj.attributes.description ||
        "Keine aktuellen Termine";

      const location =
        stateObj.attributes.location || "";

      const start =
        stateObj.attributes.start_time || "";

      content = `
        <div class="event">
          <div class="event-title">
            ${stateObj.attributes.friendly_name || "Kalender"}
          </div>

          <div class="event-info">
            ${message}
          </div>

          ${
            location
              ? `<div class="event-location">📍 ${location}</div>`
              : ""
          }

          ${
            start
              ? `<div class="event-time">🕒 ${start}</div>`
              : ""
          }
        </div>
      `;
    }

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
        }

        ha-card {
          padding: 16px;
        }

        .title {
          font-size: 18px;
          font-weight: 600;
          margin-bottom: 12px;
        }

        .event {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .event-title {
          font-size: 16px;
          font-weight: 600;
        }

        .event-info,
        .event-location,
        .event-time {
          color: var(--secondary-text-color);
        }

        .error {
          color: var(--error-color);
          font-weight: 600;
        }
      </style>

      <ha-card>
        <div class="title">
          ${this._config.title}
        </div>

        ${content}
      </ha-card>
    `;
  }
}

customElements.define(
  "shared-family-calendar-card",
  SharedFamilyCalendarCard
);

window.customCards = window.customCards || [];

window.customCards.push({
  type: "custom:shared-family-calendar-card",
  name: "Shared Family Calendar",
  description: "Shared Family Calendar for Home Assistant",
  preview: true,
});
