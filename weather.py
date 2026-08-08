import argparse
import json
import sys
import requests
from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"


def read_user_cli_args():
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description="gets weather informations for a city"
    )
    parser.add_argument(
        "city", nargs="+", type=str, help="enter the city name"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units",
    )
    return parser.parse_args()


def get_geocoding(city, limit=3):
    """获取城市的地理编码信息。

    Args:
        city: 城市名称
        limit: 返回结果的最大数量

    Returns:
        dict: 包含 'lat' 和 'lon' 的字典
    """
    payload = {'q': city, 'limit': limit, 'appid': OPENWEATHER_API_KEY}
    response = requests.get(BASE_GEOCODING_API_URL, params=payload)
    response.raise_for_status()
    geo_data = response.json()

    if not geo_data:
        raise ValueError(f"未找到城市 '{city}' 的地理信息")

    # 只有一个结果，直接返回
    if len(geo_data) == 1:
        location = geo_data[0]
        return {'lat': location['lat'], 'lon': location['lon']}

    # 多个结果，让用户选择
    return _prompt_user_choice(geo_data)


def _prompt_user_choice(locations):
    """让用户从多个地点中选择一个。

    Args:
        locations: 地点列表

    Returns:
        dict: 包含 'lat' 和 'lon' 的字典
    """
    print(f"找到多个匹配地点：")
    for i, loc in enumerate(locations, 1):
        name = loc.get('name', '未知')
        state = loc.get('state', '')
        country = loc.get('country', '未知')
        # 优雅处理空 state
        location_str = f"{name}, {state}, {country}" if state else f"{name}, {country}"
        print(f"  {i}. {location_str}")

    while True:
        try:
            choice = int(input("请输入序号选择："))
            if 1 <= choice <= len(locations):
                loc = locations[choice - 1]
                return {'lat': loc['lat'], 'lon': loc['lon']}
            print(f"请输入 1 到 {len(locations)} 之间的数字")
        except ValueError:
            print("请输入有效的数字")

if __name__ == "__main__":
    user_args = read_user_cli_args()
    geo_info = get_geocoding(" ".join(user_args.city))
    print(f"选择的城市地理信息: 纬度 {geo_info['lat']}, 经度 {geo_info['lon']}")
