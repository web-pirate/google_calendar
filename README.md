# Calendar Application

A Google Calendar-inspired web application built with Django, Bootstrap 5, and FullCalendar.

## Setup and Installation

1. Clone the repository
2. Install Python dependencies:

```bash
pip install django
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start development server:

```bash
python manage.py runserver
```

5. Visit http://localhost:8000 in your browser

## Architecture & Technology Choices

### Frontend Stack

- **Bootstrap 5**: For responsive UI components and layout
- **FullCalendar 6.x**: Professional-grade calendar library
- **Vanilla JavaScript**: No additional framework dependencies
- **Bootstrap Icons**: For consistent iconography

### Backend Stack

- **Django**: Python web framework for future API integration
- **SQLite**: Default database (can be scaled to PostgreSQL)

### External APIs Integrated

- **Open-Meteo API**: Weather forecasting
- **Nager.Date API**: Public holidays data

## Business Logic & Edge Cases

### Calendar Events

- **Event Types**: Personal, Work, and Holidays
- **Event Properties**:
  - Title, Start/End times
  - All-day flag
  - Calendar category
  - Description
  - Unique ID generation

### Edge Cases Handled

1. **Date Handling**

   - Timezone-aware datetime handling
   - All-day vs timed events
   - Cross-day events

2. **Event Management**

   - Duplicate event prevention
   - Invalid date range validation
   - Event source toggling

3. **Holiday Integration**

   - Year boundary handling
   - Cached holiday data
   - API failure fallback

4. **Weather Integration**
   - Location-based weather
   - Future date forecasts
   - API error handling

## Animations & Interactions

### UI Components

1. **Theme Switching**

   - Smooth dark/light mode transition
   - Persistent theme preference
   - System theme detection

2. **Calendar Interactions**

   - Drag-and-drop event moving
   - Event resizing
   - View transitions
   - Modal animations

3. **Responsive Design**
   - Sidebar collapse on mobile
   - Touch-friendly controls
   - Adaptive layout

## Future Enhancements

1. **Feature Additions**

   - Event recurrence patterns
   - Guest invitations
   - Email notifications
   - Calendar sharing
   - Event attachments
   - Custom calendar colors

2. **Technical Improvements**

   - Backend API implementation
   - Real-time updates (WebSocket)
   - Event caching
   - Offline support
   - Multi-language support
   - Calendar import/export

3. **Integration Options**

   - Google Calendar sync
   - Microsoft Outlook sync
   - Task management
   - Meeting room booking
   - Video conferencing

4. **Performance Optimizations**
   - Event lazy loading
   - Image optimization
   - Network caching
   - Bundle size reduction

## Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request
