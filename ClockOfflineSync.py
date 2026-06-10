import json
import time
import requests
from pathlib import Path

BASE_URL = "http://localhost:8000"
STORAGE_FILE = "offline_time_entries.json"


class OfflineSync:

    def __init__(self):
        self.pending_count = 0
        self.syncing = False

    # -----------------------------
    # Storage Helpers
    # -----------------------------

    def get_offline_entries(self):
        try:
            if Path(STORAGE_FILE).exists():
                with open(STORAGE_FILE, "r") as f:
                    return json.load(f)
            return []
        except Exception:
            return []

    def save_entries(self, entries):
        with open(STORAGE_FILE, "w") as f:
            json.dump(entries, f, indent=4)

    def save_offline_entry(self, entry):
        entries = self.get_offline_entries()

        entry["offline_id"] = int(time.time() * 1000)
        entry["pending_sync"] = True

        entries.append(entry)
        self.save_entries(entries)

    def update_offline_entry(self, offline_id, updates):

        entries = self.get_offline_entries()

        for entry in entries:
            if entry["offline_id"] == offline_id:
                entry.update(updates)

        self.save_entries(entries)

    def remove_offline_entry(self, offline_id):

        entries = [
            entry
            for entry in self.get_offline_entries()
            if entry["offline_id"] != offline_id
        ]

        self.save_entries(entries)

    def clear_synced_entries(self):

        unsynced = [
            entry
            for entry in self.get_offline_entries()
            if entry.get("pending_sync")
        ]

        self.save_entries(unsynced)

    # -----------------------------
    # Internet Check
    # -----------------------------

    def is_online(self):
        try:
            requests.get(
                "https://www.google.com",
                timeout=5
            )
            return True
        except Exception:
            return False

    # -----------------------------
    # Sync Logic
    # -----------------------------

    def sync_offline_entries(self):

        entries = [
            e
            for e in self.get_offline_entries()
            if e.get("pending_sync")
        ]

        if not entries:
            print("No pending entries")
            return

        self.syncing = True
        synced = 0

        for entry in entries:

            try:

                # CLOCK IN
                if entry["type"] == "clock_in":

                    response = requests.post(
                        f"{BASE_URL}/time-entries",
                        json={
                            "employee_id":
                                entry["employee_id"],
                            "employee_name":
                                entry["employee_name"],
                            "clock_in_time":
                                entry["clock_in_time"],
                            "clock_in_location":
                                entry["clock_in_location"],
                            "clock_in_method":
                                entry["clock_in_method"],
                            "status":
                                entry["status"],
                            "date":
                                entry["date"],
                            "is_late":
                                entry["is_late"],
                        }
                    )

                    created_entry = response.json()

                    if entry.get("employee_db_id"):

                        requests.put(
                            f"{BASE_URL}/employees/"
                            f"{entry['employee_db_id']}",
                            json={
                                "is_clocked_in": True,
                                "current_session_id":
                                    created_entry["id"],
                            }
                        )

                    self.remove_offline_entry(
                        entry["offline_id"]
                    )

                    synced += 1

                # CLOCK OUT
                elif entry["type"] == "clock_out":

                    sessions = requests.get(
                        f"{BASE_URL}/time-entries"
                        f"?employee_id="
                        f"{entry['employee_id']}"
                        f"&status=active"
                    ).json()

                    active_session = (
                        sessions[0]
                        if sessions
                        else None
                    )

                    if active_session:

                        requests.put(
                            f"{BASE_URL}/time-entries/"
                            f"{active_session['id']}",
                            json={
                                "clock_out_time":
                                    entry["clock_out_time"],
                                "clock_out_location":
                                    entry["clock_out_location"],
                                "status":
                                    "completed",
                                "total_hours":
                                    entry["total_hours"],
                                "overtime_hours":
                                    entry["overtime_hours"],
                            }
                        )

                        if entry.get("employee_db_id"):

                            requests.put(
                                f"{BASE_URL}/employees/"
                                f"{entry['employee_db_id']}",
                                json={
                                    "is_clocked_in":
                                        False,
                                    "current_session_id":
                                        None,
                                }
                            )

                    self.remove_offline_entry(
                        entry["offline_id"]
                    )

                    synced += 1

            except Exception as error:
                print(
                    f"Sync failed: {error}"
                )

        self.syncing = False

        remaining = len([
            e
            for e in self.get_offline_entries()
            if e.get("pending_sync")
        ])

        self.pending_count = remaining

        print(
            f"Synced {synced} entries."
        )
        print(
            f"{remaining} entries remaining."
        )


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":

    sync = OfflineSync()

    if sync.is_online():
        print("Online")
        sync.sync_offline_entries()
    else:
        print("Offline Mode")
