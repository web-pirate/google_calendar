from django.shortcuts import render  # already present in the file; keep it
import json
import traceback
import logging
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

from .models import Event

logger = logging.getLogger(__name__)


def calendar_view(request):
    """
    Renders the main calendar UI.
    Template expected at: core/templates/core/calendar.html
    """
    return render(request, "core/calendar.html")


def event_to_dict(ev: Event):
    return {
        "id": ev.id,
        "title": ev.title,
        "start": ev.start.isoformat() if ev.start else None,
        "end": ev.end.isoformat() if ev.end else None,
        "allDay": ev.all_day,
        "description": ev.description,
        "color": ev.color,
        "location": ev.location,
        "recurrence": ev.recurrence,
    }


@require_http_methods(["GET"])
def events_list(request):
    """
    Returns events intersecting the requested start/end window.
    FullCalendar calls with `start` and `end` query params (ISO8601).
    """
    try:
        start = request.GET.get("start")
        end = request.GET.get("end")

        # If no start/end provided, return all events (only ok for small DBs)
        if not start or not end:
            events = Event.objects.all()
            return JsonResponse([event_to_dict(e) for e in events], safe=False)

        # Try ISO datetime parse
        start_dt = parse_datetime(start)
        end_dt = parse_datetime(end)

        # If parse_datetime failed, accept YYYY-MM-DD and convert
        if start_dt is None:
            try:
                if len(start) == 10:
                    start_dt = datetime.fromisoformat(start + "T00:00:00")
            except Exception:
                start_dt = None
        if end_dt is None:
            try:
                if len(end) == 10:
                    end_dt = datetime.fromisoformat(end + "T23:59:59")
            except Exception:
                end_dt = None

        if start_dt is None or end_dt is None:
            return HttpResponseBadRequest(
                "Invalid start or end datetime format; expected ISO8601 or YYYY-MM-DD"
            )

        # return events that intersect the requested window
        events = Event.objects.filter(end__gt=start_dt, start__lt=end_dt)
        data = [event_to_dict(e) for e in events]
        return JsonResponse(data, safe=False)

    except Exception as exc:
        logger.error("Error in events_list: %s\n%s",
                     exc, traceback.format_exc())
        return JsonResponse(
            {"error": "Server error while listing events", "details": str(exc)}, status=500
        )


# NOTE: csrf_exempt is present for easier local testing.
# For production, remove csrf_exempt and ensure your fetch() sends X-CSRFToken header.
@csrf_exempt
@require_http_methods(["POST"])
def event_create(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception as e:
        return HttpResponseBadRequest(f"Invalid JSON payload: {e}")

    title = payload.get("title", "Untitled")
    start_raw = payload.get("start")
    end_raw = payload.get("end")
    all_day = bool(payload.get("allDay", False))
    description = payload.get("description", "")
    color = payload.get("color", "#3788d8")
    location = payload.get("location", "")
    recurrence = payload.get("recurrence", "")

    # parse datetimes
    start = parse_datetime(start_raw) if start_raw else None
    end = parse_datetime(end_raw) if end_raw else None

    # Accept date-only strings (YYYY-MM-DD)
    if start is None and isinstance(start_raw, str) and len(start_raw) == 10:
        try:
            start = datetime.fromisoformat(start_raw + "T00:00:00")
        except Exception:
            start = None
    if end is None and isinstance(end_raw, str) and len(end_raw) == 10:
        try:
            end = datetime.fromisoformat(end_raw + "T23:59:59")
        except Exception:
            end = None

    if not (start and end):
        return HttpResponseBadRequest("start and end datetimes are required and must be valid ISO strings")

    ev = Event.objects.create(
        title=title,
        start=start,
        end=end,
        all_day=all_day,
        description=description,
        color=color,
        location=location,
        recurrence=recurrence,
        created_by=request.user if getattr(
            request, "user", None) and request.user.is_authenticated else None,
    )
    return JsonResponse(event_to_dict(ev), status=201)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def event_update(request, event_id):
    ev = get_object_or_404(Event, pk=event_id)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception as e:
        return HttpResponseBadRequest(f"Invalid JSON payload: {e}")

    # update allowed fields
    for fld in ("title", "description", "color", "location", "recurrence"):
        if fld in payload:
            setattr(ev, fld, payload[fld])

    # times
    if "start" in payload:
        dt = parse_datetime(payload["start"]) if payload["start"] else None
        if dt is None and isinstance(payload["start"], str) and len(payload["start"]) == 10:
            try:
                dt = datetime.fromisoformat(payload["start"] + "T00:00:00")
            except Exception:
                dt = None
        if dt:
            ev.start = dt

    if "end" in payload:
        dt = parse_datetime(payload["end"]) if payload["end"] else None
        if dt is None and isinstance(payload["end"], str) and len(payload["end"]) == 10:
            try:
                dt = datetime.fromisoformat(payload["end"] + "T23:59:59")
            except Exception:
                dt = None
        if dt:
            ev.end = dt

    if "allDay" in payload:
        ev.all_day = bool(payload["allDay"])

    ev.save()
    return JsonResponse(event_to_dict(ev))


@csrf_exempt
@require_http_methods(["DELETE"])
def event_delete(request, event_id):
    ev = get_object_or_404(Event, pk=event_id)
    ev.delete()
    return JsonResponse({"deleted": True})
