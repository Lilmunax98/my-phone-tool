#!/usr/bin/env python3
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests, argparse, urllib.parse

def lookup(number_str, save_html=True):
    if not number_str.startswith('+'):
        number_str = '+' + number_str
    parsed = phonenumbers.parse(number_str, None)
    cc = parsed.country_code
    approx_location = geocoder.description_for_number(parsed, "en")
    sim_carrier = carrier.name_for_number(parsed, "en")

    print(f"\n[+] Number: {number_str}")
    print(f"[+] Approximate Area: {approx_location or 'Unknown'}")
    print(f"[+] Carrier: {sim_carrier or 'Unknown'}")

    maps_query = approx_location
    official_name = approx_location
    try:
        url = f"https://restcountries.com/v3.1/callingcode/{cc}"
        r = requests.get(url, timeout=10, headers={"User-Agent":"my-phone-tool"})
        if r.status_code == 200:
            info = r.json()[0]
            official_name = info['name']['common']
            maps_query = f"{approx_location}, {official_name}" if approx_location else official_name
            print(f"[+] Country: {official_name}")
    except:
        pass

    encoded = urllib.parse.quote(maps_query or official_name or str(cc))
    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={encoded}"
    print(f"[>] Maps URL: {gmaps_url}")

    # Save HTML with embedded map
    html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
    <title>{number_str}</title><style>body{{font-family:sans-serif;padding:20px}}iframe{{width:100%;height:80vh;border:0}}</style>
    </head><body><h2>{number_str}</h2><p>Area: {maps_query}</p><p>Carrier: {sim_carrier}</p>
    <p><b>NOT live GPS - only area from number</b></p>
    <a href='{gmaps_url}' target='_blank'>Open in Google Maps</a><br><br>
    <iframe src='https://maps.google.com/maps?q={encoded}&z=6&output=embed'></iframe>
    </body></html>"""

    filename = f"map_{number_str.replace('+','')}.html"
    with open(filename, "w") as f:
        f.write(html)
    print(f"[+] Saved: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="+263714618476")
    args = parser.parse_args()
    lookup(args.number)
