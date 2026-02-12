# EchoHola: Camera Access Over Local Network

To use the camera when accessing EchoHola from another device on your network (e.g., `http://192.168.1.174:5000`), you must use a **Secure Context**.

## Option 1: Run with HTTPS (Recommended)

I have updated the application to support an ad-hoc SSL certificate. This will allow the browser to treat the connection as secure enough for camera access.

1. **Install new dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: This adds `pyopenssl`)*

2. **Run the application with the `--https` flag:**
   ```bash
   python app.py --https
   ```

3. **Access the app:**
   Open `https://<YOUR_IP>:5000` in your browser.
   > [!IMPORTANT]
   > Your browser will show a "Your connection is not private" warning because the certificate is self-signed. Click **Advanced** and then **Proceed to ... (unsafe)**.

## Option 2: Browser Workaround (Chrome/Edge)

If you don't want to use HTTPS, you can tell your browser to trust the specific IP address.

1. Open a new tab and go to: `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
2. **Enable** the "Insecure origins treated as secure" flag.
3. In the text box, enter your application address: `http://192.168.1.174:5000`
4. Relaunch the browser.
