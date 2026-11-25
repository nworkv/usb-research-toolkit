#!/usr/bin/env python3
"""Regression test: report overview is compact and technical details are collapsed."""
import importlib.util
import sys
from pathlib import Path

script = Path(__file__).resolve().parents[1] / "scripts" / "report-usb-campaign.py"
spec = importlib.util.spec_from_file_location("report_usb_campaign", script)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

case = {
    "case": 1, "verdict": "EXPECTED_DESCRIPTOR_BYTES_MATCH_CONFIGURED_OBSERVED",
    "profile_name": "hid-mouse", "profile": "case-00001.json", "profile_sha256": "abc",
    "run_status": "COMPLETED", "trace": "trace.jsonl", "changes": ["payload byte changed"],
    "host_session_match": {"status": "MATCHED"}, "host_session_id": "session-1",
    "host_groups_in_window": 12, "correlation_mode": "sequential",
    "host_set_configuration": [{"value": 1, "complete_seen": True, "error": False, "status": "COMPLETED", "frames": [20, 21]}],
    "device_trace_summary": {"control_request_count": 2, "control_response_complete_count": 2,
                             "configured_observed": True, "stall_count": 0, "reset_count": 0,
                             "disconnect_count": 0, "error_count": 0},
    "host_errors": [], "host_cancellations": [], "host_teardown_events": [],
    "byte_correlation_status": "ALL_THREE_BYTE_STREAMS_MATCH",
    "warnings": [], "descriptor_transactions": [], "device_trace_descriptor_transactions": [],
    "correlated_data_transfers": [], "expected_descriptor_catalogue": [],
    "configuration_comparison": {"entries": [], "observed_descriptor_count": 0,
                                  "not_requested_count": 0, "partial_count": 0, "different_count": 0},
}
report = {
    "campaign_dir": ".", "host_pcap": "capture.pcapng", "created_utc": "now",
    "cases": [case], "status_counts": {},
    "device_reconciliation": {"sent_devices": [], "sent_count": 1,
                              "observed_serial_count": 0, "matching_mode": "sequential"},
    "host_capture_inventory": {"control_transfer_count": 0, "get_descriptor_count": 0, "devices": []},
    "limitations": ["USBPcap is a host-stack capture."]
}
out = module.build_html(report)
assert '<details class="case good">' in out
assert 'exchange-group' in out
assert '<details class="global-details">' in out
assert "Побайтовая проверка дескрипторов" in out
assert "Дополнительное сравнение endpoint/control" in out
assert '<details class="technical">' in out
assert "байты отправки не извлечены" not in out.lower()
assert "после исключения первых шести" not in out.lower()
assert "Что Raw Gadget записал в trace" in out


print("test_report_html_collapsible: PASS")
