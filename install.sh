sudo apt-get install sooperlooper
sudo apt-get install liblo-dev
sudo apt install libffi-dev
sudo apt-get install jackd
sudo pip3 install -U git+https://github.com/basil-huber/redlooper.git#egg=redlooper

# autostart
sudo cp redlooper.desktop /home/pi/.config/autostart/
#mkdir -p ~/.config/systemd/user
#cp redlooper.service ~/.config/systemd/user
#systemctl --user enable redlooper
