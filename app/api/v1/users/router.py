from fastapi import APIRouter

from app.api.v1.users import controller

router = APIRouter(prefix="/users", tags=["Users"])

router.add_api_route("/", controller.list_users, methods=["GET"])
router.add_api_route("/", controller.create_user, methods=["POST"])
router.add_api_route("/{user_id}", controller.get_user, methods=["GET"])
router.add_api_route("/{user_id}", controller.update_user, methods=["PUT"])
router.add_api_route("/{user_id}", controller.delete_user, methods=["DELETE"])
