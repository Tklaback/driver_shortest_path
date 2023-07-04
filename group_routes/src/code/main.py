from fastapi import FastAPI
from app.api.endpoints import offboard
from app.api.endpoints import onboard
from mangum import Mangum

app = FastAPI(debug=True,
title="Employee Service Subscription Tool API",
description="This API opens endpoints that can be programatically used to automate account closures on various third party services.",
)

app.include_router(offboard.router, prefix="/api/v1/offboard", tags=["Offboard"])

handler = Mangum(app)