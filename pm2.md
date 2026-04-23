# PM2 Process Configuration

This project uses [PM2](https://keymetrics.io) to manage the `DisplayApp` process. It handles hardware-level execution (as root), automatic restarts, and "watch" mode.

## Standard Setup (Recommended)
Since an `ecosystem.config.js` exists in the repository, you can launch the entire app with a single command:

```bash
sudo pm2 start ecosystem.config.js
```

## Manual Setup
If you need to run the script manually or the ecosystem file is unavailable, use the following command to ensure the correct hardware flags for the 16x32 matrix are applied:

```bash
sudo pm2 start display_control.py \
  --name DisplayApp \
  --watch \
  -- \
  --led-rows 16 \
  --led-cols 32 \
  --led-slowdown-gpio 2
```

## Persistence
To ensure the counter starts automatically when the Raspberry Pi boots:
1. Generate startup script: `sudo pm2 startup`
2. Run the command provided in the output.
3. Save the current list: `sudo pm2 save`

## Monitoring
- **Logs:** `sudo pm2 logs DisplayApp`
- **Status:** `sudo pm2 list`
- **Dashboard:** `sudo pm2 monit`

