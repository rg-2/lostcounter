module.exports = {
  apps : [{
    name   : "DisplayApp",
    script : "display_control.py",
    args: "--led-rows 16 --led-cols 32 --led-slowdown-gpio 2",
    interpreter: 'python3',
    error_file: '/home/pi/.pm2/log/err.log',
    out_file: '/home/pi/.pm2/log/out.log',
    log_file: '/home/pi/.pm2/log/combined.log',
    watch: true
  }]
}
