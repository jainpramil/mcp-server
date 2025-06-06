from mcp.server.fastmcp import FastMCP
from typing import List
from fastapi import FastAPI  # Import FastAPI
import requests

# In-memory mock database
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 10, "history": []}
}

# Create FastAPI and FastMCP app
app = FastAPI()
mcp = FastMCP("LeaveManager", app=app)

@app.get("/")
def root():
    return {"message": "Welcome to the Leave Manager MCP API"}

@app.get("/leave_balance/{employee_id}")
def leave_balance(employee_id: str):
    return {"result": get_leave_balance(employee_id)}

@app.get("/apply_leave/{employee_id}")
def apply_leave(employee_id: str):
    return {"result": get_apply_leave(employee_id,[])}


@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    data = employee_leaves.get(employee_id)
    if data:
        return f"{employee_id} has {data['balance']} leave days remaining."
    return "Employee ID not found."

@mcp.tool()
def get_apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    if employee_id not in employee_leaves:
        return "Employee ID not found."
    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]
    if available_balance < requested_days:
        return f"Insufficient leave balance. You requested {requested_days} day(s) but have only {available_balance}."
    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)
    return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_id]['balance']}."

@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    data = employee_leaves.get(employee_id)
    if data:
        history = ', '.join(data['history']) if data['history'] else "No leaves taken."
        return f"Leave history for {employee_id}: {history}"
    return "Employee ID not found."

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}! How can I assist you with leave management today?"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
