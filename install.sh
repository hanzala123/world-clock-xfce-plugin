pip3 install -r requirements.txt
rm -rf build
meson build
cd build
sudo meson install
cd ..