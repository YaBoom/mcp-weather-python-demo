from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP 服务器，服务名为 weather
mcp = FastMCP("weather-zhu")

# 常量：NWS API 基础地址和 User-Agent
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# 异步请求 NWS API，带异常处理，返回字典或 None
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """向 NWS API 发起请求，异常时返回 None。"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

# 格式化单条气象预警信息为可读字符串
def format_alert(feature: dict) -> str:
    """将单条预警 feature 格式化为可读字符串。"""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

# 工具函数：获取指定州的气象预警
@mcp.tool()
async def get_alerts(state: str) -> str:
    """获取美国某州的气象预警。
    参数：state - 两位州代码（如 CA, NY）
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "无法获取预警或无预警信息。"

    if not data["features"]:
        return "该州暂无有效预警。"

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

# 工具函数：获取指定经纬度的天气预报
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """获取指定位置的天气预报。
    参数：latitude - 纬度，longitude - 经度
    """
    # 先获取该点的 forecast 网格接口
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "无法获取该位置的预报数据。"

    # 从 points 响应中获取 forecast 详细预报 URL
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "无法获取详细预报信息。"

    # 格式化前 5 个时段的预报信息
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # 只显示最近 5 个时段
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

if __name__ == "__main__":
    # 启动 FastMCP 服务器，使用 stdio 作为通信方式
    mcp.run(transport='stdio')
