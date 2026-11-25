#!/usr/bin/env python3
"""Tests directional USBPcap exchange rendering in campaign reports."""
import importlib.util
import sys
from pathlib import Path

script = Path(__file__).resolve().parents[1] / "scripts" / "report-usb-campaign.py"
spec = importlib.util.spec_from_file_location("report_usb_exchange", script)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

control_in = {
    "transfer_type": 2, "endpoint_address": 0, "request": {
        "bmRequestType": 0x80, "bRequest": 6, "wValue": 0x0100, "wIndex": 0, "wLength": 18
    }, "payload": bytes.fromhex("120100020000004034125678000102030100"),
    "frame_numbers": [10, 11], "irp_id": "0x01", "bus_id": 1, "device_address": 2,
    "status": "COMPLETED", "complete_seen": True, "rows": []
}
bulk_out = {
    "transfer_type": 3, "endpoint_address": 0x01, "request": None,
    "payload": bytes.fromhex("5553424301000000"), "frame_numbers": [12, 13],
    "irp_id": "0x02", "bus_id": 1, "device_address": 2,
    "status": "COMPLETED", "complete_seen": True, "rows": []
}
bulk_in = {
    "transfer_type": 3, "endpoint_address": 0x82, "request": None,
    "payload": bytes.fromhex("5553425301000000"), "frame_numbers": [14, 15],
    "irp_id": "0x03", "bus_id": 1, "device_address": 2,
    "status": "COMPLETED", "complete_seen": True, "rows": []
}
log = module.make_usb_exchange_log([control_in, bulk_out, bulk_in], "sequential")
assert len(log) == 3
assert log[0]["setup_hex"] == "8006000100001200"
assert log[0]["direction"] == "CONTROL_IN"
assert log[0]["sent_hex"] == "8006000100001200"
assert log[0]["received_hex"] == "120100020000004034125678000102030100"
assert any("idVendor=0x1234" in x for x in log[0]["received_decoded"])
assert log[1]["direction"] == "OUT" and log[1]["sent_hex"] == "5553424301000000"
assert log[2]["direction"] == "IN" and log[2]["received_hex"] == "5553425301000000"
html = module.usb_exchange_html(log[0], 1)
assert "ОТПРАВЛЕНО · HOST → DEVICE" in html
assert "ПОЛУЧЕНО · DEVICE → HOST" in html
assert "idVendor=0x1234" in html
print("test_usb_exchange_report: PASS")
