#!/usr/bin/env python3
"""
Client04.py - 2507302045 - Quản lý cấu hình trading bot từ xa
Chạy trên Android (Termux) để thay đổi cấu hình database
"""

import requests
import json
import os
import sys
import time
import threading
from datetime import datetime

# Cấu hình
SERVER_URL = "https://2506260734c7.ngrok-free.app"  # Ngrok URL
TIMEOUT = 10


class ConfigManager:
    def __init__(self, server_url):
        self.server_url = server_url
        self.session = requests.Session()
        self.session.timeout = TIMEOUT

    def test_connection(self):
        """Test kết nối đến server"""
        try:
            response = self.session.get(f"{self.server_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                return data.get('status') == 'healthy'
            return False
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False

    def get_all_config(self):
        """Lấy toàn bộ cấu hình"""
        try:
            response = self.session.get(f"{self.server_url}/api/config")
            if response.status_code == 200:
                return response.json()['config']
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

    def update_setting(self, key, value):
        """Cập nhật setting"""
        try:
            data = {'key': key, 'value': value}
            response = self.session.put(f"{self.server_url}/api/config/settings", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False)
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False

    def update_strategy(self, strategy_name, strategy_type):
        """Cập nhật strategy"""
        try:
            data = {'strategy_name': strategy_name, 'strategy_type': strategy_type}
            response = self.session.put(f"{self.server_url}/api/config/strategies", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False)
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False

    def update_strategy_config(self, strategy_name, symbol, volume, stop_loss, take_profit, timeframe):
        """Cập nhật strategy config"""
        try:
            data = {
                'strategy_name': strategy_name,
                'symbol': symbol,
                'volume': volume,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'timeframe': timeframe
            }
            response = self.session.put(f"{self.server_url}/api/config/strategy-config", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False)
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False

    def update_test_setting(self, key, value):
        """Cập nhật test setting"""
        try:
            data = {'key': key, 'value': value}
            response = self.session.put(f"{self.server_url}/api/config/test-settings", json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get('success', False)
            return False
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return False

    def refresh_bot(self):
        """Gửi lệnh refresh bot"""
        try:
            response = self.session.post(f"{self.server_url}/api/refresh-bot")
            if response.status_code == 200:
                result = response.json()
                return True, result.get('message', 'Refresh bot thành công')
            else:
                error_data = response.json()
                return False, error_data.get('message', 'Lỗi không xác định')
        except Exception as e:
            return False, f"Lỗi kết nối: {e}"

    def get_mt5_account_info(self):
        """Lấy thông tin tài khoản MT5"""
        try:
            response = self.session.get(f"{self.server_url}/api/mt5-account-info")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

    def get_config_info(self):
        """Lấy thông tin cấu hình từ server"""
        try:
            response = self.session.get(f"{self.server_url}/api/config")
            if response.status_code == 200:
                data = response.json()
                return data.get('config', {}).get('settings', {})
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return {}

    # Firebase Management Methods
    def get_firebase_collections(self):
        """Lấy danh sách tất cả collections trong Firebase"""
        try:
            response = self.session.get(f"{self.server_url}/api/firebase/collections")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

    def get_collection_stats(self, collection_name):
        """Lấy thống kê của một collection"""
        try:
            response = self.session.get(f"{self.server_url}/api/firebase/collection/{collection_name}/stats")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

    def clear_collection(self, collection_name):
        """Xóa toàn bộ documents trong một collection"""
        try:
            response = self.session.delete(f"{self.server_url}/api/firebase/collection/{collection_name}/clear")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

    def clear_old_documents(self, collection_name, days):
        """Xóa documents cũ trong một collection dựa trên số ngày"""
        try:
            response = self.session.delete(
                f"{self.server_url}/api/firebase/collection/{collection_name}/clear-old?days={days}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

    def get_collection_documents(self, collection_name, limit=50, offset=0):
        """Lấy danh sách documents trong một collection"""
        try:
            response = self.session.get(
                f"{self.server_url}/api/firebase/collection/{collection_name}/documents?limit={limit}&offset={offset}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

    def delete_document(self, collection_name, document_id):
        """Xóa một document cụ thể"""
        try:
            response = self.session.delete(f"{self.server_url}/api/firebase/document/{collection_name}/{document_id}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

    def update_document(self, collection_name, document_id, data):
        """Cập nhật một document cụ thể"""
        try:
            response = self.session.put(f"{self.server_url}/api/firebase/document/{collection_name}/{document_id}",
                                        json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Lỗi HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None


def clear_screen():
    """Xóa màn hình"""
    os.system('clear' if os.name == 'posix' else 'cls')


def show_header():
    """Hiển thị header"""
    print("=" * 60)
    print("🤖 QUẢN LÝ CẤU HÌNH TRADING BOT")
    print("=" * 60)
    print(f"📡 Server: {SERVER_URL}")
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)


def show_mt5_account_info(config_manager):
    """Hiển thị thông tin tài khoản MT5 với cập nhật realtime"""
    # Biến để kiểm soát vòng lặp
    stop_updating = False
    update_count = 0

    def check_for_enter():
        """Thread để kiểm tra phím Enter"""
        nonlocal stop_updating
        input("Nhấn Enter để dừng cập nhật...")
        stop_updating = True

    # Bắt đầu thread kiểm tra phím Enter
    enter_thread = threading.Thread(target=check_for_enter, daemon=True)
    enter_thread.start()

    print("🔄 Bắt đầu cập nhật realtime mỗi 30 giây...")
    time.sleep(0.5)

    while not stop_updating:
        try:
            update_count += 1

            # Xóa màn hình và hiển thị header
            clear_screen()
            print("=" * 60)
            print("🤖 QUẢN LÝ CẤU HÌNH TRADING BOT")
            print("=" * 60)
            print(f"📡 Server: {SERVER_URL}")
            print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 60)
            print("💰 THÔNG TIN TÀI KHOẢN MT5 (REALTIME)")
            print("=" * 60)

            # Hiển thị trạng thái cập nhật
            loading_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            loading_char = loading_chars[update_count % len(loading_chars)]
            print(f"{loading_char} Đang cập nhật... (Lần thứ {update_count})")

            # Lấy thông tin tài khoản MT5
            account_info = config_manager.get_mt5_account_info()
            if not account_info:
                print("❌ Không thể lấy thông tin tài khoản MT5")
                print("Có thể do:")
                print("  - Bot chưa khởi động")
                print("  - MT5 chưa kết nối")
                print("  - Server không hỗ trợ API này")
                print("\n🔄 Đang thử lại...")
                time.sleep(3)
                continue

            # Hiển thị thông tin tài khoản
            if 'account' in account_info:
                account = account_info['account']
                print("\n📊 THÔNG TIN TÀI KHOẢN:")
                print(f"  🆔 Login: {account.get('login', 'N/A')}")
                print(f"  🏦 Server: {account.get('server', 'N/A')}")
                print(f"  💰 Balance: ${account.get('balance', 0):,.2f}")
                print(f"  💵 Equity: ${account.get('equity', 0):,.2f}")
                print(f"  📈 Profit: ${account.get('profit', 0):,.2f}")
                print(f"  💳 Margin: ${account.get('margin', 0):,.2f}")
                print(f"  🔒 Free Margin: ${account.get('free_margin', 0):,.2f}")
                print(f"  📊 Margin Level: {account.get('margin_level', 0):,.2f}%")
                print(f"  🎯 Currency: {account.get('currency', 'N/A')}")

            # Hiển thị các lệnh đang mở
            if 'positions' in account_info:
                positions = account_info['positions']
                print(f"\n📋 LỆNH ĐANG MỞ ({len(positions)} lệnh):")
                if positions:
                    print(
                        f"{'Ticket':<10} {'Symbol':<10} {'Type':<6} {'Volume':<8} {'Price':<10} {'Profit':<12} {'Comment':<15}")
                    print("-" * 80)
                    for pos in positions:
                        ticket = pos.get('ticket', 'N/A')
                        symbol = pos.get('symbol', 'N/A')
                        pos_type = 'BUY' if pos.get('type', 0) == 0 else 'SELL'
                        volume = pos.get('volume', 0)
                        price = pos.get('price_open', 0)
                        profit = pos.get('profit', 0)
                        comment = pos.get('comment', 'N/A')

                        # Thêm màu sắc cho profit
                        profit_str = f"${profit:<11.2f}"
                        if profit > 0:
                            profit_str = f"📈 {profit_str}"
                        elif profit < 0:
                            profit_str = f"📉 {profit_str}"

                        print(
                            f"{ticket:<10} {symbol:<10} {pos_type:<6} {volume:<8.2f} {price:<10.5f} {profit_str} {comment:<15}")
                else:
                    print("  Không có lệnh nào đang mở")

            # Lấy thông tin cấu hình
            config_info = config_manager.get_config_info()

            # Hiển thị thống kê
            if 'summary' in account_info:
                summary = account_info['summary']
                print(f"\n📈 THỐNG KÊ:")
                print(f"  📊 Tổng lệnh mở: {summary.get('total_positions', 0)}")
                print(f"  💰 Tổng profit: ${summary.get('total_profit', 0):,.2f}")
                print(f"  📈 Lệnh có lãi: {summary.get('profitable_positions', 0)}")
                print(f"  📉 Lệnh thua lỗ: {summary.get('losing_positions', 0)}")

                # Thêm thông tin cấu hình
                if config_info:
                    print(f"\n⚙️ CẤU HÌNH:")
                    balance_at_5am = float(config_info.get('balanceat5am', 0))
                    min_balance = float(config_info.get('minbalance', 0))
                    drawdown_limit = float(config_info.get('drawdown', 0))
                    daily_profit_target = float(config_info.get('dailyprofittarget', 0))
                    current_profit = account.get('profit', 0)

                    print(f"  💰 Balance at 5AM: ${balance_at_5am:,.2f}")
                    print(f"  🔒 Min Balance: ${min_balance:,.2f}")
                    print(f"  📉 Drawdown Limit: ${drawdown_limit:,.2f}")
                    print(f"  🎯 Daily Profit Target: ${daily_profit_target:,.2f}")
                    print(f"  📊 Profit hiện tại: ${current_profit:,.2f}")

                    # Tính toán thêm
                    current_balance = account.get('balance', 0)
                    daily_profit = current_balance - balance_at_5am
                    drawdown_used = balance_at_5am - current_balance

                    print(f"\n📊 PHÂN TÍCH:")
                    print(f"  📈 Daily Profit: ${daily_profit:,.2f}")
                    print(f"  📉 Drawdown Used: ${drawdown_used:,.2f}")

                    # Hiển thị trạng thái
                    if daily_profit >= daily_profit_target:
                        print(f"  🎯 Daily Target: ✅ ĐẠT MỤC TIÊU")
                    else:
                        remaining = daily_profit_target - daily_profit
                        print(f"  🎯 Daily Target: ⏳ Còn ${remaining:,.2f}")

                    if drawdown_used >= drawdown_limit:
                        print(f"  📉 Drawdown: ⚠️ VƯỢT GIỚI HẠN")
                    else:
                        remaining_dd = drawdown_limit - drawdown_used
                        print(f"  📉 Drawdown: ✅ Còn ${remaining_dd:,.2f}")

                    if current_balance < min_balance:
                        print(f"  🔒 Min Balance: ⚠️ DƯỚI GIỚI HẠN")
                    else:
                        print(f"  🔒 Min Balance: ✅ AN TOÀN")

            # Hiển thị thời gian cập nhật
            if 'timestamp' in account_info:
                timestamp = account_info['timestamp']
                print(f"\n⏰ Cập nhật lúc: {timestamp}")

            print("\n" + "=" * 60)
            print(f"🔄 Cập nhật lần thứ {update_count} - Mỗi 30 giây - Nhấn Enter để dừng")

            # Chờ 30 giây trước khi cập nhật lại
            time.sleep(30)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Lỗi khi cập nhật: {e}")
            print("🔄 Đang thử lại...")
            time.sleep(3)

    print("\n✅ Đã dừng cập nhật realtime")
    input("Nhấn Enter để quay lại menu chính...")


def show_settings_management(config_manager):
    """Hiển thị menu quản lý Settings"""
    while True:
        clear_screen()
        show_header()

        print("⚙️ QUẢN LÝ SETTINGS")
        print("=" * 60)
        print("Chức năng quản lý cấu hình cơ bản của bot:")
        print("  - Xem danh sách settings hiện tại")
        print("  - Cập nhật setting cụ thể")
        print("  - Thêm setting mới")
        print("-" * 60)

        # Lấy thông tin settings hiện tại
        config = config_manager.get_all_config()
        if config and 'settings' in config:
            settings = config['settings']
            print(f"📊 Settings hiện tại ({len(settings)} items):")
            print("-" * 60)

            if settings:
                for i, (key, value) in enumerate(settings.items(), 1):
                    print(f"  {i:2d}. {key}: {value}")
            else:
                print("  Không có settings nào")

            print("-" * 60)

        print("🔧 MENU SETTINGS:")
        print("  1. 📋 Xem danh sách Settings")
        print("  2. ✏️ Cập nhật Setting")
        print("  3. ➕ Thêm Setting mới")
        print("  0. 🔙 Quay lại menu chính")
        print("-" * 60)

        choice = input("Chọn chức năng (0-3): ").strip()

        if choice == '0':
            break
        elif choice == '1':
            show_settings_list(config_manager)
        elif choice == '2':
            show_update_setting(config_manager)
        elif choice == '3':
            show_add_setting(config_manager)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để tiếp tục...")


def show_settings_list(config_manager):
    """Hiển thị danh sách settings"""
    clear_screen()
    show_header()

    print("📋 DANH SÁCH SETTINGS")
    print("=" * 60)

    try:
        config = config_manager.get_all_config()
        if config and 'settings' in config:
            settings = config['settings']

            if settings:
                print(f"✅ Tìm thấy {len(settings)} settings:")
                print("-" * 60)

                for i, (key, value) in enumerate(settings.items(), 1):
                    print(f"  {i:2d}. {key}: {value}")

                print("-" * 60)
                print(f"📊 Tổng cộng: {len(settings)} settings")
            else:
                print("❌ Không có settings nào")
        else:
            print("❌ Không thể lấy thông tin settings")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_update_setting(config_manager):
    """Hiển thị chức năng cập nhật setting"""
    clear_screen()
    show_header()

    print("✏️ CẬP NHẬT SETTING")
    print("=" * 60)

    # Lấy danh sách settings
    config = config_manager.get_all_config()
    if not config or 'settings' not in config:
        print("❌ Không thể lấy danh sách settings")
        input("Nhấn Enter để quay lại...")
        return

    settings = config['settings']
    if not settings:
        print("❌ Không có settings nào để cập nhật")
        input("Nhấn Enter để quay lại...")
        return

    print("📋 Chọn setting để cập nhật:")
    settings_list = list(settings.items())
    for i, (key, value) in enumerate(settings_list, 1):
        print(f"  {i:2d}. {key}: {value}")

    print("-" * 60)

    try:
        choice = input("Nhập số thứ tự hoặc tên setting: ").strip()

        # Xác định setting key
        setting_key = None
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(settings_list):
                setting_key = settings_list[choice_num - 1][0]
            else:
                print("❌ Số thứ tự không hợp lệ")
                input("Nhấn Enter để quay lại...")
                return
        else:
            if choice in settings:
                setting_key = choice
            else:
                print(f"❌ Không tìm thấy setting '{choice}'")
                input("Nhấn Enter để quay lại...")
                return

        # Nhập giá trị mới
        current_value = settings[setting_key]
        print(f"\n📝 Setting: {setting_key}")
        print(f"💾 Giá trị hiện tại: {current_value}")

        new_value = input("Nhập giá trị mới: ").strip()
        if not new_value:
            print("❌ Giá trị không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Xác nhận cập nhật
        print(f"\n⚠️ Bạn có chắc chắn muốn cập nhật setting '{setting_key}'?")
        print(f"Từ: {current_value}")
        print(f"Thành: {new_value}")
        confirm = input("Nhập 'UPDATE' để xác nhận: ").strip()

        if confirm == "UPDATE":
            print(f"\n✏️ Đang cập nhật setting '{setting_key}'...")

            success = config_manager.update_setting(setting_key, new_value)
            if success:
                print(f"✅ Đã cập nhật thành công setting '{setting_key}'")
            else:
                print("❌ Lỗi khi cập nhật setting")
        else:
            print("❌ Đã hủy thao tác cập nhật")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_add_setting(config_manager):
    """Hiển thị chức năng thêm setting mới"""
    clear_screen()
    show_header()

    print("➕ THÊM SETTING MỚI")
    print("=" * 60)

    try:
        # Nhập tên setting
        setting_key = input("Nhập tên setting: ").strip()
        if not setting_key:
            print("❌ Tên setting không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Nhập giá trị
        setting_value = input("Nhập giá trị: ").strip()
        if not setting_value:
            print("❌ Giá trị không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Xác nhận thêm
        print(f"\n⚠️ Bạn có chắc chắn muốn thêm setting mới?")
        print(f"Tên: {setting_key}")
        print(f"Giá trị: {setting_value}")
        confirm = input("Nhập 'ADD' để xác nhận: ").strip()

        if confirm == "ADD":
            print(f"\n➕ Đang thêm setting '{setting_key}'...")

            success = config_manager.update_setting(setting_key, setting_value)
            if success:
                print(f"✅ Đã thêm thành công setting '{setting_key}'")
            else:
                print("❌ Lỗi khi thêm setting")
        else:
            print("❌ Đã hủy thao tác thêm")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_strategies_management(config_manager):
    """Hiển thị menu quản lý Strategies"""
    while True:
        clear_screen()
        show_header()

        print("🎯 QUẢN LÝ STRATEGIES")
        print("=" * 60)
        print("Chức năng quản lý các chiến lược trading:")
        print("  - Xem danh sách strategies hiện tại")
        print("  - Cập nhật strategy")
        print("  - Thêm strategy mới")
        print("-" * 60)

        # Lấy thông tin strategies hiện tại
        config = config_manager.get_all_config()
        if config and 'strategies' in config:
            strategies = config['strategies']
            print(f"📊 Strategies hiện tại ({len(strategies)} items):")
            print("-" * 60)

            if strategies:
                for i, (name, strategy_type) in enumerate(strategies.items(), 1):
                    print(f"  {i:2d}. {name}: {strategy_type}")
            else:
                print("  Không có strategies nào")

            print("-" * 60)

        print("🔧 MENU STRATEGIES:")
        print("  1. 📋 Xem danh sách Strategies")
        print("  2. ✏️ Cập nhật Strategy")
        print("  3. ➕ Thêm Strategy mới")
        print("  0. 🔙 Quay lại menu chính")
        print("-" * 60)

        choice = input("Chọn chức năng (0-3): ").strip()

        if choice == '0':
            break
        elif choice == '1':
            show_strategies_list(config_manager)
        elif choice == '2':
            show_update_strategy(config_manager)
        elif choice == '3':
            show_add_strategy(config_manager)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để tiếp tục...")


def show_strategies_list(config_manager):
    """Hiển thị danh sách strategies"""
    clear_screen()
    show_header()

    print("📋 DANH SÁCH STRATEGIES")
    print("=" * 60)

    try:
        config = config_manager.get_all_config()
        if config and 'strategies' in config:
            strategies = config['strategies']

            if strategies:
                print(f"✅ Tìm thấy {len(strategies)} strategies:")
                print("-" * 60)

                for i, (name, strategy_type) in enumerate(strategies.items(), 1):
                    print(f"  {i:2d}. {name}: {strategy_type}")

                print("-" * 60)
                print(f"📊 Tổng cộng: {len(strategies)} strategies")
            else:
                print("❌ Không có strategies nào")
        else:
            print("❌ Không thể lấy thông tin strategies")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_update_strategy(config_manager):
    """Hiển thị chức năng cập nhật strategy"""
    clear_screen()
    show_header()

    print("✏️ CẬP NHẬT STRATEGY")
    print("=" * 60)

    # Lấy danh sách strategies
    config = config_manager.get_all_config()
    if not config or 'strategies' not in config:
        print("❌ Không thể lấy danh sách strategies")
        input("Nhấn Enter để quay lại...")
        return

    strategies = config['strategies']
    if not strategies:
        print("❌ Không có strategies nào để cập nhật")
        input("Nhấn Enter để quay lại...")
        return

    print("📋 Chọn strategy để cập nhật:")
    strategies_list = list(strategies.items())
    for i, (name, strategy_type) in enumerate(strategies_list, 1):
        print(f"  {i:2d}. {name}: {strategy_type}")

    print("-" * 60)

    try:
        choice = input("Nhập số thứ tự hoặc tên strategy: ").strip()

        # Xác định strategy name
        strategy_name = None
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(strategies_list):
                strategy_name = strategies_list[choice_num - 1][0]
            else:
                print("❌ Số thứ tự không hợp lệ")
                input("Nhấn Enter để quay lại...")
                return
        else:
            if choice in strategies:
                strategy_name = choice
            else:
                print(f"❌ Không tìm thấy strategy '{choice}'")
                input("Nhấn Enter để quay lại...")
                return

        # Nhập strategy type mới
        current_type = strategies[strategy_name]
        print(f"\n📝 Strategy: {strategy_name}")
        print(f"💾 Loại hiện tại: {current_type}")

        print("\n📋 Các loại strategy có sẵn:")
        print("  - scalping")
        print("  - swing")
        print("  - trend")
        print("  - mean_reversion")
        print("  - breakout")

        new_type = input("Nhập loại strategy mới: ").strip()
        if not new_type:
            print("❌ Loại strategy không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Xác nhận cập nhật
        print(f"\n⚠️ Bạn có chắc chắn muốn cập nhật strategy '{strategy_name}'?")
        print(f"Từ: {current_type}")
        print(f"Thành: {new_type}")
        confirm = input("Nhập 'UPDATE' để xác nhận: ").strip()

        if confirm == "UPDATE":
            print(f"\n✏️ Đang cập nhật strategy '{strategy_name}'...")

            success = config_manager.update_strategy(strategy_name, new_type)
            if success:
                print(f"✅ Đã cập nhật thành công strategy '{strategy_name}'")
            else:
                print("❌ Lỗi khi cập nhật strategy")
        else:
            print("❌ Đã hủy thao tác cập nhật")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_add_strategy(config_manager):
    """Hiển thị chức năng thêm strategy mới"""
    clear_screen()
    show_header()

    print("➕ THÊM STRATEGY MỚI")
    print("=" * 60)

    try:
        # Nhập tên strategy
        strategy_name = input("Nhập tên strategy: ").strip()
        if not strategy_name:
            print("❌ Tên strategy không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Nhập loại strategy
        print("\n📋 Các loại strategy có sẵn:")
        print("  - scalping")
        print("  - swing")
        print("  - trend")
        print("  - mean_reversion")
        print("  - breakout")

        strategy_type = input("Nhập loại strategy: ").strip()
        if not strategy_type:
            print("❌ Loại strategy không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Xác nhận thêm
        print(f"\n⚠️ Bạn có chắc chắn muốn thêm strategy mới?")
        print(f"Tên: {strategy_name}")
        print(f"Loại: {strategy_type}")
        confirm = input("Nhập 'ADD' để xác nhận: ").strip()

        if confirm == "ADD":
            print(f"\n➕ Đang thêm strategy '{strategy_name}'...")

            success = config_manager.update_strategy(strategy_name, strategy_type)
            if success:
                print(f"✅ Đã thêm thành công strategy '{strategy_name}'")
            else:
                print("❌ Lỗi khi thêm strategy")
        else:
            print("❌ Đã hủy thao tác thêm")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_strategy_config_management(config_manager):
    """Hiển thị menu quản lý Strategy Config"""
    while True:
        clear_screen()
        show_header()

        print("⚙️ QUẢN LÝ STRATEGY CONFIG")
        print("=" * 60)
        print("Chức năng quản lý cấu hình chi tiết cho từng strategy:")
        print("  - Xem danh sách strategy configs")
        print("  - Cập nhật strategy config")
        print("  - Thêm strategy config mới")
        print("-" * 60)

        # Lấy thông tin strategy configs hiện tại
        config = config_manager.get_all_config()
        if config and 'strategy_config' in config:
            strategy_configs = config['strategy_config']
            print(f"📊 Strategy Configs hiện tại ({len(strategy_configs)} items):")
            print("-" * 60)

            if strategy_configs:
                for i, (name, config_data) in enumerate(strategy_configs.items(), 1):
                    symbol = config_data.get('symbol', 'N/A')
                    volume = config_data.get('volume', 'N/A')
                    print(f"  {i:2d}. {name} - {symbol} (Vol: {volume})")
            else:
                print("  Không có strategy configs nào")

            print("-" * 60)

        print("🔧 MENU STRATEGY CONFIG:")
        print("  1. 📋 Xem danh sách Strategy Configs")
        print("  2. ✏️ Cập nhật Strategy Config")
        print("  3. ➕ Thêm Strategy Config mới")
        print("  0. 🔙 Quay lại menu chính")
        print("-" * 60)

        choice = input("Chọn chức năng (0-3): ").strip()

        if choice == '0':
            break
        elif choice == '1':
            show_strategy_configs_list(config_manager)
        elif choice == '2':
            show_update_strategy_config(config_manager)
        elif choice == '3':
            show_add_strategy_config(config_manager)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để tiếp tục...")


def show_strategy_configs_list(config_manager):
    """Hiển thị danh sách strategy configs"""
    clear_screen()
    show_header()

    print("📋 DANH SÁCH STRATEGY CONFIGS")
    print("=" * 60)

    try:
        config = config_manager.get_all_config()
        if config and 'strategy_config' in config:
            strategy_configs = config['strategy_config']

            if strategy_configs:
                print(f"✅ Tìm thấy {len(strategy_configs)} strategy configs:")
                print("-" * 80)
                print(f"{'Tên':<20} {'Symbol':<10} {'Volume':<8} {'SL':<8} {'TP':<8} {'TF':<10}")
                print("-" * 80)

                for name, config_data in strategy_configs.items():
                    symbol = config_data.get('symbol', 'N/A')
                    volume = config_data.get('volume', 'N/A')
                    stop_loss = config_data.get('stop_loss', 'N/A')
                    take_profit = config_data.get('take_profit', 'N/A')
                    timeframe = config_data.get('timeframe', 'N/A')

                    print(f"{name:<20} {symbol:<10} {volume:<8} {stop_loss:<8} {take_profit:<8} {timeframe:<10}")

                print("-" * 80)
                print(f"📊 Tổng cộng: {len(strategy_configs)} strategy configs")
            else:
                print("❌ Không có strategy configs nào")
        else:
            print("❌ Không thể lấy thông tin strategy configs")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_update_strategy_config(config_manager):
    """Hiển thị chức năng cập nhật strategy config"""
    clear_screen()
    show_header()

    print("✏️ CẬP NHẬT STRATEGY CONFIG")
    print("=" * 60)

    # Lấy danh sách strategy configs
    config = config_manager.get_all_config()
    if not config or 'strategy_config' not in config:
        print("❌ Không thể lấy danh sách strategy configs")
        input("Nhấn Enter để quay lại...")
        return

    strategy_configs = config['strategy_config']
    if not strategy_configs:
        print("❌ Không có strategy configs nào để cập nhật")
        input("Nhấn Enter để quay lại...")
        return

    print("📋 Chọn strategy config để cập nhật:")
    configs_list = list(strategy_configs.items())
    for i, (name, config_data) in enumerate(configs_list, 1):
        symbol = config_data.get('symbol', 'N/A')
        volume = config_data.get('volume', 'N/A')
        print(f"  {i:2d}. {name} - {symbol} (Vol: {volume})")

    print("-" * 60)

    try:
        choice = input("Nhập số thứ tự hoặc tên strategy: ").strip()

        # Xác định strategy name
        strategy_name = None
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(configs_list):
                strategy_name = configs_list[choice_num - 1][0]
            else:
                print("❌ Số thứ tự không hợp lệ")
                input("Nhấn Enter để quay lại...")
                return
        else:
            if choice in strategy_configs:
                strategy_name = choice
            else:
                print(f"❌ Không tìm thấy strategy '{choice}'")
                input("Nhấn Enter để quay lại...")
                return

        # Hiển thị thông tin hiện tại
        current_config = strategy_configs[strategy_name]
        print(f"\n📝 Strategy: {strategy_name}")
        print(f"💾 Cấu hình hiện tại:")
        print(f"  - Symbol: {current_config.get('symbol', 'N/A')}")
        print(f"  - Volume: {current_config.get('volume', 'N/A')}")
        print(f"  - Stop Loss: {current_config.get('stop_loss', 'N/A')}")
        print(f"  - Take Profit: {current_config.get('take_profit', 'N/A')}")
        print(f"  - Timeframe: {current_config.get('timeframe', 'N/A')}")

        # Nhập thông tin mới
        print(f"\n📝 Nhập thông tin mới:")
        symbol = input("Symbol (Enter để giữ nguyên): ").strip() or current_config.get('symbol', '')
        volume = input("Volume (Enter để giữ nguyên): ").strip() or current_config.get('volume', '')
        stop_loss = input("Stop Loss (Enter để giữ nguyên): ").strip() or current_config.get('stop_loss', '')
        take_profit = input("Take Profit (Enter để giữ nguyên): ").strip() or current_config.get('take_profit', '')
        timeframe = input("Timeframe (Enter để giữ nguyên): ").strip() or current_config.get('timeframe', '')

        # Xác nhận cập nhật
        print(f"\n⚠️ Bạn có chắc chắn muốn cập nhật strategy config '{strategy_name}'?")
        print(f"Symbol: {symbol}")
        print(f"Volume: {volume}")
        print(f"Stop Loss: {stop_loss}")
        print(f"Take Profit: {take_profit}")
        print(f"Timeframe: {timeframe}")
        confirm = input("Nhập 'UPDATE' để xác nhận: ").strip()

        if confirm == "UPDATE":
            print(f"\n✏️ Đang cập nhật strategy config '{strategy_name}'...")

            success = config_manager.update_strategy_config(strategy_name, symbol, volume, stop_loss, take_profit,
                                                            timeframe)
            if success:
                print(f"✅ Đã cập nhật thành công strategy config '{strategy_name}'")
            else:
                print("❌ Lỗi khi cập nhật strategy config")
        else:
            print("❌ Đã hủy thao tác cập nhật")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_add_strategy_config(config_manager):
    """Hiển thị chức năng thêm strategy config mới"""
    clear_screen()
    show_header()

    print("➕ THÊM STRATEGY CONFIG MỚI")
    print("=" * 60)

    try:
        # Nhập thông tin strategy config
        strategy_name = input("Nhập tên strategy: ").strip()
        if not strategy_name:
            print("❌ Tên strategy không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        symbol = input("Nhập symbol (VD: XAUUSD): ").strip()
        if not symbol:
            print("❌ Symbol không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        volume = input("Nhập volume (VD: 0.01): ").strip()
        if not volume:
            print("❌ Volume không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        stop_loss = input("Nhập stop loss (VD: 50): ").strip()
        if not stop_loss:
            print("❌ Stop loss không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        take_profit = input("Nhập take profit (VD: 100): ").strip()
        if not take_profit:
            print("❌ Take profit không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        timeframe = input("Nhập timeframe (VD: M5): ").strip()
        if not timeframe:
            print("❌ Timeframe không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Xác nhận thêm
        print(f"\n⚠️ Bạn có chắc chắn muốn thêm strategy config mới?")
        print(f"Tên: {strategy_name}")
        print(f"Symbol: {symbol}")
        print(f"Volume: {volume}")
        print(f"Stop Loss: {stop_loss}")
        print(f"Take Profit: {take_profit}")
        print(f"Timeframe: {timeframe}")
        confirm = input("Nhập 'ADD' để xác nhận: ").strip()

        if confirm == "ADD":
            print(f"\n➕ Đang thêm strategy config '{strategy_name}'...")

            success = config_manager.update_strategy_config(strategy_name, symbol, volume, stop_loss, take_profit,
                                                            timeframe)
            if success:
                print(f"✅ Đã thêm thành công strategy config '{strategy_name}'")
            else:
                print("❌ Lỗi khi thêm strategy config")
        else:
            print("❌ Đã hủy thao tác thêm")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_test_settings_management(config_manager):
    """Hiển thị menu quản lý Test Settings"""
    while True:
        clear_screen()
        show_header()

        print("🧪 QUẢN LÝ TEST SETTINGS")
        print("=" * 60)
        print("Chức năng quản lý cấu hình test và debug:")
        print("  - Xem danh sách test settings hiện tại")
        print("  - Cập nhật test setting")
        print("  - Thêm test setting mới")
        print("-" * 60)

        # Lấy thông tin test settings hiện tại
        config = config_manager.get_all_config()
        if config and 'test_settings' in config:
            test_settings = config['test_settings']
            print(f"📊 Test Settings hiện tại ({len(test_settings)} items):")
            print("-" * 60)

            if test_settings:
                for i, (key, value) in enumerate(test_settings.items(), 1):
                    print(f"  {i:2d}. {key}: {value}")
            else:
                print("  Không có test settings nào")

            print("-" * 60)

        print("🔧 MENU TEST SETTINGS:")
        print("  1. 📋 Xem danh sách Test Settings")
        print("  2. ✏️ Cập nhật Test Setting")
        print("  3. ➕ Thêm Test Setting mới")
        print("  0. 🔙 Quay lại menu chính")
        print("-" * 60)

        choice = input("Chọn chức năng (0-3): ").strip()

        if choice == '0':
            break
        elif choice == '1':
            show_test_settings_list(config_manager)
        elif choice == '2':
            show_update_test_setting(config_manager)
        elif choice == '3':
            show_add_test_setting(config_manager)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để tiếp tục...")


def show_test_settings_list(config_manager):
    """Hiển thị danh sách test settings"""
    clear_screen()
    show_header()

    print("📋 DANH SÁCH TEST SETTINGS")
    print("=" * 60)

    try:
        config = config_manager.get_all_config()
        if config and 'test_settings' in config:
            test_settings = config['test_settings']

            if test_settings:
                print(f"✅ Tìm thấy {len(test_settings)} test settings:")
                print("-" * 60)

                for i, (key, value) in enumerate(test_settings.items(), 1):
                    print(f"  {i:2d}. {key}: {value}")

                print("-" * 60)
                print(f"📊 Tổng cộng: {len(test_settings)} test settings")
            else:
                print("❌ Không có test settings nào")
        else:
            print("❌ Không thể lấy thông tin test settings")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_update_test_setting(config_manager):
    """Hiển thị chức năng cập nhật test setting"""
    clear_screen()
    show_header()

    print("✏️ CẬP NHẬT TEST SETTING")
    print("=" * 60)

    # Lấy danh sách test settings
    config = config_manager.get_all_config()
    if not config or 'test_settings' not in config:
        print("❌ Không thể lấy danh sách test settings")
        input("Nhấn Enter để quay lại...")
        return

    test_settings = config['test_settings']
    if not test_settings:
        print("❌ Không có test settings nào để cập nhật")
        input("Nhấn Enter để quay lại...")
        return

    print("📋 Chọn test setting để cập nhật:")
    settings_list = list(test_settings.items())
    for i, (key, value) in enumerate(settings_list, 1):
        print(f"  {i:2d}. {key}: {value}")

    print("-" * 60)

    try:
        choice = input("Nhập số thứ tự hoặc tên test setting: ").strip()

        # Xác định setting key
        setting_key = None
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(settings_list):
                setting_key = settings_list[choice_num - 1][0]
            else:
                print("❌ Số thứ tự không hợp lệ")
                input("Nhấn Enter để quay lại...")
                return
        else:
            if choice in test_settings:
                setting_key = choice
            else:
                print(f"❌ Không tìm thấy test setting '{choice}'")
                input("Nhấn Enter để quay lại...")
                return

        # Nhập giá trị mới
        current_value = test_settings[setting_key]
        print(f"\n📝 Test Setting: {setting_key}")
        print(f"💾 Giá trị hiện tại: {current_value}")

        new_value = input("Nhập giá trị mới: ").strip()
        if not new_value:
            print("❌ Giá trị không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Xác nhận cập nhật
        print(f"\n⚠️ Bạn có chắc chắn muốn cập nhật test setting '{setting_key}'?")
        print(f"Từ: {current_value}")
        print(f"Thành: {new_value}")
        confirm = input("Nhập 'UPDATE' để xác nhận: ").strip()

        if confirm == "UPDATE":
            print(f"\n✏️ Đang cập nhật test setting '{setting_key}'...")

            success = config_manager.update_test_setting(setting_key, new_value)
            if success:
                print(f"✅ Đã cập nhật thành công test setting '{setting_key}'")
            else:
                print("❌ Lỗi khi cập nhật test setting")
        else:
            print("❌ Đã hủy thao tác cập nhật")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_add_test_setting(config_manager):
    """Hiển thị chức năng thêm test setting mới"""
    clear_screen()
    show_header()

    print("➕ THÊM TEST SETTING MỚI")
    print("=" * 60)

    try:
        # Nhập tên test setting
        setting_key = input("Nhập tên test setting: ").strip()
        if not setting_key:
            print("❌ Tên test setting không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Nhập giá trị
        setting_value = input("Nhập giá trị: ").strip()
        if not setting_value:
            print("❌ Giá trị không được để trống")
            input("Nhấn Enter để quay lại...")
            return

        # Xác nhận thêm
        print(f"\n⚠️ Bạn có chắc chắn muốn thêm test setting mới?")
        print(f"Tên: {setting_key}")
        print(f"Giá trị: {setting_value}")
        confirm = input("Nhập 'ADD' để xác nhận: ").strip()

        if confirm == "ADD":
            print(f"\n➕ Đang thêm test setting '{setting_key}'...")

            success = config_manager.update_test_setting(setting_key, setting_value)
            if success:
                print(f"✅ Đã thêm thành công test setting '{setting_key}'")
            else:
                print("❌ Lỗi khi thêm test setting")
        else:
            print("❌ Đã hủy thao tác thêm")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_full_config(config_manager):
    """Hiển thị toàn bộ cấu hình"""
    clear_screen()
    show_header()

    print("📊 TOÀN BỘ CẤU HÌNH")
    print("=" * 60)

    try:
        config = config_manager.get_all_config()
        if config:
            print("✅ Lấy cấu hình thành công!")
            print("=" * 60)

            # Hiển thị Settings
            if 'settings' in config and config['settings']:
                print("⚙️ SETTINGS:")
                print("-" * 40)
                for key, value in config['settings'].items():
                    print(f"  {key}: {value}")
                print()

            # Hiển thị Strategies
            if 'strategies' in config and config['strategies']:
                print("🎯 STRATEGIES:")
                print("-" * 40)
                for name, strategy_type in config['strategies'].items():
                    print(f"  {name}: {strategy_type}")
                print()

            # Hiển thị Strategy Configs
            if 'strategy_config' in config and config['strategy_config']:
                print("⚙️ STRATEGY CONFIGS:")
                print("-" * 40)
                for name, config_data in config['strategy_config'].items():
                    print(f"  {name}:")
                    for key, value in config_data.items():
                        print(f"    {key}: {value}")
                    print()

            # Hiển thị Test Settings
            if 'test_settings' in config and config['test_settings']:
                print("🧪 TEST SETTINGS:")
                print("-" * 40)
                for key, value in config['test_settings'].items():
                    print(f"  {key}: {value}")
                print()

            # Thống kê tổng quan
            print("📈 THỐNG KÊ TỔNG QUAN:")
            print("-" * 40)
            print(f"  Settings: {len(config.get('settings', {}))} items")
            print(f"  Strategies: {len(config.get('strategies', {}))} items")
            print(f"  Strategy Configs: {len(config.get('strategy_config', {}))} items")
            print(f"  Test Settings: {len(config.get('test_settings', {}))} items")

        else:
            print("❌ Không thể lấy cấu hình")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

    print("\n" + "=" * 60)
    input("Nhấn Enter để quay lại...")


def show_main_menu(config_manager):
    """Hiển thị menu chính"""
    while True:
        clear_screen()
        show_header()

        # Test kết nối
        if not config_manager.test_connection():
            print("❌ Không thể kết nối đến server!")
            print("Hãy kiểm tra:")
            print("  - Server có đang chạy không?")
            print("  - IP address có đúng không?")
            print("  - Port 5000 có mở không?")
            print(f"  - URL hiện tại: {SERVER_URL}")
            print("\nNhấn Enter để thử lại...")
            input()
            continue

        print("✅ Kết nối server thành công!")

        # Lấy thông tin cấu hình
        config = config_manager.get_all_config()
        if config:
            print(f"📊 Thống kê:")
            print(f"  - Settings: {len(config['settings'])} items")
            print(f"  - Strategies: {len(config['strategies'])} items")
            print(f"  - Strategy Configs: {len(config['strategy_config'])} items")
            print(f"  - Test Settings: {len(config['test_settings'])} items")

            # Hiển thị trạng thái refresh bot
            test_settings = config['test_settings']
            refresh_status = test_settings.get('refresh_bot', 'N/A')
            print(f"  - Refresh Bot: {refresh_status}")

        print("\n🔧 MENU CHÍNH:")
        print("  1. ⚙️  Quản lý Settings")
        print("  2. 🎯 Quản lý Strategies")
        print("  3. ⚙️  Quản lý Strategy Config")
        print("  4. 🧪 Quản lý Test Settings")
        print("  5. 🔄 Refresh Bot")
        print("  6. 📊 Xem toàn bộ cấu hình")
        print("  7. 💰 Thông tin tài khoản MT5")
        print("  8.  Quản lý Firebase")
        print("  0. 🚪 Thoát")
        print("-" * 60)

        choice = input("Chọn chức năng (0-8): ").strip()

        if choice == '0':
            print("👋 Tạm biệt!")
            break
        elif choice == '1':
            show_settings_management(config_manager)
        elif choice == '2':
            show_strategies_management(config_manager)
        elif choice == '3':
            show_strategy_config_management(config_manager)
        elif choice == '4':
            show_test_settings_management(config_manager)
        elif choice == '5':
            show_refresh_bot(config_manager)
        elif choice == '6':
            show_full_config(config_manager)
        elif choice == '7':
            show_mt5_account_info(config_manager)
        elif choice == '8':
            show_firebase_management(config_manager)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            input("Nhấn Enter để tiếp tục...")


def main():
    """Hàm chính"""
    global SERVER_URL

    print("🚀 KHỞI ĐỘNG CLIENT04.PY")
    print("=" * 60)

    # Kiểm tra kết nối mạng
    print("📡 Kiểm tra kết nối...")

    config_manager = ConfigManager(SERVER_URL)

    if not config_manager.test_connection():
        print(f"❌ Không thể kết nối đến {SERVER_URL}")
        print("\n🔧 HƯỚNG DẪN KHẮC PHỤC:")
        print("1. Đảm bảo server04.py đang chạy trên máy chủ")
        print("2. Kiểm tra IP address trong file client04.py")
        print("3. Đảm bảo port 5000 được mở")
        print("4. Kiểm tra firewall")
        print(f"\nIP hiện tại: {SERVER_URL}")
        change_ip = input("Bạn có muốn thay đổi IP không? (y/n): ").lower()
        if change_ip == 'y':
            new_ip = input("Nhập IP mới: ").strip()
            if new_ip:
                SERVER_URL = f"http://{new_ip}:5000"
                config_manager = ConfigManager(SERVER_URL)
                print(f"✅ Đã thay đổi IP thành: {SERVER_URL}")
                input("Nhấn Enter để tiếp tục...")

    # Hiển thị menu chính
    show_main_menu(config_manager)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Chương trình bị gián đoạn")
        print("👋 Tạm biệt!")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
        print("Hãy kiểm tra lại và thử lại") 