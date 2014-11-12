install:
	@mkdir -p /var/www
	@cp -rf /lib/webui/* /var/www/
	@chmod 775 /var/www/_OS_SETTINGS/etc/rc.local
	@chmod 755 /var/www/_OS_SETTINGS/etc/php5/mods-available/apc.ini
	@chmod -R 777 /var/www/command/
	@chmod -R 777 /var/www/db/
	@chmod -R 777 /var/www/inc/
	@sed -i s/9000/19000/g /var/www/_OS_SETTINGS/etc/php5/fpm/pool.d/display.conf
	@sed -i s/9001/19001/g /var/www/_OS_SETTINGS/etc/php5/fpm/pool.d/db.conf
	@sed -i s/9002/19002/g /var/www/_OS_SETTINGS/etc/php5/fpm/pool.d/command.conf
	@sed -i s/80/19080/g /var/www/_OS_SETTINGS/etc/nginx/nginx.conf
	@sed -i s/81/19081/g /var/www/_OS_SETTINGS/etc/nginx/nginx.conf
	@sed -i s/82/19082/g /var/www/_OS_SETTINGS/etc/nginx/nginx.conf
	@sed -i s/9000/19000/g /var/www/_OS_SETTINGS/etc/nginx/nginx.conf
	@sed -i s/9001/19001/g /var/www/_OS_SETTINGS/etc/nginx/nginx.conf
	@sed -i s/9002/19002/g /var/www/_OS_SETTINGS/etc/nginx/nginx.conf
	@cp -var /var/www/_OS_SETTINGS/etc /
	@ln -s /media /var/lib/mpd/music/SHARED
	@chown 1913 -R /var/www
	@usermod -a -G audio www-data
	@mkdir -p /var/lib/mpd/music/WEBRADIO
	@chmod 777 /var/lib/mpd/music/WEBRADIO
	@cp -f /lib/webraio/* /var/lib/mpd/music/WEBRADIO/
	@chown root:root /etc/init.d/shairport
	@chmod a+x /etc/init.d/shairport
	@/lib/shairport/configure
	@sed -i 's/^#auto_update .*/auto_update\t"yes"/g' /etc/mpd.conf
	@sed -i 's/^#auto_update_depth.*/auto_update_depth\t"5"/g' /etc/mpd.conf 
	@sed -i 's/^#follow_outside_symlinks.*/follow_outside_symlinks\t"yes"/g' /etc/mpd.conf
	@sed -i 's/^#follow_inside_symlinks.*/follow_inside_symlinks\t"yes"/g' /etc/mpd.conf 
	@echo 'audio_output {' >> /etc/mpd.conf
	@echo '        type      "alsa"' >> /etc/mpd.conf
	@echo '        name      "Card1 device"' >> /etc/mpd.conf
	@echo '        device    "hw:1,0"' >> /etc/mpd.conf
	@echo '        dsd_usb   "yes"' >> /etc/mpd.conf
	@echo '}' >> /etc/mpd.conf
	@echo "Finish volumio library install."
