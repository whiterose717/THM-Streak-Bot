#!/usr/bin/env python3
"""
Export TryHackMe cookies from Firefox for use with THM Streak Bot.

Usage:
    1. Login to tryhackme.com in Firefox
    2. Run: python3 export_cookies.py
    3. Copy the base64 output
    4. Add as GitHub secret: THM_FIREFOX_COOKIES

Requirements:
    pip install requests (only for optional validation)
"""
import sqlite3
import json
import base64
import os
import shutil
import tempfile
import glob


def find_firefox_cookies():
    """Find Firefox cookies.sqlite file."""
    patterns = [
        os.path.expanduser("~/.mozilla/firefox/*/cookies.sqlite"),
        os.path.expanduser("~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite"),
        os.path.expanduser("%APPDATA%\\Mozilla\\Firefox\\Profiles\\*\\cookies.sqlite"),
    ]
    
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]
    
    return None


def export_cookies(cookie_db_path=None):
    """Export THM cookies from Firefox."""
    if not cookie_db_path:
        cookie_db_path = find_firefox_cookies()
    
    if not cookie_db_path:
        print("❌ Firefox cookies.sqlite not found!")
        print("\nManual steps:")
        print("1. Find your Firefox profile folder")
        print("2. Copy the cookies.sqlite file")
        print("3. Run: python3 export_cookies.py /path/to/cookies.sqlite")
        return None
    
    print(f"📁 Found cookies: {cookie_db_path}")
    
    # Copy to temp file (Firefox locks the original)
    tmp = tempfile.mktemp(suffix=".db")
    shutil.copy2(cookie_db_path, tmp)
    
    try:
        conn = sqlite3.connect(tmp)
        cursor = conn.cursor()
        
        # Get all THM cookies
        cursor.execute("""
            SELECT name, value, host, path, expiry, isSecure, isHttpOnly
            FROM moz_cookies 
            WHERE host LIKE '%tryhackme%'
        """)
        
        cookies = []
        for row in cursor.fetchall():
            cookies.append({
                "name": row[0],
                "value": row[1],
                "host": row[2],
                "path": row[3],
                "expiry": row[4],
                "secure": bool(row[5]),
                "httpOnly": bool(row[6]),
            })
        
        conn.close()
        
        if not cookies:
            print("❌ No TryHackMe cookies found!")
            print("\nMake sure you:")
            print("1. Login to tryhackme.com in Firefox")
            print("2. Visit a few pages to set cookies")
            return None
        
        print(f"✅ Found {len(cookies)} THM cookies")
        
        # Encode as base64 JSON
        json_str = json.dumps(cookies, indent=2)
        b64 = base64.b64encode(json_str.encode()).decode()
        
        print(f"\n📋 Base64 output ({len(b64)} chars):")
        print("=" * 60)
        print(b64)
        print("=" * 60)
        
        # Save to file
        output_file = "thm_cookies_b64.txt"
        with open(output_file, "w") as f:
            f.write(b64)
        
        print(f"\n💾 Saved to: {output_file}")
        print("\n📝 Next steps:")
        print("1. Copy the base64 string above")
        print("2. Go to GitHub → Your repo → Settings → Secrets → Actions")
        print("3. Create new secret: THM_FIREFOX_COOKIES")
        print("4. Paste the base64 string as the value")
        
        return b64
        
    except Exception as e:
        print(f"❌ Error reading cookies: {e}")
        return None
    finally:
        # Clean up temp file
        try:
            os.unlink(tmp)
        except:
            pass


def validate_cookies(b64_cookies):
    """Optional: Validate cookies work with THM API."""
    try:
        import requests
        
        cookies_json = base64.b64decode(b64_cookies).decode()
        cookies = json.loads(cookies_json)
        
        session = requests.Session()
        for c in cookies:
            session.cookies.set(c["name"], c["value"], domain=c["host"].lstrip("."), path=c["path"])
        
        r = session.get(
            "https://tryhackme.com/api/v2/auth/csrf",
            headers={"Accept": "application/json"},
            timeout=10
        )
        
        if r.status_code == 200 and "json" in r.headers.get("content-type", ""):
            data = r.json()
            if data.get("status") == "success":
                print("\n✅ Cookies are valid! CSRF token obtained.")
                return True
        
        print(f"\n⚠️ Cookie validation failed (status={r.status_code})")
        print("Cookies may be expired. Try re-logging in to THM.")
        return False
        
    except ImportError:
        print("\n💡 Install requests to validate: pip install requests")
        return False
    except Exception as e:
        print(f"\n⚠️ Validation error: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    cookie_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("🍪 THM Streak Bot - Cookie Exporter")
    print("=" * 40)
    
    b64 = export_cookies(cookie_path)
    
    if b64:
        # Optionally validate
        if "--validate" in sys.argv:
            validate_cookies(b64)
        elif "--validate-interactive" in sys.argv:
            response = input("\nValidate cookies? (y/n): ").lower()
            if response == "y":
                validate_cookies(b64)
