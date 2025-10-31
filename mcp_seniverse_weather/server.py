import os
from typing import Any, Dict
import requests
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

# 格式化单条气象预警信息为可读字符串
def format_alert(feature: dict) -> str:
    """将单条预警 feature 格式化为可读字符串。"""
    props = feature["now"]
    return f"""
Text: {props.get('text', 'Unknown')}
Code: {props.get('code', 'Unknown')}
temperature: {props.get('temperature', 'Unknown')}
feels_like: {props.get('feels_like', 'No feels_like available')}
pressure: {props.get('pressure', 'No specific pressure provided')}
"""

@mcp.tool()
def current_weather(city: str) -> str:
    api_key = os.getenv("SENIVERSE_API_KEY")
    
    if not api_key:
        raise ValueError("SENIVERSE_API_KEY environment variable is required")
    
    try:
        weather_response = requests.get(
            "https://api.seniverse.com/v3/weather/now.json",
            params={
                "key": api_key,
                "location": city,
                "language": "zh-Hans",
                "unit": "c"
            }
        )
        weather_response.raise_for_status()
        data = weather_response.json()
        
        if not data or "results" not in data:
            return "无法获取天气信息。"

        if not data["results"]:
            return "该城市暂无有效具体详情。"

        alerts = [format_alert(feature) for feature in data["results"]]
        return "\n---\n".join(alerts)
        # results = data["results"]
        
        # if not results:
        #     return {"error": f"Could not find weather data for city: {city}"}
        # return results
    except requests.exceptions.RequestException as e:
        error_message = f"Weather API error: {str(e)}"
        if hasattr(e,'response') and e.response is not None:
            try:
                error_data = e.response.json()
                if 'message' in error_data:
                    error_message = f"Weather API error: {error_data['message']}"
            except ValueError:
                pass
        return {"error": error_message}