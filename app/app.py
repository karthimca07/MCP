import os
import asyncio
from fastmcp import FastMCP
import asyncpg
from dotenv import load_dotenv

load_dotenv()  # Reads .env file

DB_HOST = os.getenv("PG_HOST")
DB_NAME = os.getenv("PG_DB")
DB_USER = os.getenv("PG_USER")
DB_PASS = os.getenv("PG_PASSWORD")
DB_PORT = 5432

mcp = FastMCP("Mini-Ecommerce MCP")

async def get_conn():
    return await asyncpg.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        ssl="require"
    )

# ---------- PRODUCTS ----------

@mcp.tool()
async def list_products(category: str | None = None):
    """List all products or filter by category"""
    conn = await get_conn()
    try:
        if category:
            rows = await conn.fetch(
                "SELECT * FROM products WHERE category=$1",
                category
            )
        else:
            rows = await conn.fetch("SELECT * FROM products")

        return [dict(r) for r in rows]
    finally:
        await conn.close()

@mcp.tool()

async def get_product(product_id: str):
    """Get product details"""
    conn = await get_conn()
    try:
        row = await conn.fetchrow(
            "SELECT * FROM products WHERE product_id=$1",
            product_id
        )
        return dict(row) if row else None
    finally:
        await conn.close()

# ---------- ORDERS ----------

@mcp.tool()
async def get_order(order_id: str):
    """Get order with items"""
    conn = await get_conn()
    try:
        order = await conn.fetchrow(
            "SELECT * FROM orders WHERE order_id=$1",
            order_id
        )
        if not order:
            return None

        items = await conn.fetch(
            "SELECT * FROM order_items WHERE order_id=$1",
            order_id
        )

        return {
            "order": dict(order),
            "items": [dict(i) for i in items]
        }
    finally:
        await conn.close()

@mcp.tool()
async def list_orders(customer_id: str):
    """List orders for a customer"""
    conn = await get_conn()
    try:
        rows = await conn.fetch(
            "SELECT * FROM orders WHERE customer_id=$1 ORDER BY created_at DESC",
            customer_id
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@mcp.tool()
async def health_check():
    """Simple health check tool"""
    return {"status": "ok"} 

# # ---------- SERVER ----------

# if __name__ == "__main__":
#     # IMPORTANT: HTTP transport for APIM
#     mcp.run(transport="streamable-http")