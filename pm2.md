# PM2 Process Configuration

This project uses [PM2](https://keymetrics.io) to manage the execution of the counter script. PM2 handles the hardware-level execution (as root), automatic restarts on failure, and "watch" mode for development.

## Current Setup Details
- **Process Name:** `DisplayApp`
- **Script:** `display_control.py`
- **Interpreter:** `python3`
- **Watch Mode:** Enabled (restarts on file change)

## Launch Command
To recreate the process with the correct hardware flags for the 16x32 matrix, run:

```bash
sudo pm2 start display_control.py \
  --name DisplayApp \
  --watch \
  -- \
  --led-rows 16 \
  --led-cols 32 \
  --led-slowdown-gpio 2
```

## Management Commands

### Persistence (Start on Boot)
To ensure the counter starts automatically when the Raspberry Pi boots:
```bash
sudo pm2 startup
# Follow the on-screen instructions to copy/paste the command provided
sudo pm2 save
```

### Logs & Monitoring
* **View live logs:** `sudo pm2 logs DisplayApp`
* **Check status:** `sudo pm2 list`
* **Process details:** `sudo pm2 describe 0`
* **Monitor CPU/RAM:** `sudo pm2 monit`

### Stopping/Restarting
* **Restart:** `sudo pm2 restart DisplayApp`
* **Stop:** `sudo pm2 stop DisplayApp`
