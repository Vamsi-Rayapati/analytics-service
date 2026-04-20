from fastapi import APIRouter

from app.api.v1.events import controller

router = APIRouter(prefix="/events", tags=["Events"])

router.add_api_route("/", controller.list_events, methods=["GET"])
router.add_api_route("/", controller.create_event, methods=["POST"])
router.add_api_route("/{event_id}", controller.get_event, methods=["GET"])
