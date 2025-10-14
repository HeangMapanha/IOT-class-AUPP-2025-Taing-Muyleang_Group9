import socket
from time import time, localtime

# Data shared from main.py
slots = {}             # live slots
closed_tickets = []    # closed tickets list

# Helper functions
def format_time(t):
    lt = localtime(t)
    return "{:02d}:{:02d}:{:02d}".format(lt[3], lt[4], lt[5])

def get_dashboard_html():
    free_count = sum(1 for s in slots.values() if not s["occupied"])
    occupied_count = sum(1 for s in slots.values() if s["occupied"])
    status = "Available" if free_count > 0 else "FULL"

    # Slots panel
    slots_html = ""
    for sn, s in slots.items():
        if s["occupied"]:
            elapsed = int(time() - s["time_in"])
            minutes = elapsed // 60
            seconds = elapsed % 60
            slots_html += f"<tr><td>S{sn}</td><td>Occupied</td><td>{s['id']}</td><td>{format_time(s['time_in'])}</td><td>{minutes}m {seconds}s</td></tr>"
        else:
            slots_html += f"<tr><td>S{sn}</td><td>Free</td><td>-</td><td>-</td><td>-</td></tr>"

    # Active tickets
    active_html = ""
    for sn, s in slots.items():
        if s["occupied"]:
            elapsed = int(time() - s["time_in"])
            minutes = elapsed // 60
            seconds = elapsed % 60
            active_html += f"<tr><td>{s['id']}</td><td>S{sn}</td><td>{format_time(s['time_in'])}</td><td>{minutes}m {seconds}s</td></tr>"

    # Closed tickets
    closed_html = ""
    for c in closed_tickets:
        closed_html += f"<tr><td>{c['id']}</td><td>S{c['slot']}</td><td>{c['duration']}</td><td>${c['fee']:.2f}</td><td>{c['time_out']}</td></tr>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Parking Dashboard</title>
        <meta http-equiv="refresh" content="3">
        <style>
            body {{ font-family: Arial; }}
            h1 {{ text-align:center; }}
            table {{ width: 90%; margin: 10px auto; border-collapse: collapse; }}
            th, td {{ border: 1px solid #333; padding: 6px; text-align: center; }}
            th {{ background-color: #444; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .status-bar {{ width: 90%; margin: 10px auto; padding: 10px; background-color: #ddd; text-align: center; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Smart Parking Dashboard</h1>
        <div class="status-bar">
            Total Slots: 3 | Free: {free_count} | Occupied: {occupied_count} | Status: {status}
        </div>

        <h2>Slots Panel</h2>
        <table>
            <tr><th>Slot</th><th>Status</th><th>ID</th><th>Time-In</th><th>Elapsed</th></tr>
            {slots_html}
        </table>

        <h2>Active (OPEN) Tickets</h2>
        <table>
            <tr><th>ID</th><th>Slot</th><th>Time-In</th><th>Elapsed</th></tr>
            {active_html}
        </table>

        <h2>Recent (CLOSED) Tickets</h2>
        <table>
            <tr><th>ID</th><th>Slot</th><th>Duration</th><th>Fee</th><th>Time-Out</th></tr>
            {closed_html}
        </table>
    </body>
    </html>
    """
    return html

# Web server
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Web server running on http://0.0.0.0:80")

    while True:
        cl, addr = s.accept()
        try:
            cl_file = cl.makefile('rwb', 0)
            request_line = cl_file.readline()
            while True:
                h = cl_file.readline()
                if h == b'' or h == b'\r\n':
                    break
            response = get_dashboard_html()
            cl.send(b"HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
            cl.send(response.encode('utf-8'))
        except Exception as e:
            print("Error serving request:", e)
        finally:
            cl.close()
