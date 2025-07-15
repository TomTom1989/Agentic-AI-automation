import os

polygon_plan = os.getenv("POLYGON_PLAN")
is_paid_polygon = polygon_plan == "paid"
is_realtime_polygon = polygon_plan == "realtime" 