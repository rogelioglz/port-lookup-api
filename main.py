import os
import secrets
from datetime import datetime

import stripe
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# ============================================================
# CONFIGURACIÓN
# ============================================================

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
PUBLIC_BASE_URL = os.getenv(
    "PUBLIC_BASE_URL",
    "https://much-plane-silver-wrist.trycloudflare.com"
)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./port_lookup.db"
)
ADMIN_KEY = os.getenv("ADMIN_KEY")

if not STRIPE_SECRET_KEY:
    raise RuntimeError("Falta STRIPE_SECRET_KEY en .env")

stripe.api_key = STRIPE_SECRET_KEY

# ============================================================
# DATABASE
# ============================================================

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    plan = Column(String(50), nullable=False)
    queries_limit = Column(Integer, nullable=False)
    queries_used = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    stripe_session_id = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    plan = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(10), default="mxn")
    status = Column(String(50), default="pending")
    api_key = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)

# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Port & Service Lookup API",
    version="2.0.0"
)

# ============================================================
# PUERTOS
# ============================================================

PORTS_DB = {
<<<<<<< Updated upstream
    20: {"service": "FTP-DATA", "protocol": "TCP", "risk": "Medio", "desc": "Transferencia de datos FTP no cifrada."},
    21: {"service": "FTP", "protocol": "TCP", "risk": "Alto", "desc": "Control FTP."},
    22: {"service": "SSH", "protocol": "TCP", "risk": "Bajo", "desc": "Secure Shell."},
    23: {"service": "TELNET", "protocol": "TCP", "risk": "Alto", "desc": "Consola remota sin cifrado."},
    25: {"service": "SMTP", "protocol": "TCP", "risk": "Medio", "desc": "Envio de correo."},
    53: {"service": "DNS", "protocol": "TCP/UDP", "risk": "Bajo", "desc": "Domain Name System."},
    80: {"service": "HTTP", "protocol": "TCP", "risk": "Medio", "desc": "Trafico web no cifrado."},
    443: {"service": "HTTPS", "protocol": "TCP", "risk": "Bajo", "desc": "Trafico web cifrado SSL/TLS."},
    445: {"service": "SMB", "protocol": "TCP", "risk": "Alto", "desc": "Comparticion de archivos Windows."},
    3306: {"service": "MySQL", "protocol": "TCP", "risk": "Medio", "desc": "Base de datos MySQL."},
    3389: {"service": "RDP", "protocol": "TCP", "risk": "Alto", "desc": "Remote Desktop Protocol."},
    8080: {"service": "HTTP-ALT", "protocol": "TCP", "risk": "Medio", "desc": "Servidor web alternativo."}
=======
    20: {
        "service": "FTP-Data",
        "protocol": "TCP",
        "description": "FTP data transfer"
    },
    21: {
        "service": "FTP",
        "protocol": "TCP",
        "description": "File Transfer Protocol"
    },
    22: {
        "service": "SSH",
        "protocol": "TCP",
        "description": "Secure Shell"
    },
    23: {
        "service": "Telnet",
        "protocol": "TCP",
        "description": "Telnet"
    },
    25: {
        "service": "SMTP",
        "protocol": "TCP",
        "description": "Simple Mail Transfer Protocol"
    },
    53: {
        "service": "DNS",
        "protocol": "TCP/UDP",
        "description": "Domain Name System"
    },
    80: {
        "service": "HTTP",
        "protocol": "TCP",
        "description": "Hypertext Transfer Protocol"
    },
    443: {
        "service": "HTTPS",
        "protocol": "TCP",
        "description": "Secure HTTP"
    },
    445: {
        "service": "SMB",
        "protocol": "TCP",
        "description": "Server Message Block"
    },
    3306: {
        "service": "MySQL",
        "protocol": "TCP",
        "description": "MySQL database"
    },
    3389: {
        "service": "RDP",
        "protocol": "TCP",
        "description": "Remote Desktop Protocol"
    }
>>>>>>> Stashed changes
}

# ============================================================
# PLANES
# ============================================================

PLANS = {
    "starter": {
        "name": "Starter",
        "price_mxn": 99,
        "queries": 1000
    },
    "pro": {
        "name": "Pro",
        "price_mxn": 299,
        "queries": 5000
    },
    "business": {
        "name": "Business",
        "price_mxn": 599,
        "queries": 20000
    }
}

# ============================================================
# HEALTH
# ============================================================

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Port & Service Lookup API",
        "version": "2.0.0"
    }


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "port-lookup-api",
        "stripe_configured": bool(STRIPE_SECRET_KEY),
        "webhook_configured": bool(STRIPE_WEBHOOK_SECRET)
    }

# ============================================================
# PLANES
# ============================================================

@app.get("/plans")
def get_plans():
    return {
        "currency": "MXN",
        "plans": PLANS
    }

# ============================================================
# CONSULTA DE PUERTO
# ============================================================

@app.get("/api/v1/ports")
def get_ports():
    return {
        "count": len(PORTS_DB),
        "ports": PORTS_DB
    }


@app.get("/api/v1/port/{port_number}")
def get_port(port_number: int, request: Request):

    api_key = request.headers.get("X-API-Key")

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Falta el header X-API-Key"
        )

    db = SessionLocal()

    try:
        account = db.query(APIKey).filter(
            APIKey.key == api_key,
            APIKey.active == True
        ).first()

        if not account:
            raise HTTPException(
                status_code=401,
                detail="API Key inválida"
            )

        if account.queries_used >= account.queries_limit:
            raise HTTPException(
                status_code=429,
                detail="Límite de consultas alcanzado"
            )

        if port_number not in PORTS_DB:
            raise HTTPException(
                status_code=404,
                detail="Puerto no encontrado"
            )

        account.queries_used += 1
        db.commit()

        result = PORTS_DB[port_number]

        return {
            "port": port_number,
            "service": result["service"],
            "protocol": result["protocol"],
            "description": result["description"],
            "queries_used": account.queries_used,
            "queries_remaining": (
                account.queries_limit -
                account.queries_used
            )
        }

    finally:
        db.close()

# ============================================================
# CUENTA
# ============================================================

@app.get("/api/v1/account")
def account_info(request: Request):

    api_key = request.headers.get("X-API-Key")

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Falta el header X-API-Key"
        )

    db = SessionLocal()

    try:
        account = db.query(APIKey).filter(
            APIKey.key == api_key,
            APIKey.active == True
        ).first()

        if not account:
            raise HTTPException(
                status_code=401,
                detail="API Key inválida"
            )

        return {
            "plan": account.plan,
            "api_key": account.key,
            "queries_limit": account.queries_limit,
            "queries_used": account.queries_used,
            "queries_remaining": (
                account.queries_limit -
                account.queries_used
            ),
            "active": account.active
        }

    finally:
        db.close()

# ============================================================
# CREAR CHECKOUT
# ============================================================

@app.post("/checkout")
def create_checkout(plan: str = "starter"):

    if plan not in PLANS:
        raise HTTPException(
            status_code=400,
            detail="Plan inválido"
        )

    selected = PLANS[plan]

    try:

        session = stripe.checkout.Session.create(

            mode="payment",

            line_items=[
                {
                    "price_data": {
                        "currency": "mxn",

                        "product_data": {
                            "name": (
                                f"Port Lookup API - "
                                f"{selected['name']}"
                            ),
                            "description": (
                                f"{selected['queries']} "
                                "consultas de puertos"
                            )
                        },

                        "unit_amount": (
                            selected["price_mxn"] * 100
                        )
                    },

                    "quantity": 1
                }
            ],

            metadata={
                "plan": plan
            },

            success_url=(
                f"{PUBLIC_BASE_URL}"
                "/checkout/success"
                "?session_id={CHECKOUT_SESSION_ID}"
            ),

            cancel_url=(
                f"{PUBLIC_BASE_URL}"
                "/checkout/cancel"
            )
        )

        db = SessionLocal()

        try:

            order = Order(
                stripe_session_id=session.id,
                plan=plan,
                amount=selected["price_mxn"],
                currency="mxn",
                status="pending"
            )

            db.add(order)
            db.commit()

        finally:
            db.close()

        return {
            "ok": True,
            "plan": plan,
            "price_mxn": selected["price_mxn"],
            "checkout_session_id": session.id,
            "checkout_url": session.url
        }

    except stripe.StripeError as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# Alias
@app.post("/create-checkout-session")
def create_checkout_session(plan: str = "starter"):
    return create_checkout(plan)

# ============================================================
# CHECKOUT SUCCESS
# ============================================================

@app.get("/checkout/success")
def checkout_success(session_id: str | None = None):

    if not session_id:
        return {
            "ok": True,
            "message": "Pago recibido"
        }

    db = SessionLocal()

    try:

        order = db.query(Order).filter(
            Order.stripe_session_id == session_id
        ).first()

        if not order:
            return {
                "ok": True,
                "message": "Pago recibido"
            }

        return {
            "ok": True,
            "message": "Pago recibido",
            "status": order.status,
            "plan": order.plan
        }

    finally:
        db.close()

# ============================================================
# CHECKOUT CANCEL
# ============================================================

@app.get("/checkout/cancel")
def checkout_cancel():

    return {
        "ok": False,
        "message": "El pago fue cancelado"
    }

# ============================================================
# STRIPE WEBHOOK
# ============================================================

@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):

    payload = await request.body()

    signature = request.headers.get(
        "stripe-signature"
    )

    if not signature:
        raise HTTPException(
            status_code=400,
            detail="Falta Stripe-Signature"
        )

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Falta STRIPE_WEBHOOK_SECRET"
        )

    try:

        event = stripe.Webhook.construct_event(
            payload,
            signature,
            STRIPE_WEBHOOK_SECRET
        )

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail="Payload inválido"
        )

    except stripe.error.SignatureVerificationError:

        raise HTTPException(
            status_code=400,
            detail="Firma Stripe inválida"
        )

    event_type = event["type"]

    # --------------------------------------------------------
    # PAGO COMPLETADO
    # --------------------------------------------------------

    if event_type in [
        "checkout.session.completed",
        "checkout.session.async_payment_succeeded"
    ]:

        session = event["data"]["object"]

        session_id = session.get("id")

        if not session_id:
            return {
                "received": True
            }

        db = SessionLocal()

        try:

            order = db.query(Order).filter(
                Order.stripe_session_id == session_id
            ).first()

            if not order:
                return {
                    "received": True,
                    "message": "Orden no encontrada"
                }

            # Idempotencia:
            # si ya fue procesada, no crear otra API key
            if order.status == "paid" and order.api_key:

                return {
                    "received": True,
                    "message": "Orden ya procesada"
                }

            plan = PLANS.get(order.plan)

            if not plan:
                order.status = "error"
                db.commit()

                return {
                    "received": True,
                    "message": "Plan no encontrado"
                }

            # Crear API KEY
            new_api_key = (
                "plk_live_" +
                secrets.token_urlsafe(32)
            )

            account = APIKey(
                key=new_api_key,
                plan=order.plan,
                queries_limit=plan["queries"],
                queries_used=0,
                active=True
            )

            db.add(account)

            order.status = "paid"
            order.api_key = new_api_key

            db.commit()

        finally:
            db.close()

    return {
        "received": True
    }

# ============================================================
# ADMIN
# ============================================================

@app.get("/admin/stats")
def admin_stats(request: Request):

    provided_key = request.headers.get(
        "X-Admin-Key"
    )

    if not ADMIN_KEY:
        raise HTTPException(
            status_code=500,
            detail="ADMIN_KEY no configurada"
        )

    if provided_key != ADMIN_KEY:
        raise HTTPException(
            status_code=401,
            detail="No autorizado"
        )

    db = SessionLocal()

    try:

        accounts = db.query(APIKey).count()
        orders = db.query(Order).count()
        paid_orders = db.query(Order).filter(
            Order.status == "paid"
        ).count()

        return {
            "accounts": accounts,
            "orders": orders,
            "paid_orders": paid_orders
        }

    finally:
        db.close()































