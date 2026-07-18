from fastapi import APIRouter

from api.database import SessionLocal
from api.models import Inspection

router = APIRouter()


def get_summary():

    db = SessionLocal()

    inspections = db.query(Inspection).all()

    total = len(inspections)

    passed = 0
    failed = 0
    missing = 0

    for inspection in inspections:

        if inspection.status == "PASS":
            passed += 1
        else:
            failed += 1

        missing += inspection.missing_eggs

    db.close()

    return {
        "total_inspections": total,
        "passed": passed,
        "failed": failed,
        "total_missing_eggs": missing
    }


router.add_api_route(
    path="/reports/summary",
    endpoint=get_summary,
    methods=["GET"]
)